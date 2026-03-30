"""Tests for paper trading simulation."""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from paper.models import PaperAccount, PaperPosition
from paper.services.simulator import recalculate_account_metrics
from market.models import Asset

User = get_user_model()


class PaperTradingSimulatorTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="trader", email="trader@test.com", password="pass123")
        self.asset = Asset.objects.create(
            symbol="EURUSD",
            name="Euro/USD",
            market_type=Asset.MarketType.FOREX,
            broker="test",
        )
        self.account = PaperAccount.objects.create(user=self.user, name="Demo Account", balance=Decimal("10000"))

    def test_margin_level_calculation(self):
        """Test margin level percentage calculation."""
        position = PaperPosition.objects.create(
            account=self.account,
            asset=self.asset,
            direction=PaperPosition.Direction.LONG,
            status=PaperPosition.Status.OPEN,
            entry_price=Decimal("1.0500"),
            current_price=Decimal("1.0550"),
            size_lots=Decimal("1.0"),
            leverage=Decimal("10.00"),
            unrealized_pnl=Decimal("50"),
        )

        recalculate_account_metrics(self.account)
        self.assertGreater(self.account.margin_level_percent, 0)
        self.assertGreater(self.account.used_margin, 0)
        self.assertEqual(self.account.equity, self.account.balance + position.unrealized_pnl)

    def test_free_margin_calculation(self):
        """Test free margin calculation."""
        position = PaperPosition.objects.create(
            account=self.account,
            asset=self.asset,
            direction=PaperPosition.Direction.LONG,
            status=PaperPosition.Status.OPEN,
            entry_price=Decimal("1.0500"),
            current_price=Decimal("1.0550"),
            size_lots=Decimal("5.0"),
            leverage=Decimal("20.00"),
            unrealized_pnl=Decimal("0"),
        )

        recalculate_account_metrics(self.account)
        self.assertEqual(self.account.free_margin, self.account.equity - self.account.used_margin)
