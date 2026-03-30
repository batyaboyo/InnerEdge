"""Serializers for paper trading domain."""

from __future__ import annotations

from rest_framework import serializers

from paper.models import PaperAccount, PaperPosition


class PaperAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperAccount
        fields = "__all__"


class PaperPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperPosition
        fields = "__all__"
