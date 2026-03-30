"""Tests for trader accounts module."""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

from accounts.models import TraderProfile

User = get_user_model()


class TraderProfileModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="trader", email="trader@test.com", password="pass123")

    def test_trader_profile_auto_creation(self):
        """Test TraderProfile is auto-created on user registration."""
        profile = TraderProfile.objects.get(user=self.user)
        self.assertEqual(profile.base_currency, "USD")
        self.assertEqual(profile.default_risk_percent, Decimal("1.00"))
        self.assertEqual(profile.max_leverage_limit, Decimal("20.00"))

    def test_trader_profile_updates(self):
        """Test TraderProfile field updates."""
        profile = TraderProfile.objects.get(user=self.user)
        profile.default_risk_percent = Decimal("2.50")
        profile.max_leverage_limit = Decimal("50.00")
        profile.save()

        profile.refresh_from_db()
        self.assertEqual(profile.default_risk_percent, Decimal("2.50"))
        self.assertEqual(profile.max_leverage_limit, Decimal("50.00"))


class TraderProfileAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="trader", email="trader@test.com", password="pass123")
        self.profile = TraderProfile.objects.get(user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_retrieve_own_profile(self):
        """Test authenticated user can retrieve their profile."""
        response = self.client.get("/api/accounts/profiles/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.profile.id, [p["id"] for p in response.data])

    def test_profile_update(self):
        """Test profile update."""
        response = self.client.patch(
            f"/api/accounts/profiles/{self.profile.id}/",
            {"default_risk_percent": "3.00"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data["default_risk_percent"]), 3.0)

    def test_unauthenticated_cannot_access(self):
        """Test unauthenticated users cannot access profile endpoint."""
        self.client.force_authenticate(user=None)
        response = self.client.get("/api/accounts/profiles/")
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
