from datetime import datetime

from backend.business.bcrp_business import BCRPBusiness
from backend.schemas.data_schemas import EtoroDeposits, EtoroDeposit
from backend.client.etoro_client import EtoroClient
import os
from pathlib import Path
import sqlite3


class EtoroDAO:
    ETORO_DB_PATH = Path(os.getenv("ETORO_DB_PATH"))
    ETORO_DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    @classmethod
    def query_deposits(cls, filter = None):
        with sqlite3.connect(cls.ETORO_DB_PATH) as connection:
            query = f"SELECT * FROM h_deposits"
            if filter:
                query+= f" WHERE {filter}"
            result = connection.execute(query)
            rows = result.fetchall()

        deposits = [EtoroDeposit(id=row[0], amount=row[1], 
                                 currency=row[2], deposited_at=row[3], 
                                 created_at=row[4]) 
                                 for row in rows]
        
        return EtoroDeposits(deposits=deposits)

    @classmethod
    def insert_deposits(cls, deposits: EtoroDeposits):

        with sqlite3.connect(cls.ETORO_DB_PATH) as connection:
            connection.executemany("""
                INSERT INTO h_deposits (
                    amount,
                    currency,
                    deposited_at
                )
                VALUES (?, ?, ?)
            """, deposits.as_for_insert())

    
    @classmethod
    def update_deposits(cls, deposits: EtoroDeposits):
        current_deposits = cls.query_deposits()

        for deposit in deposits.deposits:
            if deposit.id is None:
                # Insert new deposit
                cls.insert_deposits(EtoroDeposits(deposits=[deposit]))
            if deposit.id is not None:
                # Update existing deposit
                with sqlite3.connect(cls.ETORO_DB_PATH) as connection:
                    connection.execute("""
                        UPDATE h_deposits
                        SET amount = ?, currency = ?, deposited_at = ?
                        WHERE id = ?
                    """, (deposit.amount, deposit.currency, deposit.deposited_at, deposit.id))

    @classmethod
    def delete_deposits(cls, deposit_ids: list):
        with sqlite3.connect(cls.ETORO_DB_PATH) as connection:
            connection.executemany("""
                DELETE FROM h_deposits WHERE id = ?
            """, [(deposit_id,) for deposit_id in deposit_ids])
        

    @classmethod
    def get_total_deposits(cls) -> float:
        deposits = cls.query_deposits()
        total = sum([deposit.amount for deposit in deposits.deposits])
        return total

    @classmethod
    def get_latest_snapshots(cls, period: str = "1M") -> list:
        if period not in ["1M", "3M", "6M", "1Y", "3Y", "5Y", "10Y", "ALL"]:
            raise ValueError("Invalid period. Must be one of: '1M', '3M', '6M', '1Y', '3Y', '5Y', '10Y', 'ALL'.")

        match period:
            case "1M":
                sqlite_query = "SELECT * FROM h_snapshots WHERE snapshot_date BETWEEN date('now', '-1 month') AND date('now') ORDER BY snapshot_date DESC ;"
            case "3M":
                sqlite_query = "SELECT * FROM h_snapshots WHERE snapshot_date BETWEEN date('now', '-3 months') AND date('now') ORDER BY snapshot_date DESC ;"
            case "6M":
                sqlite_query = "SELECT * FROM h_snapshots WHERE snapshot_date BETWEEN date('now', '-6 months') AND date('now') ORDER BY snapshot_date DESC ;"
            case "1Y":
                sqlite_query = "SELECT * FROM h_snapshots WHERE snapshot_date BETWEEN date('now', '-1 year') AND date('now') ORDER BY snapshot_date DESC ;"
            case "3Y":
                sqlite_query = "SELECT * FROM h_snapshots WHERE snapshot_date BETWEEN date('now', '-3 years') AND date('now') ORDER BY snapshot_date DESC ;"
            case "5Y":
                sqlite_query = "SELECT * FROM h_snapshots WHERE snapshot_date BETWEEN date('now', '-5 years') AND date('now') ORDER BY snapshot_date DESC ;"
            case "10Y":
                sqlite_query = "SELECT * FROM h_snapshots WHERE snapshot_date BETWEEN date('now', '-10 years') AND date('now') ORDER BY snapshot_date DESC ;"
            case "ALL":
                sqlite_query = "SELECT * FROM h_snapshots WHERE snapshot_date ORDER BY snapshot_date DESC ;"

        with sqlite3.connect(cls.ETORO_DB_PATH) as connection:
            result = connection.execute(sqlite_query)
            rows = result.fetchall()

        return rows

    @classmethod
    def update_snapshots(cls, public_key: str, user_key: str) -> None:
        
        with sqlite3.connect(cls.ETORO_DB_PATH) as connection:
            result = connection.execute("SELECT * FROM h_snapshots WHERE snapshot_date ORDER BY snapshot_date DESC LIMIT 1;")
            rows = result.fetchall()
        last_snapshot_date = rows[0][4] if rows else None
        if last_snapshot_date:
            #toca actualizar la tabla
            exchange_rates = BCRPBusiness.retrieve_exchange_rates(last_snapshot_date, datetime.now().strftime("%Y-%m-%d"))

            nr_last_days = (datetime.now() - datetime.strptime(last_snapshot_date, "%Y-%m-%d")).days
            new_snapshots = EtoroClient.get_balance_snapshots(public_key, user_key, nr_last_days=nr_last_days)
            
            inserts = []
            for snapshot in new_snapshots:
                value_usd = snapshot["totalBalance"]
                exchange_rate = (exchange_rates[snapshot["date"]]["buy"] + exchange_rates[snapshot["date"]]["sell"] )/ 2
                value_pen = value_usd * exchange_rate
                if snapshot["date"] == last_snapshot_date:
                    # Update existing snapshot
                    with sqlite3.connect(cls.ETORO_DB_PATH) as connection:
                        connection.execute("""
                            UPDATE h_snapshots
                            SET value_usd = ?, value_pen = ?, exchange_rate = ?
                            WHERE snapshot_date = ?
                        """, (value_usd, value_pen, exchange_rate, snapshot["date"]))
                else:
                    inserts.append((value_usd, value_pen, exchange_rate, snapshot["date"]))

            if inserts:
                with sqlite3.connect(cls.ETORO_DB_PATH) as connection:
                    connection.executemany("""
                        INSERT INTO h_snapshots (
                            value_usd,
                            value_pen,
                            exchange_rate,
                            snapshot_date
                        )
                        VALUES (?, ?, ?, ?)
                    """, inserts)


        else:
            #poblar toda la tabla con los 365 dias ultimos desde la fecha actual
            new_snapshots = EtoroClient.get_balance_snapshots(public_key, user_key, nr_last_days=365)
            snapshot_dates = [datetime.strptime(snapshot["date"], "%Y-%m-%d") for snapshot in new_snapshots]
            fist_date = min(snapshot_dates)
            last_date = max(snapshot_dates)


            exchange_rates = BCRPBusiness.retrieve_exchange_rates(fist_date.strftime("%Y-%m-%d"), last_date.strftime("%Y-%m-%d"))
            
            
            inserts = []
            for snapshot in new_snapshots:
                value_usd = snapshot["totalBalance"]
                exchange_rate = (exchange_rates[snapshot["date"]]["buy"] + exchange_rates[snapshot["date"]]["sell"] )/ 2
                value_pen = value_usd * exchange_rate
                inserts.append((value_usd, value_pen, exchange_rate, snapshot["date"]))

            if inserts:
                with sqlite3.connect(cls.ETORO_DB_PATH) as connection:
                    connection.executemany("""
                        INSERT INTO h_snapshots (
                            value_usd,
                            value_pen,
                            exchange_rate,
                            snapshot_date
                        )
                        VALUES (?, ?, ?, ?)
                    """, inserts)
    