"""Market data and Smart Money Concepts domain models."""

from __future__ import annotations

from django.db import models


class Asset(models.Model):
    """Tradeable CFD instrument metadata."""

    class MarketType(models.TextChoices):
        FOREX = "forex", "Forex"
        INDEX = "index", "Index"
        COMMODITY = "commodity", "Commodity"
        STOCK = "stock", "Stock"
        CRYPTO = "crypto", "Crypto"

    symbol = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=128)
    market_type = models.CharField(max_length=16, choices=MarketType.choices)
    broker = models.CharField(max_length=64)
    base_currency = models.CharField(max_length=8, default="USD")
    quote_currency = models.CharField(max_length=8, default="USD")
    default_leverage = models.DecimalField(max_digits=8, decimal_places=2, default=20.00)
    max_leverage = models.DecimalField(max_digits=8, decimal_places=2, default=200.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.symbol


class CFDCondition(models.Model):
    """CFD cost and margin conditions that can change over time."""

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="conditions")
    spread_points = models.DecimalField(max_digits=12, decimal_places=5)
    overnight_swap_long = models.DecimalField(max_digits=12, decimal_places=5)
    overnight_swap_short = models.DecimalField(max_digits=12, decimal_places=5)
    margin_requirement_percent = models.DecimalField(max_digits=6, decimal_places=3)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField(null=True, blank=True)


class Candle(models.Model):
    """OHLCV bar with CFD spread metadata."""

    class Timeframe(models.TextChoices):
        M1 = "M1", "M1"
        M5 = "M5", "M5"
        M15 = "M15", "M15"
        H1 = "H1", "H1"
        H4 = "H4", "H4"
        D1 = "D1", "D1"

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="candles")
    timeframe = models.CharField(max_length=3, choices=Timeframe.choices)
    open_time = models.DateTimeField()
    open = models.DecimalField(max_digits=18, decimal_places=8)
    high = models.DecimalField(max_digits=18, decimal_places=8)
    low = models.DecimalField(max_digits=18, decimal_places=8)
    close = models.DecimalField(max_digits=18, decimal_places=8)
    volume = models.DecimalField(max_digits=22, decimal_places=8, default=0)
    spread_points = models.DecimalField(max_digits=12, decimal_places=5, default=0)
    bid_close = models.DecimalField(max_digits=18, decimal_places=8, null=True, blank=True)
    ask_close = models.DecimalField(max_digits=18, decimal_places=8, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["asset", "timeframe", "open_time"],
                name="uniq_candle_asset_tf_time",
            )
        ]
        indexes = [models.Index(fields=["asset", "timeframe", "open_time"])]


class LiquidityZone(models.Model):
    """Liquidity pool formed by equal highs or equal lows."""

    class Side(models.TextChoices):
        BUY_SIDE = "buy_side", "Buy-side"
        SELL_SIDE = "sell_side", "Sell-side"

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="liquidity_zones")
    timeframe = models.CharField(max_length=3, choices=Candle.Timeframe.choices)
    side = models.CharField(max_length=16, choices=Side.choices)
    level_price = models.DecimalField(max_digits=18, decimal_places=8)
    tolerance_points = models.DecimalField(max_digits=12, decimal_places=5, default=0)
    touch_count = models.PositiveIntegerField(default=2)
    strength_score = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    first_seen_at = models.DateTimeField()
    last_seen_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)


class SweepEvent(models.Model):
    """Liquidity sweep event where stops are likely harvested."""

    class Direction(models.TextChoices):
        BULLISH = "bullish", "Bullish"
        BEARISH = "bearish", "Bearish"

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="sweep_events")
    timeframe = models.CharField(max_length=3, choices=Candle.Timeframe.choices)
    liquidity_zone = models.ForeignKey(
        LiquidityZone,
        on_delete=models.SET_NULL,
        related_name="sweeps",
        null=True,
        blank=True,
    )
    direction = models.CharField(max_length=8, choices=Direction.choices)
    swept_at = models.DateTimeField()
    swept_price = models.DecimalField(max_digits=18, decimal_places=8)
    entry_zone_low = models.DecimalField(max_digits=18, decimal_places=8)
    entry_zone_high = models.DecimalField(max_digits=18, decimal_places=8)
    context = models.JSONField(default=dict, blank=True)


class DailyBias(models.Model):
    """Higher-timeframe directional context for execution day."""

    class Bias(models.TextChoices):
        BULLISH = "bullish", "Bullish"
        BEARISH = "bearish", "Bearish"
        NEUTRAL = "neutral", "Neutral"

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="daily_biases")
    session_date = models.DateField()
    timeframe = models.CharField(max_length=3, choices=Candle.Timeframe.choices, default=Candle.Timeframe.D1)
    bias = models.CharField(max_length=8, choices=Bias.choices)
    structure_context = models.JSONField(default=dict, blank=True)
    previous_day_high = models.DecimalField(max_digits=18, decimal_places=8)
    previous_day_low = models.DecimalField(max_digits=18, decimal_places=8)
    calculated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["asset", "session_date", "timeframe"],
                name="uniq_daily_bias_asset_day_tf",
            )
        ]


class FairValueGap(models.Model):
    """Three-candle imbalance zone used as a secondary confluence signal."""

    class GapType(models.TextChoices):
        BULLISH = "bullish", "Bullish"
        BEARISH = "bearish", "Bearish"

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="fvg_zones")
    timeframe = models.CharField(max_length=3, choices=Candle.Timeframe.choices)
    gap_type = models.CharField(max_length=8, choices=GapType.choices)
    zone_low = models.DecimalField(max_digits=18, decimal_places=8)
    zone_high = models.DecimalField(max_digits=18, decimal_places=8)
    anchor_time = models.DateTimeField()
    strength_score = models.DecimalField(max_digits=6, decimal_places=2, default=0)


class OrderBlock(models.Model):
    """Last opposite candle before displacement, secondary to liquidity narrative."""

    class BlockType(models.TextChoices):
        BULLISH = "bullish", "Bullish"
        BEARISH = "bearish", "Bearish"

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="order_blocks")
    timeframe = models.CharField(max_length=3, choices=Candle.Timeframe.choices)
    block_type = models.CharField(max_length=8, choices=BlockType.choices)
    zone_low = models.DecimalField(max_digits=18, decimal_places=8)
    zone_high = models.DecimalField(max_digits=18, decimal_places=8)
    origin_time = models.DateTimeField()
    strength_score = models.DecimalField(max_digits=6, decimal_places=2, default=0)
