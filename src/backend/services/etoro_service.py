from typing import Dict, List

from backend.client.etoro_client import EtoroClient
from backend.schemas.request_schemas import EtoroAccountSummary
from backend.schemas.data_schemas import EtoroDeposit, EtoroDeposits
from backend.dao.etoro_dao import EtoroDAO


class EtoroService:

    @classmethod
    def get_account_summary(cls, public_key: str,
                            user_key: str) -> EtoroAccountSummary:

        balance = EtoroClient.get_balance(public_key, user_key)
        snapshots = EtoroClient.get_balance_snapshots(public_key, user_key)

        if not snapshots:
            raise RuntimeError(
                "No historical balance snapshots were returned"
            )

        # The latest snapshot is the most recent EOD snapshot.
        latest_snapshot = max(
            snapshots,
            key=lambda snapshot: snapshot["date"],
        )

        current_balance = balance["totalBalance"]
        current_cash = EtoroClient.get_available_cash(public_key, user_key)
        total_deposits = EtoroDAO.get_total_deposits()

        previous_balance = latest_snapshot["displayTotalBalance"] 

        change = current_balance - previous_balance ## implementar que considere deposito del dia

        change_pct = (
            (change / previous_balance) * 100
            if previous_balance != 0
            else None
        )

        return EtoroAccountSummary(
            currency="USD",
            total_balance=current_balance,
            total_cash=current_cash["total_cash"],
            reserved_cash=current_cash["reserved_cash"],
            available_cash=current_cash["available_cash"],
            deposits=total_deposits,
            last_close_date=latest_snapshot["date"],
            last_close_balance=previous_balance,
            change_since_last_close=change,
            change_since_last_close_pct=change_pct,
        )

    @classmethod
    def get_deposits(cls) -> List[Dict] | None:
        deposits = EtoroDAO.query_deposits()
        if not deposits:
            return None
        else:
            return deposits.as_dict()

    @classmethod
    def update_deposits(cls, deposits: List[Dict]) -> List[Dict] | None:
        deposits_to_update = EtoroDeposits(
            deposits=[EtoroDeposit(**deposit) for deposit in deposits]
        )
        EtoroDAO.update_deposits(deposits_to_update)
        updated_deposits = EtoroDAO.query_deposits()
        if not updated_deposits:
            return None
        else:
            return updated_deposits.as_dict()

    @classmethod
    def delete_deposits(cls, deposit_ids: List[int]) -> None:
        EtoroDAO.delete_deposits(deposit_ids)
        updated_deposits = EtoroDAO.query_deposits()
        if not updated_deposits:
            return None
        else:
            return updated_deposits.as_dict()