from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class EtoroDeposit:
    amount: float
    deposited_at: str
    id: int = None 
    created_at: str = None
    currency: str = 'USD'
    
    
    def as_for_insert(self):
        return (self.amount, self.currency, self.deposited_at)
    def as_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "currency": self.currency,
            "deposited_at": self.deposited_at,
            "created_at": self.created_at
        }

@dataclass
class EtoroDeposits:
    deposits: List[EtoroDeposit] = field(default_factory=list)

    def as_for_insert(self):
        return [deposit.as_for_insert() for deposit in self.deposits]
    def as_dict(self):
        return [deposit.as_dict() for deposit in self.deposits]
