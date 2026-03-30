"""Alert rule and event models."""

from __future__ import annotations

from django.conf import settings
from django.db import models

from market.models import Asset


class AlertRule(models.Model):
	"""User-defined alert rules for market and risk events."""

	class RuleType(models.TextChoices):
		LIQUIDITY_BUILD = "liquidity_build", "Liquidity Build"
		LIQUIDITY_SWEEP = "liquidity_sweep", "Liquidity Sweep"
		MARGIN_RISK = "margin_risk", "Margin Risk"
		LEVERAGE_WARNING = "leverage_warning", "Leverage Warning"
		SWAP_IMPACT = "swap_impact", "Swap Impact"

	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="alert_rules")
	asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="alert_rules", null=True, blank=True)
	rule_type = models.CharField(max_length=24, choices=RuleType.choices)
	threshold_value = models.DecimalField(max_digits=18, decimal_places=5, null=True, blank=True)
	config = models.JSONField(default=dict, blank=True)
	is_enabled = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)


class AlertEvent(models.Model):
	"""Alert event generated from rules or system checks."""

	class Level(models.TextChoices):
		INFO = "info", "Info"
		WARNING = "warning", "Warning"
		CRITICAL = "critical", "Critical"

	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="alert_events")
	rule = models.ForeignKey(AlertRule, on_delete=models.SET_NULL, null=True, blank=True, related_name="events")
	asset = models.ForeignKey(Asset, on_delete=models.SET_NULL, null=True, blank=True, related_name="alert_events")
	level = models.CharField(max_length=8, choices=Level.choices)
	title = models.CharField(max_length=160)
	message = models.TextField()
	payload = models.JSONField(default=dict, blank=True)
	is_read = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
