"""Pytest configuration and fixtures."""

import os
import django
from django.conf import settings

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    """Return a REST API test client."""
    return APIClient()


@pytest.fixture
def authenticated_user(db):
    """Create an authenticated test user."""
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )
    return user


@pytest.fixture
def authenticated_client(api_client, authenticated_user):
    """Return an authenticated API client."""
    api_client.force_authenticate(user=authenticated_user)
    return api_client


@pytest.fixture
def trader_profile(db, authenticated_user):
    """Create a trader profile for authenticated user."""
    from accounts.models import TraderProfile
    profile = TraderProfile.objects.get(user=authenticated_user)
    return profile


@pytest.fixture
def test_asset(db):
    """Create a test asset."""
    from market.models import Asset
    asset = Asset.objects.create(
        symbol='EURUSD',
        name='Euro/USD',
        market_type=Asset.MarketType.FOREX,
        broker='test_broker'
    )
    return asset


@pytest.fixture
def test_plan(db):
    """Create a test billing plan."""
    from billing.models import Plan
    plan = Plan.objects.create(
        code='pro',
        name='Pro Plan',
        price_monthly_cents=9900,
        features={'alerts': True, 'ai_insights': True},
        stripe_product_id='prod_test',
        stripe_price_id='price_test'
    )
    return plan
