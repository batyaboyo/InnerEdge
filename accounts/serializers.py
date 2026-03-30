"""Serializers for account domain."""

from __future__ import annotations

from rest_framework import serializers

from accounts.models import TraderProfile


class TraderProfileSerializer(serializers.ModelSerializer):
    """Serializer for trader profile data."""

    class Meta:
        model = TraderProfile
        fields = [
            "id",
            "user",
            "base_currency",
            "timezone",
            "default_risk_percent",
            "max_leverage_limit",
            "preferred_markets",
            "margin_call_threshold_percent",
            "stop_out_threshold_percent",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]
