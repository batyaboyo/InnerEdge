"""URL configuration for billing API."""

from __future__ import annotations

from django.urls import path
from rest_framework.routers import DefaultRouter

from billing.views import InvoiceViewSet, PlanViewSet, StripeWebhookAPIView, SubscriptionViewSet

router = DefaultRouter()
router.register("plans", PlanViewSet, basename="plan")
router.register("subscriptions", SubscriptionViewSet, basename="subscription")
router.register("invoices", InvoiceViewSet, basename="invoice")

urlpatterns = router.urls + [
    path("stripe/webhook/", StripeWebhookAPIView.as_view(), name="stripe-webhook"),
]
