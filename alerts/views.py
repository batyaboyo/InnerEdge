"""REST API views for alerts."""

from __future__ import annotations

from rest_framework import decorators, permissions, response, viewsets

from alerts.models import AlertEvent, AlertRule
from alerts.serializers import AlertEventSerializer, AlertRuleSerializer


class AlertRuleViewSet(viewsets.ModelViewSet):
	serializer_class = AlertRuleSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return AlertRule.objects.filter(user=self.request.user)

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)


class AlertEventViewSet(viewsets.ReadOnlyModelViewSet):
	serializer_class = AlertEventSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return AlertEvent.objects.filter(user=self.request.user).order_by("-created_at")

	@decorators.action(detail=True, methods=["post"], url_path="mark-read")
	def mark_read(self, request, pk=None):
		event = self.get_object()
		event.is_read = True
		event.save(update_fields=["is_read"])
		return response.Response(self.get_serializer(event).data)
