"""URL configuration for intelligence API."""

from __future__ import annotations

from rest_framework.routers import DefaultRouter

from intel.views import BehaviorInsightViewSet, BehaviorMetricDailyViewSet

router = DefaultRouter()
router.register("metrics", BehaviorMetricDailyViewSet, basename="behavior-metric")
router.register("insights", BehaviorInsightViewSet, basename="behavior-insight")

urlpatterns = router.urls
