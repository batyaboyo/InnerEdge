"""Tests for trading journal analytics."""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from journal.models import Trade
from market.models import Asset

User = get_user_model()


class TradeAnalyticsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="trader", email="trader@test.com", password="pass123")
        self.asset = Asset.objects.create(
            symbol="EURUSD",
            name="Euro/USD",
            market_type=Asset.MarketType.FOREX,
            broker="test",
        )

    def test_win_rate_calculation(self):
        """Test win rate calculation from closed trades."""
        trades = [
            (True, Decimal("100")),  # win
            (True, Decimal("150")),  # win
            (False, Decimal("-50")),  # loss
            (False, Decimal("-30")),  # loss
            (True, Decimal("75")),  # win
        ]

        for is_win, pnl in trades:
            Trade.objects.create(
                user=self.user,
                asset=self.asset,
                direction=Trade.Direction.LONG,
                status=Trade.Status.CLOSED,
                entry_price=Decimal("1.0500"),
                exit_price=Decimal("1.0600") if is_win else Decimal("1.0400"),
                stop_loss=Decimal("1.0450"),
                take_profit=Decimal("1.0650"),
                position_size_lots=Decimal("1.0"),
                leverage=Decimal("10.00"),
                margin_used=Decimal("100"),
                risk_percent=Decimal("1.00"),
                opened_at=timezone.now(),
                closed_at=timezone.now(),
                account_currency="USD",
                base_currency="USD",
                pnl_account_currency=pnl,
            )

        closed_trades = Trade.objects.filter(user=self.user, status=Trade.Status.CLOSED)
        total = closed_trades.count()
        wins = closed_trades.filter(pnl_account_currency__gt=0).count()
        win_rate = (wins / total * 100) if total else 0

        self.assertEqual(total, 5)
        self.assertEqual(wins, 3)
        self.assertEqual(win_rate, 60.0)
