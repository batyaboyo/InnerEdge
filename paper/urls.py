"""URL configuration for paper trading API."""

from __future__ import annotations

from rest_framework.routers import DefaultRouter

from paper.views import PaperAccountViewSet, PaperPositionViewSet

router = DefaultRouter()
router.register("accounts", PaperAccountViewSet, basename="paper-account")
router.register("positions", PaperPositionViewSet, basename="paper-position")

urlpatterns = router.urls
