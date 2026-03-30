"""Management command to seed setup tags."""

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from journal.models import SetupTag


class Command(BaseCommand):
    help = "Seed SMC setup tags for trade classification"

    def handle(self, *args, **options):
        tags_data = [
            ("Liquidity Sweep", True),
            ("Fair Value Gap", False),
            ("Order Block", False),
            ("Daily Bias Confluence", True),
            ("Multiple Liquidity Pools", True),
            ("Institutional Order Flow", True),
            ("Market Structure Break", False),
            ("Swing High/Low", False),
        ]

        created_count = 0
        for name, is_primary in tags_data:
            slug = slugify(name)
            _, created = SetupTag.objects.get_or_create(
                name=name,
                defaults={"slug": slug, "is_primary_smc": is_primary},
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"✓ Created tag: {name}"))
            else:
                self.stdout.write(self.style.WARNING(f"⊗ Tag already exists: {name}"))

        self.stdout.write(self.style.SUCCESS(f"\n{created_count} tags created."))
