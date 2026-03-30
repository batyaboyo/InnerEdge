"""REST API views for billing and Stripe integration."""

from __future__ import annotations

from django.http import HttpRequest
from django.utils.dateparse import parse_datetime
from rest_framework import decorators, permissions, response, status, viewsets
from rest_framework.views import APIView

from billing.models import Invoice, Plan, Subscription
from billing.serializers import InvoiceSerializer, PlanSerializer, SubscriptionSerializer
from billing.services.stripe_api import build_checkout_session, verify_webhook


class PlanViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Plan.objects.filter(is_active=True)
	serializer_class = PlanSerializer
	permission_classes = [permissions.AllowAny]


class SubscriptionViewSet(viewsets.ModelViewSet):
	serializer_class = SubscriptionSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return Subscription.objects.filter(user=self.request.user).select_related("plan")

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

	@decorators.action(detail=False, methods=["post"], url_path="checkout")
	def checkout(self, request):
		plan_id = request.data.get("plan_id")
		success_url = request.data.get("success_url")
		cancel_url = request.data.get("cancel_url")
		plan = Plan.objects.get(id=plan_id, is_active=True)
		session = build_checkout_session(
			price_id=plan.stripe_price_id,
			customer_email=request.user.email,
			success_url=success_url,
			cancel_url=cancel_url,
		)
		return response.Response({"checkout_url": session.url})


class InvoiceViewSet(viewsets.ReadOnlyModelViewSet):
	serializer_class = InvoiceSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return Invoice.objects.filter(subscription__user=self.request.user)


class StripeWebhookAPIView(APIView):
	"""Handle Stripe webhook events for subscription lifecycle."""

	authentication_classes: list = []
	permission_classes = [permissions.AllowAny]

	def post(self, request: HttpRequest):
		signature = request.headers.get("Stripe-Signature", "")
		event = verify_webhook(request.body, signature)

		if event["type"] == "invoice.paid":
			invoice_data = event["data"]["object"]
			subscription = Subscription.objects.filter(
				stripe_subscription_id=invoice_data.get("subscription", "")
			).first()
			if subscription:
				Invoice.objects.update_or_create(
					stripe_invoice_id=invoice_data["id"],
					defaults={
						"subscription": subscription,
						"amount_paid_cents": invoice_data.get("amount_paid", 0),
						"currency": invoice_data.get("currency", "usd"),
						"status": invoice_data.get("status", "paid"),
						"invoice_pdf_url": invoice_data.get("invoice_pdf", ""),
						"issued_at": parse_datetime(invoice_data.get("status_transitions", {}).get("paid_at", ""))
						or subscription.updated_at,
					},
				)

		return response.Response({"received": True}, status=status.HTTP_200_OK)
