"""Management command to seed subscription plans."""

from django.core.management.base import BaseCommand

from billing.models import Plan


class Command(BaseCommand):
    help = "Seed SaaS subscription plans"

    def handle(self, *args, **options):
        plans_data = [
            {
                "code": "free",
                "name": "Free",
                "price_monthly_cents": 0,
                "features": {
                    "max_trades_per_month": 50,
                    "liquidity_zones": True,
                    "daily_bias": True,
                    "fvg": False,
                    "order_blocks": False,
                    "ai_insights": False,
                    "paper_trading": False,
                    "alerts": False,
                },
            },
            {
                "code": "pro",
                "name": "Pro",
                "price_monthly_cents": 4999,  # $49.99
                "features": {
                    "max_trades_per_month": 1000,
                    "liquidity_zones": True,
                    "daily_bias": True,
                    "fvg": True,
                    "order_blocks": True,
                    "ai_insights": False,
                    "paper_trading": True,
                    "alerts": True,
                },
            },
            {
                "code": "premium",
                "name": "Premium",
                "price_monthly_cents": 9999,  # $99.99
                "features": {
                    "max_trades_per_month": 10000,
                    "liquidity_zones": True,
                    "daily_bias": True,
                    "fvg": True,
                    "order_blocks": True,
                    "ai_insights": True,
                    "paper_trading": True,
                    "alerts": True,
                    "priority_support": True,
                    "custom_brokers": True,
                },
            },
        ]

        created_count = 0
        for plan_data in plans_data:
            _, created = Plan.objects.get_or_create(code=plan_data["code"], defaults=plan_data)
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"✓ Created plan: {plan_data['name']}"))
            else:
                self.stdout.write(self.style.WARNING(f"⊗ Plan already exists: {plan_data['code']}"))

        self.stdout.write(self.style.SUCCESS(f"\n{created_count} plans created."))
