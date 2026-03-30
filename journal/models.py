"""CFD trading journal and performance models."""

from __future__ import annotations

from django.conf import settings
from django.db import models

from market.models import Asset


class SetupTag(models.Model):
	"""Tag trades by setup archetype and SMC context."""

	name = models.CharField(max_length=64, unique=True)
	slug = models.SlugField(max_length=64, unique=True)
	is_primary_smc = models.BooleanField(default=False)

	def __str__(self) -> str:
		return self.name


class Trade(models.Model):
	"""Primary CFD trade record."""

	class Direction(models.TextChoices):
		LONG = "long", "Long"
		SHORT = "short", "Short"

	class Status(models.TextChoices):
		OPEN = "open", "Open"
		CLOSED = "closed", "Closed"

	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="trades")
	asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="trades")
	direction = models.CharField(max_length=8, choices=Direction.choices)
	status = models.CharField(max_length=8, choices=Status.choices, default=Status.OPEN)
	entry_price = models.DecimalField(max_digits=18, decimal_places=8)
	exit_price = models.DecimalField(max_digits=18, decimal_places=8, null=True, blank=True)
	stop_loss = models.DecimalField(max_digits=18, decimal_places=8)
	take_profit = models.DecimalField(max_digits=18, decimal_places=8)
	position_size_lots = models.DecimalField(max_digits=12, decimal_places=4)
	leverage = models.DecimalField(max_digits=8, decimal_places=2)
	margin_used = models.DecimalField(max_digits=18, decimal_places=2, default=0)
	swap_fee = models.DecimalField(max_digits=18, decimal_places=2, default=0)
	commission = models.DecimalField(max_digits=18, decimal_places=2, default=0)
	pnl_account_currency = models.DecimalField(max_digits=18, decimal_places=2, default=0)
	pnl_base_currency = models.DecimalField(max_digits=18, decimal_places=2, default=0)
	account_currency = models.CharField(max_length=8, default="USD")
	base_currency = models.CharField(max_length=8, default="USD")
	risk_percent = models.DecimalField(max_digits=5, decimal_places=2)
	opened_at = models.DateTimeField()
	closed_at = models.DateTimeField(null=True, blank=True)
	screenshot_url = models.URLField(blank=True)
	tags = models.ManyToManyField(SetupTag, related_name="trades", blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class TradeNote(models.Model):
	"""Free-form note attached to a trade."""

	trade = models.ForeignKey(Trade, on_delete=models.CASCADE, related_name="notes")
	note = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)


class TradeAnalyticsSnapshot(models.Model):
	"""Cached analytics for a user over a time range."""

	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name="analytics_snapshots",
	)
	period_start = models.DateField()
	period_end = models.DateField()
	total_trades = models.PositiveIntegerField(default=0)
	win_rate = models.DecimalField(max_digits=6, decimal_places=2, default=0)
	avg_r_multiple = models.DecimalField(max_digits=10, decimal_places=4, default=0)
	gross_profit = models.DecimalField(max_digits=18, decimal_places=2, default=0)
	gross_loss = models.DecimalField(max_digits=18, decimal_places=2, default=0)
	created_at = models.DateTimeField(auto_now_add=True)
