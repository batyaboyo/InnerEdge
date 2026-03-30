"""Behavioral insight service for CFD trading performance."""

from __future__ import annotations

from decimal import Decimal
from typing import Any

from django.contrib.auth import get_user_model
from django.db.models import Avg, Count, Sum

from journal.models import Trade
from intel.models import BehaviorInsight

User = get_user_model()


def generate_behavior_insights(user: Any) -> list[BehaviorInsight]:
    """Generate human-readable behavior insights without market prediction."""
    closed = Trade.objects.filter(user=user, status=Trade.Status.CLOSED)
    if not closed.exists():
        return []

    created: list[BehaviorInsight] = []
    leverage_avg = closed.aggregate(value=Avg("leverage"))["value"] or Decimal("0")
    total_swap = closed.aggregate(value=Sum("swap_fee"))["value"] or Decimal("0")
    gross_pnl = closed.aggregate(value=Sum("pnl_account_currency"))["value"] or Decimal("0")

    if leverage_avg > Decimal("30"):
        created.append(
            BehaviorInsight.objects.create(
                user=user,
                category="leverage",
                severity=BehaviorInsight.Severity.HIGH,
                title="Over-leverage pattern detected",
                detail="Average leverage is above 30x, which raises stop-out and margin-call risk.",
                evidence={"avg_leverage": str(leverage_avg)},
            )
        )

    if total_swap < Decimal("-50"):
        created.append(
            BehaviorInsight.objects.create(
                user=user,
                category="swap",
                severity=BehaviorInsight.Severity.MEDIUM,
                title="Swap costs are materially reducing returns",
                detail="Cumulative overnight swaps are materially negative and eroding profitability.",
                evidence={"swap_total": str(total_swap)},
            )
        )

    short_stats = closed.filter(direction=Trade.Direction.SHORT).aggregate(
        trades=Count("id"),
        pnl=Sum("pnl_account_currency"),
    )
    long_stats = closed.filter(direction=Trade.Direction.LONG).aggregate(
        trades=Count("id"),
        pnl=Sum("pnl_account_currency"),
    )

    if (short_stats["trades"] or 0) >= 10 and (short_stats["pnl"] or 0) < (long_stats["pnl"] or 0):
        created.append(
            BehaviorInsight.objects.create(
                user=user,
                category="directional-behavior",
                severity=BehaviorInsight.Severity.MEDIUM,
                title="Short-side execution underperforms long-side",
                detail="Journal data indicates weaker outcomes on short CFD positions versus long positions.",
                evidence={"short": short_stats, "long": long_stats, "gross_pnl": str(gross_pnl)},
            )
        )

    return created
