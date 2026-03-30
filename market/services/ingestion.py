"""Market data ingestion service that stores broker candles."""

from __future__ import annotations

from django.db import transaction

from market.models import Asset, Candle
from market.services.brokers import BinanceAdapter, BrokerAdapter, IGAdapter, OANDAAdapter


def _select_adapter(broker: str) -> BrokerAdapter:
    mapping: dict[str, type[BrokerAdapter]] = {
        "ig": IGAdapter,
        "oanda": OANDAAdapter,
        "binance": BinanceAdapter,
    }
    adapter_cls = mapping.get(broker.lower(), BinanceAdapter)
    return adapter_cls()


@transaction.atomic
def ingest_candles(asset: Asset, timeframe: str, limit: int = 500) -> int:
    """Fetch candles from configured broker and upsert in database."""
    adapter = _select_adapter(asset.broker)
    candles = adapter.fetch_candles(symbol=asset.symbol, timeframe=timeframe, limit=limit)
    ingested = 0

    for candle in candles:
        _, created = Candle.objects.update_or_create(
            asset=asset,
            timeframe=timeframe,
            open_time=candle.open_time,
            defaults={
                "open": candle.open,
                "high": candle.high,
                "low": candle.low,
                "close": candle.close,
                "volume": candle.volume,
                "spread_points": candle.spread_points,
            },
        )
        if created:
            ingested += 1
    return ingested
