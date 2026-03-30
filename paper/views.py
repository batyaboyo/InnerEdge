"""REST API views for paper trading."""

from __future__ import annotations

from rest_framework import decorators, permissions, response, viewsets

from paper.models import PaperAccount, PaperPosition
from paper.serializers import PaperAccountSerializer, PaperPositionSerializer
from paper.services.simulator import recalculate_account_metrics


class PaperAccountViewSet(viewsets.ModelViewSet):
	serializer_class = PaperAccountSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return PaperAccount.objects.filter(user=self.request.user)

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

	@decorators.action(detail=True, methods=["post"], url_path="recalculate")
	def recalculate(self, request, pk=None):
		account = self.get_object()
		account = recalculate_account_metrics(account)
		return response.Response(PaperAccountSerializer(account).data)


class PaperPositionViewSet(viewsets.ModelViewSet):
	serializer_class = PaperPositionSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return PaperPosition.objects.filter(account__user=self.request.user).select_related("account", "asset")
