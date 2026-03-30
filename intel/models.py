"""Behavioral analytics and AI insight models."""

from __future__ import annotations

from django.conf import settings
from django.db import models


class BehaviorMetricDaily(models.Model):
	"""Daily behavior metrics used by the AI behavioral engine."""

	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="behavior_metrics")
	metric_date = models.DateField()
	avg_leverage = models.DecimalField(max_digits=8, decimal_places=2, default=0)
	swap_cost_ratio = models.DecimalField(max_digits=8, decimal_places=4, default=0)
	long_win_rate = models.DecimalField(max_digits=6, decimal_places=2, default=0)
	short_win_rate = models.DecimalField(max_digits=6, decimal_places=2, default=0)
	risk_breach_count = models.PositiveIntegerField(default=0)
	overtrade_count = models.PositiveIntegerField(default=0)

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=["user", "metric_date"], name="uniq_metric_per_user_day")
		]


class BehaviorInsight(models.Model):
	"""Generated behavioral insight without directional price prediction."""

	class Severity(models.TextChoices):
		LOW = "low", "Low"
		MEDIUM = "medium", "Medium"
		HIGH = "high", "High"

	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="behavior_insights")
	category = models.CharField(max_length=64)
	severity = models.CharField(max_length=8, choices=Severity.choices)
	title = models.CharField(max_length=160)
	detail = models.TextField()
	evidence = models.JSONField(default=dict, blank=True)
	is_actioned = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
