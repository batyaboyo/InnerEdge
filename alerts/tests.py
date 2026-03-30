"""Tests for alerts module."""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

from alerts.models import AlertRule, AlertEvent
from market.models import Asset

User = get_user_model()


class AlertRuleModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="trader", email="trader@test.com", password="pass123")
        self.asset = Asset.objects.create(
            symbol="EURUSD",
            name="Euro/USD",
            market_type=Asset.MarketType.FOREX,
            broker="test",
        )

    def test_alert_rule_creation(self):
        """Test alert rule creation."""
        rule = AlertRule.objects.create(
            user=self.user,
            asset=self.asset,
            rule_type=AlertRule.RuleType.LIQUIDITY_SWEEP,
            threshold_value=Decimal("1.0500"),
            config={"direction": "above"},
        )
        self.assertEqual(rule.user, self.user)
        self.assertEqual(rule.asset, self.asset)
        self.assertEqual(rule.threshold_value, Decimal("1.0500"))

    def test_alert_rule_query(self):
        """Test retrieving alert rules by user."""
        rule1 = AlertRule.objects.create(
            user=self.user,
            asset=self.asset,
            rule_type=AlertRule.RuleType.LIQUIDITY_SWEEP,
            threshold_value=Decimal("1.0500"),
            config={},
        )
        rule2 = AlertRule.objects.create(
            user=self.user,
            asset=self.asset,
            rule_type=AlertRule.RuleType.SWAP_IMPACT,
            threshold_value=Decimal("0.50"),
            config={},
        )

        user_rules = AlertRule.objects.filter(user=self.user)
        self.assertEqual(user_rules.count(), 2)


class AlertEventModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="trader", email="trader@test.com", password="pass123")
        self.asset = Asset.objects.create(
            symbol="EURUSD",
            name="Euro/USD",
            market_type=Asset.MarketType.FOREX,
            broker="test",
        )
        self.rule = AlertRule.objects.create(
            user=self.user,
            asset=self.asset,
            rule_type=AlertRule.RuleType.LIQUIDITY_SWEEP,
            threshold_value=Decimal("1.0500"),
            config={},
        )

    def test_alert_event_creation(self):
        """Test alert event creation."""
        event = AlertEvent.objects.create(
            user=self.user,
            rule=self.rule,
            asset=self.asset,
            level=AlertEvent.Level.INFO,
            title="Price Target Reached",
            message="EURUSD reached 1.0500",
            payload={"price": "1.0500"},
        )
        self.assertEqual(event.user, self.user)
        self.assertFalse(event.is_read)


class AlertAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="trader", email="trader@test.com", password="pass123")
        self.asset = Asset.objects.create(
            symbol="EURUSD",
            name="Euro/USD",
            market_type=Asset.MarketType.FOREX,
            broker="test",
        )
        self.client.force_authenticate(user=self.user)

    def test_create_alert_rule(self):
        """Test creating an alert rule."""
        response = self.client.post(
            "/api/alerts/rules/",
            {
                "asset": self.asset.id,
                "rule_type": "liquidity_sweep",
                "threshold_value": "1.0500",
                "config": {"direction": "above"},
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["threshold_value"], "1.05000")

    def test_list_alert_rules(self):
        """Test listing user's alert rules."""
        AlertRule.objects.create(
            user=self.user,
            asset=self.asset,
            rule_type=AlertRule.RuleType.LIQUIDITY_SWEEP,
            threshold_value=Decimal("1.0500"),
            config={},
        )

        response = self.client.get("/api/alerts/rules/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_alert_events(self):
        """Test listing alert events."""
        response = self.client.get("/api/alerts/events/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
