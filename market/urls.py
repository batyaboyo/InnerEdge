"""URL configuration for market API."""

from __future__ import annotations

from rest_framework.routers import DefaultRouter

from market.views import (
    AssetViewSet,
    CandleViewSet,
    CFDConditionViewSet,
    DailyBiasViewSet,
    FairValueGapViewSet,
    LiquidityZoneViewSet,
    OrderBlockViewSet,
    SweepEventViewSet,
)

router = DefaultRouter()
router.register("assets", AssetViewSet, basename="asset")
router.register("conditions", CFDConditionViewSet, basename="cfd-condition")
router.register("candles", CandleViewSet, basename="candle")
router.register("liquidity-zones", LiquidityZoneViewSet, basename="liquidity-zone")
router.register("sweep-events", SweepEventViewSet, basename="sweep-event")
router.register("daily-bias", DailyBiasViewSet, basename="daily-bias")
router.register("fvg", FairValueGapViewSet, basename="fair-value-gap")
router.register("order-blocks", OrderBlockViewSet, basename="order-block")

urlpatterns = router.urls
