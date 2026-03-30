"""Serializers for alerts module."""

from __future__ import annotations

from rest_framework import serializers

from alerts.models import AlertEvent, AlertRule


class AlertRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertRule
        fields = "__all__"
        read_only_fields = ("user", "created_at")


class AlertEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertEvent
        fields = "__all__"
        read_only_fields = ("user", "created_at")
