"""Paper trading models for simulated CFD execution."""

from __future__ import annotations

from django.conf import settings
from django.db import models

from market.models import Asset


class PaperAccount(models.Model):
	"""Simulated account with margin and equity tracking."""

	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="paper_accounts")
	name = models.CharField(max_length=120)
	balance = models.DecimalField(max_digits=18, decimal_places=2, default=10000)
	equity = models.DecimalField(max_digits=18, decimal_places=2, default=10000)
	used_margin = models.DecimalField(max_digits=18, decimal_places=2, default=0)
	free_margin = models.DecimalField(max_digits=18, decimal_places=2, default=10000)
	margin_level_percent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)


class PaperPosition(models.Model):
	"""Simulated position with CFD cost metadata."""

	class Direction(models.TextChoices):
		LONG = "long", "Long"
		SHORT = "short", "Short"

	class Status(models.TextChoices):
		OPEN = "open", "Open"
		CLOSED = "closed", "Closed"

	account = models.ForeignKey(PaperAccount, on_delete=models.CASCADE, related_name="positions")
	asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="paper_positions")
	direction = models.CharField(max_length=8, choices=Direction.choices)
	status = models.CharField(max_length=8, choices=Status.choices, default=Status.OPEN)
	entry_price = models.DecimalField(max_digits=18, decimal_places=8)
	current_price = models.DecimalField(max_digits=18, decimal_places=8)
	size_lots = models.DecimalField(max_digits=12, decimal_places=4)
	leverage = models.DecimalField(max_digits=8, decimal_places=2)
	stop_loss = models.DecimalField(max_digits=18, decimal_places=8, null=True, blank=True)
	take_profit = models.DecimalField(max_digits=18, decimal_places=8, null=True, blank=True)
	unrealized_pnl = models.DecimalField(max_digits=18, decimal_places=2, default=0)
	realized_pnl = models.DecimalField(max_digits=18, decimal_places=2, default=0)
	swap_accrued = models.DecimalField(max_digits=18, decimal_places=2, default=0)
	opened_at = models.DateTimeField(auto_now_add=True)
	closed_at = models.DateTimeField(null=True, blank=True)
