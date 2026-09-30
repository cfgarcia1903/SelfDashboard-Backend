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