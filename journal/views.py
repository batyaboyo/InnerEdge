"""REST API views for journaling and analytics."""

from __future__ import annotations

from django.db.models import Avg, Count, Sum
from rest_framework import decorators, permissions, response, viewsets

from journal.models import SetupTag, Trade, TradeAnalyticsSnapshot, TradeNote
from journal.serializers import (
	SetupTagSerializer,
	TradeAnalyticsSnapshotSerializer,
	TradeNoteSerializer,
	TradeSerializer,
)


class SetupTagViewSet(viewsets.ModelViewSet):
	queryset = SetupTag.objects.all()
	serializer_class = SetupTagSerializer
	permission_classes = [permissions.IsAuthenticated]


class TradeViewSet(viewsets.ModelViewSet):
	serializer_class = TradeSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return Trade.objects.filter(user=self.request.user).select_related("asset").prefetch_related("tags", "notes")

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

	@decorators.action(detail=False, methods=["get"], url_path="analytics")
	def analytics(self, request):
		queryset = self.get_queryset().filter(status=Trade.Status.CLOSED)
		total = queryset.count()
		wins = queryset.filter(pnl_account_currency__gt=0).count()
		stats = queryset.aggregate(
			total_pnl=Sum("pnl_account_currency"),
			avg_risk=Avg("risk_percent"),
			long_count=Count("id"),
		)
		return response.Response(
			{
				"total_trades": total,
				"win_rate": round((wins / total * 100), 2) if total else 0,
				"total_pnl": stats["total_pnl"] or 0,
				"avg_risk_percent": stats["avg_risk"] or 0,
			}
		)


class TradeNoteViewSet(viewsets.ModelViewSet):
	serializer_class = TradeNoteSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return TradeNote.objects.filter(trade__user=self.request.user).select_related("trade")


class TradeAnalyticsSnapshotViewSet(viewsets.ReadOnlyModelViewSet):
	serializer_class = TradeAnalyticsSnapshotSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return TradeAnalyticsSnapshot.objects.filter(user=self.request.user)
