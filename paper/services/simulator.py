"""Paper trading simulation and margin calculations."""

from __future__ import annotations

from decimal import Decimal

from paper.models import PaperAccount, PaperPosition


def recalculate_account_metrics(account: PaperAccount) -> PaperAccount:
    """Recompute account equity and margin levels from open positions."""
    open_positions = account.positions.filter(status=PaperPosition.Status.OPEN)
    unrealized = sum((position.unrealized_pnl for position in open_positions), Decimal("0"))
    used_margin = sum(
        (
            (position.entry_price * position.size_lots) / max(position.leverage, Decimal("1"))
            for position in open_positions
        ),
        Decimal("0"),
    )
    account.used_margin = used_margin
    account.equity = account.balance + unrealized
    account.free_margin = account.equity - account.used_margin
    account.margin_level_percent = (
        (account.equity / account.used_margin) * Decimal("100") if account.used_margin > 0 else Decimal("0")
    )
    account.save(update_fields=["used_margin", "equity", "free_margin", "margin_level_percent"])
    return account
