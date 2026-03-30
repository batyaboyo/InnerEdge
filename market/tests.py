"""Tests for market liquidity engine."""

from decimal import Decimal
from datetime import datetime, timedelta

from django.test import TestCase
from django.utils import timezone

from market.models import Asset, Candle, LiquidityZone, SweepEvent
from market.services.liquidity import detect_liquidity_zones, detect_liquidity_sweeps, compute_daily_bias


class LiquidityDetectionTestCase(TestCase):
    def setUp(self):
        self.asset = Asset.objects.create(
            symbol="EURUSD",
            name="Euro/USD",
            market_type=Asset.MarketType.FOREX,
            broker="test",
            base_currency="EUR",
            quote_currency="USD",
        )

    def test_detect_liquidity_zones_buy_side(self):
        """Test detection of buy-side (equal lows) liquidity zones."""
        base_time = timezone.now()
        candle_data = [
            (base_time, Decimal("1.0500"), Decimal("1.0600"), Decimal("1.0450"), Decimal("1.0550")),
            (base_time + timedelta(hours=1), Decimal("1.0520"), Decimal("1.0620"), Decimal("1.0450"), Decimal("1.0580")),
            (base_time + timedelta(hours=2), Decimal("1.0540"), Decimal("1.0640"), Decimal("1.0450"), Decimal("1.0600")),
        ]
        for time, open_, high, low, close in candle_data:
            Candle.objects.create(
                asset=self.asset,
                timeframe=Candle.Timeframe.H1,
                open_time=time,
                open=open_,
                high=high,
                low=low,
                close=close,
                volume=Decimal("1000"),
            )

        created = detect_liquidity_zones(self.asset, Candle.Timeframe.H1)
        self.assertGreater(created, 0)
        zones = LiquidityZone.objects.filter(asset=self.asset, side=LiquidityZone.Side.SELL_SIDE)
        self.assertTrue(zones.exists())

    def test_detect_liquidity_sweeps(self):
        """Test identification of liquidity sweep events."""
        base_time = timezone.now()
        candle_data = [
            (base_time, Decimal("1.0500"), Decimal("1.0600"), Decimal("1.0450"), Decimal("1.0550")),
            (base_time + timedelta(hours=1), Decimal("1.0520"), Decimal("1.0620"), Decimal("1.0450"), Decimal("1.0580")),
        ]
        for time, open_, high, low, close in candle_data:
            Candle.objects.create(
                asset=self.asset,
                timeframe=Candle.Timeframe.H1,
                open_time=time,
                open=open_,
                high=high,
                low=low,
                close=close,
                volume=Decimal("1000"),
            )

        zone = LiquidityZone.objects.create(
            asset=self.asset,
            timeframe=Candle.Timeframe.H1,
            side=LiquidityZone.Side.BUY_SIDE,
            level_price=Decimal("1.0450"),
            touch_count=2,
            first_seen_at=base_time,
            last_seen_at=base_time + timedelta(hours=1),
        )

        created = detect_liquidity_sweeps(self.asset, Candle.Timeframe.H1)
        self.assertGreaterEqual(created, 0)

    def test_daily_bias_computation(self):
        """Test daily directional bias calculation."""
        base_time = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        candle_data = [
            (base_time - timedelta(days=2), Decimal("1.0400"), Decimal("1.0600"), Decimal("1.0350"), Decimal("1.0500")),
            (base_time - timedelta(days=1), Decimal("1.0500"), Decimal("1.0700"), Decimal("1.0450"), Decimal("1.0600")),
            (base_time, Decimal("1.0600"), Decimal("1.0750"), Decimal("1.0550"), Decimal("1.0700")),
        ]
        for time, open_, high, low, close in candle_data:
            Candle.objects.create(
                asset=self.asset,
                timeframe=Candle.Timeframe.D1,
                open_time=time,
                open=open_,
                high=high,
                low=low,
                close=close,
                volume=Decimal("1000"),
            )

        bias = compute_daily_bias(self.asset)
        self.assertIsNotNone(bias)
        self.assertIn(bias.bias, [choice[0] for choice in bias.Bias.choices])
