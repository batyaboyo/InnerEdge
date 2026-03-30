"""Asynchronous market ingestion and analysis tasks."""

from __future__ import annotations

from celery import shared_task

from market.models import Asset
from market.services.ingestion import ingest_candles
from market.services.liquidity import (
    compute_daily_bias,
    detect_fair_value_gaps,
    detect_liquidity_sweeps,
    detect_liquidity_zones,
    detect_order_blocks,
)


@shared_task
def run_liquidity_pipeline(asset_id: int, timeframe: str = "H1") -> dict[str, int | str]:
    """Run full liquidity pipeline for an asset and timeframe."""
    asset = Asset.objects.get(id=asset_id)
    zones = detect_liquidity_zones(asset=asset, timeframe=timeframe)
    sweeps = detect_liquidity_sweeps(asset=asset, timeframe=timeframe)
    fvg_count = detect_fair_value_gaps(asset=asset, timeframe=timeframe)
    ob_count = detect_order_blocks(asset=asset, timeframe=timeframe)
    compute_daily_bias(asset=asset)
    return {
        "asset": asset.symbol,
        "zones_created": zones,
        "sweeps_created": sweeps,
        "fvg_created": fvg_count,
        "order_blocks_created": ob_count,
    }


@shared_task
def ingest_asset_candles(asset_id: int, timeframe: str = "H1", limit: int = 500) -> dict[str, int | str]:
    """Ingest candles from the configured broker adapter for one asset."""
    asset = Asset.objects.get(id=asset_id)
    inserted = ingest_candles(asset=asset, timeframe=timeframe, limit=limit)
    return {"asset": asset.symbol, "candles_ingested": inserted}
