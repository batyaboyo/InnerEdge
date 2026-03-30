"""Serializers for market and SMC data."""

from __future__ import annotations

from rest_framework import serializers

from market.models import (
    Asset,
    Candle,
    CFDCondition,
    DailyBias,
    FairValueGap,
    LiquidityZone,
    OrderBlock,
    SweepEvent,
)


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = "__all__"


class CFDConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CFDCondition
        fields = "__all__"


class CandleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candle
        fields = "__all__"


class LiquidityZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiquidityZone
        fields = "__all__"


class SweepEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = SweepEvent
        fields = "__all__"


class DailyBiasSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyBias
        fields = "__all__"


class FairValueGapSerializer(serializers.ModelSerializer):
    class Meta:
        model = FairValueGap
        fields = "__all__"


class OrderBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderBlock
        fields = "__all__"
