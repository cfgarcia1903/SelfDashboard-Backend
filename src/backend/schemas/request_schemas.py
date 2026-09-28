from dataclasses import dataclass


@dataclass
class EtoroAccountSummary:
    currency: str = ''
    total_balance: float = 0.0
    total_cash: float = 0.0
    reserved_cash: float = 0.0
    available_cash: float = 0.0
    deposits: float = 0.0
    last_close_date: str = ''
    last_close_balance: float = 0.0
    change_since_last_close: float = 0.0
    change_since_last_close_pct: float = 0.0
