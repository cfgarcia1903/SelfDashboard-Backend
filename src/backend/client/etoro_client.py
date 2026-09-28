from backend.constants.constants import ETORO_BASE_URL

import uuid
import requests


class EtoroClient:
    ETORO_REAL_PNL_URL = f"{ETORO_BASE_URL}/trading/info/real/pnl"
    ETORO_BALANCES_URL = f"{ETORO_BASE_URL}/balances"
    ETORO_BALANCES_HISTORY_URL = f"{ETORO_BASE_URL}/balances/history"

    @classmethod
    def get_available_cash(cls,public_key: str, user_key: str) -> float:
        headers = {
            "x-api-key": public_key,
            "x-user-key": user_key,
            "x-request-id": str(uuid.uuid4()),
        }

        response = requests.get(
            cls.ETORO_REAL_PNL_URL,
            headers=headers,
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        credits = data["clientPortfolio"]["credit"]

        orders_for_open_amount = sum(
            order["amount"]
            for order in data["clientPortfolio"]["ordersForOpen"]
            if order["mirrorID"] == 0
        )

        orders_amount = sum(
            order["amount"]
            for order in data["clientPortfolio"]["orders"]
        )

        available_cash = (
            credits
            - orders_for_open_amount
            - orders_amount
        )

        return {"total_cash": credits, "reserved_cash": orders_for_open_amount + orders_amount, "available_cash": available_cash}

    @classmethod
    def get_balance(cls, public_key: str, user_key: str) -> dict:

        headers = {
            "x-api-key": public_key,
            "x-user-key": user_key,
            "x-request-id": str(uuid.uuid4()),
            "Accept": "application/json",
        }

        # Current balance
        balance_response = requests.get(
            cls.ETORO_BALANCES_URL,
            headers=headers,
            params={
                "displayCurrency": "USD",
            },
            timeout=10,
        )

        balance_response.raise_for_status()
        balance = balance_response.json()

        return balance
    
    @classmethod
    def get_balance_snapshots(cls, public_key: str, user_key: str) -> list:

        headers = {
            "x-api-key": public_key,
            "x-user-key": user_key,
            "x-request-id": str(uuid.uuid4()),
            "Accept": "application/json",
        }


        # Historical daily balances
        history_response = requests.get(
            cls.ETORO_BALANCES_HISTORY_URL,
            headers=headers,
            params={
                "displayCurrency": "USD",
            },
            timeout=10,
        )

        history_response.raise_for_status()
        history = history_response.json()

        snapshots = history.get("snapshots", [])
        return snapshots
 