"""Django admin configuration for all domains."""

from django.contrib import admin

from accounts.models import TraderProfile
from alerts.models import AlertEvent, AlertRule
from billing.models import Invoice, Plan, Subscription
from intel.models import BehaviorInsight, BehaviorMetricDaily
from journal.models import SetupTag, Trade, TradeAnalyticsSnapshot, TradeNote
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
from paper.models import PaperAccount, PaperPosition


@admin.register(TraderProfile)
class TraderProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "base_currency", "default_risk_percent", "max_leverage_limit", "created_at")
    search_fields = ("user__username", "user__email")
    list_filter = ("base_currency", "created_at")


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ("symbol", "name", "market_type", "broker", "default_leverage", "is_active")
    search_fields = ("symbol", "name")
    list_filter = ("market_type", "broker", "is_active")


@admin.register(Candle)
class CandleAdmin(admin.ModelAdmin):
    list_display = ("asset", "timeframe", "open_time", "open", "high", "low", "close")
    search_fields = ("asset__symbol",)
    list_filter = ("asset", "timeframe", "open_time")
    readonly_fields = ("open_time",)


@admin.register(LiquidityZone)
class LiquidityZoneAdmin(admin.ModelAdmin):
    list_display = ("asset", "timeframe", "side", "level_price", "touch_count", "strength_score", "is_active")
    search_fields = ("asset__symbol",)
    list_filter = ("asset", "side", "is_active")


@admin.register(SweepEvent)
class SweepEventAdmin(admin.ModelAdmin):
    list_display = ("asset", "timeframe", "direction", "swept_at", "swept_price")
    search_fields = ("asset__symbol",)
    list_filter = ("asset", "direction", "swept_at")


@admin.register(DailyBias)
class DailyBiasAdmin(admin.ModelAdmin):
    list_display = ("asset", "session_date", "bias", "previous_day_high", "previous_day_low")
    search_fields = ("asset__symbol",)
    list_filter = ("asset", "bias", "session_date")


@admin.register(FairValueGap)
class FairValueGapAdmin(admin.ModelAdmin):
    list_display = ("asset", "timeframe", "gap_type", "zone_low", "zone_high", "strength_score")
    search_fields = ("asset__symbol",)
    list_filter = ("asset", "gap_type")


@admin.register(OrderBlock)
class OrderBlockAdmin(admin.ModelAdmin):
    list_display = ("asset", "timeframe", "block_type", "zone_low", "zone_high", "strength_score")
    search_fields = ("asset__symbol",)
    list_filter = ("asset", "block_type")


@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ("user", "asset", "direction", "status", "entry_price", "exit_price", "pnl_account_currency", "opened_at")
    search_fields = ("user__username", "asset__symbol")
    list_filter = ("status", "direction", "opened_at", "asset")
    readonly_fields = ("created_at", "updated_at")


@admin.register(SetupTag)
class SetupTagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_primary_smc")
    search_fields = ("name", "slug")


@admin.register(TradeNote)
class TradeNoteAdmin(admin.ModelAdmin):
    list_display = ("trade", "created_at")
    search_fields = ("trade__user__username",)
    list_filter = ("created_at",)


@admin.register(TradeAnalyticsSnapshot)
class TradeAnalyticsSnapshotAdmin(admin.ModelAdmin):
    list_display = ("user", "period_start", "period_end", "total_trades", "win_rate", "gross_profit")
    search_fields = ("user__username",)
    list_filter = ("period_start", "period_end")


@admin.register(BehaviorMetricDaily)
class BehaviorMetricDailyAdmin(admin.ModelAdmin):
    list_display = ("user", "metric_date", "avg_leverage", "swap_cost_ratio", "long_win_rate", "short_win_rate")
    search_fields = ("user__username",)
    list_filter = ("metric_date",)


@admin.register(BehaviorInsight)
class BehaviorInsightAdmin(admin.ModelAdmin):
    list_display = ("user", "category", "severity", "title", "is_actioned", "created_at")
    search_fields = ("user__username", "title")
    list_filter = ("severity", "category", "created_at")


@admin.register(PaperAccount)
class PaperAccountAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "balance", "equity", "margin_level_percent", "is_active")
    search_fields = ("user__username", "name")
    list_filter = ("is_active", "created_at")


@admin.register(PaperPosition)
class PaperPositionAdmin(admin.ModelAdmin):
    list_display = ("account", "asset", "direction", "status", "entry_price", "current_price", "unrealized_pnl")
    search_fields = ("account__user__username", "asset__symbol")
    list_filter = ("status", "direction")


@admin.register(AlertRule)
class AlertRuleAdmin(admin.ModelAdmin):
    list_display = ("user", "rule_type", "asset", "threshold_value", "is_enabled")
    search_fields = ("user__username",)
    list_filter = ("rule_type", "is_enabled")


@admin.register(AlertEvent)
class AlertEventAdmin(admin.ModelAdmin):
    list_display = ("user", "level", "title", "is_read", "created_at")
    search_fields = ("user__username", "title")
    list_filter = ("level", "is_read", "created_at")


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "price_monthly_cents", "is_active")
    search_fields = ("code", "name")
    list_filter = ("is_active",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "status", "current_period_start", "current_period_end", "cancel_at_period_end")
    search_fields = ("user__username",)
    list_filter = ("status", "created_at")


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("subscription", "amount_paid_cents", "currency", "status", "issued_at")
    search_fields = ("subscription__user__username",)
    list_filter = ("status", "currency", "issued_at")
