"""Tests for behavioral intelligence engine."""

from decimal import Decimal
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from journal.models import Trade
from market.models import Asset
from intel.services.behavioral import generate_behavior_insights
from intel.models import BehaviorInsight

User = get_user_model()


class BehavioralInsightTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="trader", email="trader@test.com", password="pass123")
        self.asset = Asset.objects.create(
            symbol="EURUSD",
            name="Euro/USD",
            market_type=Asset.MarketType.FOREX,
            broker="test",
        )

    def test_over_leverage_detection(self):
        """Test detection of over-leverage behavior."""
        for i in range(5):
            Trade.objects.create(
                user=self.user,
                asset=self.asset,
                direction=Trade.Direction.LONG,
                status=Trade.Status.CLOSED,
                entry_price=Decimal("1.0500"),
                exit_price=Decimal("1.0600"),
                stop_loss=Decimal("1.0450"),
                take_profit=Decimal("1.0650"),
                position_size_lots=Decimal("1.0"),
                leverage=Decimal("50.00"),
                margin_used=Decimal("100"),
                risk_percent=Decimal("5.00"),
                opened_at=timezone.now(),
                closed_at=timezone.now(),
                account_currency="USD",
                base_currency="USD",
                pnl_account_currency=Decimal("100"),
            )

        insights = generate_behavior_insights(self.user)
        insight_titles = [i.title for i in insights]
        self.assertIn("Over-leverage pattern detected", insight_titles)

    def test_swap_cost_detection(self):
        """Test detection of swap cost impact."""
        Trade.objects.create(
            user=self.user,
            asset=self.asset,
            direction=Trade.Direction.SHORT,
            status=Trade.Status.CLOSED,
            entry_price=Decimal("1.0500"),
            exit_price=Decimal("1.0400"),
            stop_loss=Decimal("1.0550"),
            take_profit=Decimal("1.0350"),
            position_size_lots=Decimal("10.0"),
            leverage=Decimal("10.00"),
            margin_used=Decimal("500"),
            swap_fee=Decimal("-100.00"),
            risk_percent=Decimal("2.00"),
            opened_at=timezone.now(),
            closed_at=timezone.now(),
            account_currency="USD",
            base_currency="USD",
            pnl_account_currency=Decimal("-50"),
        )

        insights = generate_behavior_insights(self.user)
        insight_titles = [i.title for i in insights]
        self.assertIn("Swap costs are materially reducing returns", insight_titles)
