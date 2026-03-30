"""URL configuration for alerts API."""

from __future__ import annotations

from rest_framework.routers import DefaultRouter

from alerts.views import AlertEventViewSet, AlertRuleViewSet

router = DefaultRouter()
router.register("rules", AlertRuleViewSet, basename="alert-rule")
router.register("events", AlertEventViewSet, basename="alert-event")

urlpatterns = router.urls
