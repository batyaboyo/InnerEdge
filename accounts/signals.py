"""Signal handlers for account bootstrapping."""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import TraderProfile

User = get_user_model()


@receiver(post_save, sender=User)
def create_trader_profile(sender, instance: User, created: bool, **kwargs) -> None:
    """Create profile row whenever a new user is registered."""
    if created:
        TraderProfile.objects.create(user=instance)
