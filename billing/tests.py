"""Tests for billing module."""

from decimal import Decimal
from unittest.mock import patch, MagicMock

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

from billing.models import Plan, Subscription
from billing.services.stripe_api import build_checkout_session

User = get_user_model()


class BillingPlanModelTestCase(TestCase):
    def setUp(self):
        self.plan = Plan.objects.create(
            code="pro",
            name="Pro Plan",
            price_monthly_cents=9900,
            features={"max_trades": 100, "alerts": True, "ai_insights": True},
            stripe_product_id="prod_test",
            stripe_price_id="price_test",
        )

    def test_plan_creation(self):
        """Test plan can be created."""
        self.assertEqual(self.plan.code, "pro")
        self.assertEqual(self.plan.price_monthly_cents, 9900)
        self.assertIn("alerts", self.plan.features)

    def test_plan_pricing(self):
        """Test plan pricing."""
        self.assertEqual(self.plan.price_monthly_cents, 9900)
        self.assertEqual(float(self.plan.price_monthly_cents / 100), 99.0)


class SubscriptionModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="trader", email="trader@test.com", password="pass123")
        self.plan = Plan.objects.create(
            code="pro",
            name="Pro Plan",
            price_monthly_cents=9900,
            features={},
            stripe_product_id="prod_test",
            stripe_price_id="price_test",
        )

    def test_subscription_creation(self):
        """Test subscription creation."""
        sub = Subscription.objects.create(
            user=self.user,
            plan=self.plan,
            status=Subscription.Status.ACTIVE,
            stripe_customer_id="cus_test",
            stripe_subscription_id="sub_test",
        )
        self.assertEqual(sub.user, self.user)
        self.assertEqual(sub.plan, self.plan)
        self.assertEqual(sub.status, Subscription.Status.ACTIVE)


class BillingAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="trader", email="trader@test.com", password="pass123")
        self.plan = Plan.objects.create(
            code="pro",
            name="Pro Plan",
            price_monthly_cents=9900,
            features={"alerts": True},
            stripe_product_id="prod_test",
            stripe_price_id="price_test",
        )
        self.client.force_authenticate(user=self.user)

    def test_list_plans(self):
        """Test listing available plans."""
        response = self.client.get("/api/billing/plans/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_plan_detail(self):
        """Test plan detail view."""
        response = self.client.get(f"/api/billing/plans/{self.plan.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["code"], "pro")
        self.assertEqual(response.data["price_monthly_cents"], 9900)

    @patch("billing.services.stripe_api.stripe.checkout.Session.create")
    def test_subscription_checkout(self, mock_stripe):
        """Test subscription checkout session creation."""
        mock_stripe.return_value = MagicMock(id="cs_test", url="https://checkout.stripe.com/test")

        response = self.client.post(
            "/api/billing/subscriptions/",
            {"plan": self.plan.id},
            format="json",
        )
        # Should return checkout URL
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])
