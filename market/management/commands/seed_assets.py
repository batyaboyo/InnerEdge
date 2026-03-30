"""Management command to seed sample CFD assets."""

from decimal import Decimal

from django.core.management.base import BaseCommand

from market.models import Asset


class Command(BaseCommand):
    help = "Seed sample CFD assets (Forex, Indices, Commodities)"

    def handle(self, *args, **options):
        assets_data = [
            {
                "symbol": "EURUSD",
                "name": "Euro / US Dollar",
                "market_type": Asset.MarketType.FOREX,
                "broker": "oanda",
                "base_currency": "EUR",
                "quote_currency": "USD",
                "default_leverage": Decimal("50"),
                "max_leverage": Decimal("50"),
            },
            {
                "symbol": "GBPUSD",
                "name": "British Pound / US Dollar",
                "market_type": Asset.MarketType.FOREX,
                "broker": "oanda",
                "base_currency": "GBP",
                "quote_currency": "USD",
                "default_leverage": Decimal("50"),
                "max_leverage": Decimal("50"),
            },
            {
                "symbol": "SPX500",
                "name": "S&P 500 Index",
                "market_type": Asset.MarketType.INDEX,
                "broker": "ig",
                "base_currency": "USD",
                "quote_currency": "USD",
                "default_leverage": Decimal("20"),
                "max_leverage": Decimal("20"),
            },
            {
                "symbol": "XAUUSD",
                "name": "Gold / US Dollar",
                "market_type": Asset.MarketType.COMMODITY,
                "broker": "oanda",
                "base_currency": "XAU",
                "quote_currency": "USD",
                "default_leverage": Decimal("10"),
                "max_leverage": Decimal("10"),
            },
            {
                "symbol": "BTCUSDT",
                "name": "Bitcoin / US Dollar Tether",
                "market_type": Asset.MarketType.CRYPTO,
                "broker": "binance",
                "base_currency": "BTC",
                "quote_currency": "USDT",
                "default_leverage": Decimal("10"),
                "max_leverage": Decimal("125"),
            },
        ]

        created_count = 0
        for asset_data in assets_data:
            _, created = Asset.objects.get_or_create(symbol=asset_data["symbol"], defaults=asset_data)
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"✓ Created asset: {asset_data['symbol']}"))
            else:
                self.stdout.write(self.style.WARNING(f"⊗ Asset already exists: {asset_data['symbol']}"))

        self.stdout.write(self.style.SUCCESS(f"\n{created_count} assets created."))
