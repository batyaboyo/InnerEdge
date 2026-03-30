"""REST API views for market data and SMC engines."""

from __future__ import annotations

from rest_framework import decorators, permissions, response, status, viewsets

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
from market.serializers import (
    AssetSerializer,
    CandleSerializer,
    CFDConditionSerializer,
    DailyBiasSerializer,
    FairValueGapSerializer,
    LiquidityZoneSerializer,
    OrderBlockSerializer,
    SweepEventSerializer,
)
from market.services.liquidity import (
    compute_daily_bias,
    detect_fair_value_gaps,
    detect_liquidity_sweeps,
    detect_liquidity_zones,
    detect_order_blocks,
)


class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [permissions.IsAuthenticated]

    @decorators.action(detail=True, methods=["post"], url_path="run-liquidity")
    def run_liquidity(self, request, pk=None):
        asset = self.get_object()
        timeframe = request.data.get("timeframe", Candle.Timeframe.H1)
        zones = detect_liquidity_zones(asset=asset, timeframe=timeframe)
        sweeps = detect_liquidity_sweeps(asset=asset, timeframe=timeframe)
        fvg_count = detect_fair_value_gaps(asset=asset, timeframe=timeframe)
        ob_count = detect_order_blocks(asset=asset, timeframe=timeframe)
        bias = compute_daily_bias(asset=asset)
        return response.Response(
            {
                "asset": asset.symbol,
                "timeframe": timeframe,
                "zones_created": zones,
                "sweeps_created": sweeps,
                "fvg_created": fvg_count,
                "order_blocks_created": ob_count,
                "daily_bias": bias.bias if bias else None,
            },
            status=status.HTTP_200_OK,
        )


class CFDConditionViewSet(viewsets.ModelViewSet):
    queryset = CFDCondition.objects.select_related("asset").all()
    serializer_class = CFDConditionSerializer
    permission_classes = [permissions.IsAuthenticated]


class CandleViewSet(viewsets.ModelViewSet):
    queryset = Candle.objects.select_related("asset").all()
    serializer_class = CandleSerializer
    permission_classes = [permissions.IsAuthenticated]


class LiquidityZoneViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LiquidityZone.objects.select_related("asset").all()
    serializer_class = LiquidityZoneSerializer
    permission_classes = [permissions.IsAuthenticated]


class SweepEventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SweepEvent.objects.select_related("asset", "liquidity_zone").all()
    serializer_class = SweepEventSerializer
    permission_classes = [permissions.IsAuthenticated]


class DailyBiasViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DailyBias.objects.select_related("asset").all()
    serializer_class = DailyBiasSerializer
    permission_classes = [permissions.IsAuthenticated]


class FairValueGapViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FairValueGap.objects.select_related("asset").all()
    serializer_class = FairValueGapSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrderBlockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OrderBlock.objects.select_related("asset").all()
    serializer_class = OrderBlockSerializer
    permission_classes = [permissions.IsAuthenticated]
