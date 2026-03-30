"""URL configuration for accounts API."""

from __future__ import annotations

from rest_framework.routers import DefaultRouter

from accounts.views import TraderProfileViewSet

router = DefaultRouter()
router.register("profiles", TraderProfileViewSet, basename="trader-profile")

urlpatterns = router.urls
