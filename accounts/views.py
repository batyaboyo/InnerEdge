"""REST API views for account domain."""

from __future__ import annotations

from rest_framework import mixins, permissions, viewsets

from accounts.models import TraderProfile
from accounts.serializers import TraderProfileSerializer


class TraderProfileViewSet(
	mixins.ListModelMixin,
	mixins.RetrieveModelMixin,
	mixins.UpdateModelMixin,
	viewsets.GenericViewSet,
):
	"""Expose logged-in user trader profile endpoints."""

	serializer_class = TraderProfileSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return TraderProfile.objects.filter(user=self.request.user)
