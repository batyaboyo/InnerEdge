"""Serializers for behavioral intelligence."""

from __future__ import annotations

from rest_framework import serializers

from intel.models import BehaviorInsight, BehaviorMetricDaily


class BehaviorMetricDailySerializer(serializers.ModelSerializer):
    class Meta:
        model = BehaviorMetricDaily
        fields = "__all__"


class BehaviorInsightSerializer(serializers.ModelSerializer):
    class Meta:
        model = BehaviorInsight
        fields = "__all__"
