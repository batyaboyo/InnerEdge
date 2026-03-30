"""Serializers for journal domain."""

from __future__ import annotations

from rest_framework import serializers

from journal.models import SetupTag, Trade, TradeAnalyticsSnapshot, TradeNote


class SetupTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetupTag
        fields = "__all__"


class TradeNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeNote
        fields = "__all__"


class TradeSerializer(serializers.ModelSerializer):
    notes = TradeNoteSerializer(many=True, read_only=True)

    class Meta:
        model = Trade
        fields = "__all__"


class TradeAnalyticsSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeAnalyticsSnapshot
        fields = "__all__"
