from backend.schemas.data_schemas import EtoroDeposits, EtoroDeposit
import os
from pathlib import Path
import sqlite3


class EtoroDAO:
    ETORO_DB_PATH = Path(os.getenv("ETORO_DB_PATH"))
    

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
    def get_total_deposits(cls) -> float:
        deposits = cls.query_deposits()
        total = sum([deposit.amount for deposit in deposits.deposits])
        return total