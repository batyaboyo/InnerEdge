"""Broker adapters for OHLCV ingestion (CFD oriented)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class NormalizedCandle:
    open_time: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal
    spread_points: Decimal


class BrokerAdapter:
    """Interface for broker-specific market data clients."""

    def fetch_candles(self, symbol: str, timeframe: str, limit: int = 500) -> list[NormalizedCandle]:
        raise NotImplementedError


class IGAdapter(BrokerAdapter):
    def fetch_candles(self, symbol: str, timeframe: str, limit: int = 500) -> list[NormalizedCandle]:
        return []


class OANDAAdapter(BrokerAdapter):
    def fetch_candles(self, symbol: str, timeframe: str, limit: int = 500) -> list[NormalizedCandle]:
        return []


class BinanceAdapter(BrokerAdapter):
    def fetch_candles(self, symbol: str, timeframe: str, limit: int = 500) -> list[NormalizedCandle]:
        return []
