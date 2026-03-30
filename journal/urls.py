"""URL configuration for journal API."""

from __future__ import annotations

from rest_framework.routers import DefaultRouter

from journal.views import SetupTagViewSet, TradeAnalyticsSnapshotViewSet, TradeNoteViewSet, TradeViewSet

router = DefaultRouter()
router.register("tags", SetupTagViewSet, basename="setup-tag")
router.register("trades", TradeViewSet, basename="trade")
router.register("notes", TradeNoteViewSet, basename="trade-note")
router.register("analytics-snapshots", TradeAnalyticsSnapshotViewSet, basename="trade-analytics")

urlpatterns = router.urls
