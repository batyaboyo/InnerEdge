"""Liquidity and structure detection services."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable

from django.db import transaction

from market.models import (
    Asset,
    Candle,
    DailyBias,
    FairValueGap,
    LiquidityZone,
    OrderBlock,
    SweepEvent,
)


@dataclass
class LiquidityDetectionConfig:
    """Configuration used by liquidity and sweep detection."""

    tolerance_points: Decimal = Decimal("0.00020")
    min_touches: int = 2


def _candles_to_levels(candles: Iterable[Candle], use_high: bool) -> list[tuple[Decimal, Candle]]:
    return [((c.high if use_high else c.low), c) for c in candles]


@transaction.atomic
def detect_liquidity_zones(asset: Asset, timeframe: str, config: LiquidityDetectionConfig | None = None) -> int:
    """Detect equal-high and equal-low liquidity pools from recent candles."""
    cfg = config or LiquidityDetectionConfig()
    candles = list(Candle.objects.filter(asset=asset, timeframe=timeframe).order_by("open_time")[:5000])
    if len(candles) < 3:
        return 0

    created = 0
    for side, use_high in ((LiquidityZone.Side.BUY_SIDE, True), (LiquidityZone.Side.SELL_SIDE, False)):
        levels = _candles_to_levels(candles, use_high)
        for idx, (level, source) in enumerate(levels[:-1]):
            touches = [source]
            for other_level, other_candle in levels[idx + 1 :]:
                if abs(other_level - level) <= cfg.tolerance_points:
                    touches.append(other_candle)
            if len(touches) >= cfg.min_touches:
                first_seen = min(t.open_time for t in touches)
                last_seen = max(t.open_time for t in touches)
                strength = Decimal(len(touches)) * Decimal("10")
                _, created_flag = LiquidityZone.objects.update_or_create(
                    asset=asset,
                    timeframe=timeframe,
                    side=side,
                    level_price=level,
                    defaults={
                        "touch_count": len(touches),
                        "tolerance_points": cfg.tolerance_points,
                        "strength_score": strength,
                        "first_seen_at": first_seen,
                        "last_seen_at": last_seen,
                        "is_active": True,
                    },
                )
                if created_flag:
                    created += 1
    return created


@transaction.atomic
def detect_liquidity_sweeps(asset: Asset, timeframe: str) -> int:
    """Identify sweep events where price takes liquidity then reverses."""
    candles = list(Candle.objects.filter(asset=asset, timeframe=timeframe).order_by("open_time")[:5000])
    zones = list(LiquidityZone.objects.filter(asset=asset, timeframe=timeframe, is_active=True))
    if len(candles) < 2 or not zones:
        return 0

    created = 0
    for zone in zones:
        for i in range(1, len(candles)):
            prev_candle = candles[i - 1]
            candle = candles[i]
            swept = False
            direction = SweepEvent.Direction.BEARISH
            if zone.side == LiquidityZone.Side.BUY_SIDE:
                if candle.high > zone.level_price and candle.close < zone.level_price:
                    swept = True
                    direction = SweepEvent.Direction.BEARISH
            else:
                if candle.low < zone.level_price and candle.close > zone.level_price:
                    swept = True
                    direction = SweepEvent.Direction.BULLISH

            if swept:
                _, created_flag = SweepEvent.objects.get_or_create(
                    asset=asset,
                    timeframe=timeframe,
                    liquidity_zone=zone,
                    swept_at=candle.open_time,
                    swept_price=zone.level_price,
                    direction=direction,
                    defaults={
                        "entry_zone_low": min(prev_candle.low, candle.low),
                        "entry_zone_high": max(prev_candle.high, candle.high),
                        "context": {
                            "philosophy": "liquidity_to_liquidity",
                            "note": "institutional stop-hunt signature",
                        },
                    },
                )
                if created_flag:
                    created += 1
    return created


@transaction.atomic
def compute_daily_bias(asset: Asset) -> DailyBias | None:
    """Compute daily directional bias from previous-day structure and swings."""
    candles = list(Candle.objects.filter(asset=asset, timeframe=Candle.Timeframe.D1).order_by("-open_time")[:3])
    if len(candles) < 3:
        return None

    current, prev, prev2 = candles[0], candles[1], candles[2]
    bullish_structure = prev.high > prev2.high and prev.low > prev2.low
    bearish_structure = prev.high < prev2.high and prev.low < prev2.low

    if bullish_structure and current.close >= prev.high:
        bias = DailyBias.Bias.BULLISH
    elif bearish_structure and current.close <= prev.low:
        bias = DailyBias.Bias.BEARISH
    else:
        bias = DailyBias.Bias.NEUTRAL

    daily_bias, _ = DailyBias.objects.update_or_create(
        asset=asset,
        session_date=current.open_time.date(),
        timeframe=Candle.Timeframe.D1,
        defaults={
            "bias": bias,
            "structure_context": {
                "prev_high": str(prev.high),
                "prev_low": str(prev.low),
                "prev2_high": str(prev2.high),
                "prev2_low": str(prev2.low),
                "model": "market-structure-with-pdh-pdl",
            },
            "previous_day_high": prev.high,
            "previous_day_low": prev.low,
        },
    )
    return daily_bias


@transaction.atomic
def detect_fair_value_gaps(asset: Asset, timeframe: str) -> int:
    """Detect three-candle fair value gaps as secondary context."""
    candles = list(Candle.objects.filter(asset=asset, timeframe=timeframe).order_by("open_time")[:5000])
    if len(candles) < 3:
        return 0

    created = 0
    for left, mid, right in zip(candles, candles[1:], candles[2:]):
        if right.low > left.high:
            _, created_flag = FairValueGap.objects.get_or_create(
                asset=asset,
                timeframe=timeframe,
                gap_type=FairValueGap.GapType.BULLISH,
                zone_low=left.high,
                zone_high=right.low,
                anchor_time=mid.open_time,
                defaults={"strength_score": Decimal("55")},
            )
            if created_flag:
                created += 1
        elif right.high < left.low:
            _, created_flag = FairValueGap.objects.get_or_create(
                asset=asset,
                timeframe=timeframe,
                gap_type=FairValueGap.GapType.BEARISH,
                zone_low=right.high,
                zone_high=left.low,
                anchor_time=mid.open_time,
                defaults={"strength_score": Decimal("55")},
            )
            if created_flag:
                created += 1
    return created


@transaction.atomic
def detect_order_blocks(asset: Asset, timeframe: str) -> int:
    """Detect simple order block candidates from displacement patterns."""
    candles = list(Candle.objects.filter(asset=asset, timeframe=timeframe).order_by("open_time")[:5000])
    if len(candles) < 3:
        return 0

    created = 0
    for prev_candle, candle in zip(candles, candles[1:]):
        body = abs(candle.close - candle.open)
        range_size = candle.high - candle.low
        if range_size <= 0:
            continue
        displacement = (body / range_size) > Decimal("0.65")
        if not displacement:
            continue

        if candle.close > candle.open and prev_candle.close < prev_candle.open:
            block_type = OrderBlock.BlockType.BULLISH
        elif candle.close < candle.open and prev_candle.close > prev_candle.open:
            block_type = OrderBlock.BlockType.BEARISH
        else:
            continue

        _, created_flag = OrderBlock.objects.get_or_create(
            asset=asset,
            timeframe=timeframe,
            block_type=block_type,
            zone_low=prev_candle.low,
            zone_high=prev_candle.high,
            origin_time=prev_candle.open_time,
            defaults={"strength_score": Decimal("60")},
        )
        if created_flag:
            created += 1

    return created
