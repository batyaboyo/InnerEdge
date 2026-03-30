"""Account and user-level trading preference models."""

from __future__ import annotations

from django.conf import settings
from django.db import models


class TraderProfile(models.Model):
	"""Stores CFD-specific profile and default risk configuration."""

	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	base_currency = models.CharField(max_length=8, default="USD")
	timezone = models.CharField(max_length=64, default="UTC")
	default_risk_percent = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)
	max_leverage_limit = models.DecimalField(max_digits=8, decimal_places=2, default=20.00)
	preferred_markets = models.JSONField(default=list, blank=True)
	margin_call_threshold_percent = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
	stop_out_threshold_percent = models.DecimalField(max_digits=5, decimal_places=2, default=50.00)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self) -> str:
		return f"Profile<{self.user_id}>"
