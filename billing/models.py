"""Billing and subscription domain models."""

from __future__ import annotations

from django.conf import settings
from django.db import models


class Plan(models.Model):
	"""SaaS subscription plan metadata."""

	code = models.CharField(max_length=32, unique=True)
	name = models.CharField(max_length=64)
	price_monthly_cents = models.PositiveIntegerField()
	features = models.JSONField(default=dict, blank=True)
	stripe_product_id = models.CharField(max_length=128, blank=True)
	stripe_price_id = models.CharField(max_length=128, blank=True)
	is_active = models.BooleanField(default=True)


class Subscription(models.Model):
	"""Current user subscription status."""

	class Status(models.TextChoices):
		TRIAL = "trial", "Trial"
		ACTIVE = "active", "Active"
		PAST_DUE = "past_due", "Past Due"
		CANCELED = "canceled", "Canceled"

	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions")
	plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name="subscriptions")
	status = models.CharField(max_length=16, choices=Status.choices, default=Status.TRIAL)
	stripe_customer_id = models.CharField(max_length=128, blank=True)
	stripe_subscription_id = models.CharField(max_length=128, blank=True)
	current_period_start = models.DateTimeField(null=True, blank=True)
	current_period_end = models.DateTimeField(null=True, blank=True)
	cancel_at_period_end = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class Invoice(models.Model):
	"""Stripe invoice mirror for account history."""

	subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name="invoices")
	stripe_invoice_id = models.CharField(max_length=128, unique=True)
	amount_paid_cents = models.PositiveIntegerField(default=0)
	currency = models.CharField(max_length=8, default="usd")
	status = models.CharField(max_length=32)
	invoice_pdf_url = models.URLField(blank=True)
	issued_at = models.DateTimeField()
