"""Stripe integration helpers for subscriptions."""

from __future__ import annotations

from typing import Any

import stripe
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY


def build_checkout_session(price_id: str, customer_email: str, success_url: str, cancel_url: str) -> stripe.checkout.Session:
    """Create checkout session for a recurring subscription."""
    return stripe.checkout.Session.create(
        mode="subscription",
        line_items=[{"price": price_id, "quantity": 1}],
        customer_email=customer_email,
        success_url=success_url,
        cancel_url=cancel_url,
    )


def verify_webhook(payload: bytes, sig_header: str) -> dict[str, Any]:
    """Verify and parse Stripe webhook event."""
    event = stripe.Webhook.construct_event(
        payload=payload,
        sig_header=sig_header,
        secret=settings.STRIPE_WEBHOOK_SECRET,
    )
    return event
