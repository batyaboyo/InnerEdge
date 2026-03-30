"""REST API views for behavioral intelligence."""

from __future__ import annotations

from rest_framework import decorators, permissions, response, viewsets

from intel.models import BehaviorInsight, BehaviorMetricDaily
from intel.serializers import BehaviorInsightSerializer, BehaviorMetricDailySerializer
from intel.services.behavioral import generate_behavior_insights


class BehaviorMetricDailyViewSet(viewsets.ModelViewSet):
	serializer_class = BehaviorMetricDailySerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return BehaviorMetricDaily.objects.filter(user=self.request.user)

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)


class BehaviorInsightViewSet(viewsets.ReadOnlyModelViewSet):
	serializer_class = BehaviorInsightSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return BehaviorInsight.objects.filter(user=self.request.user).order_by("-created_at")

	@decorators.action(detail=False, methods=["post"], url_path="generate")
	def generate(self, request):
		generated = generate_behavior_insights(user=request.user)
		serializer = self.get_serializer(generated, many=True)
		return response.Response(serializer.data)
