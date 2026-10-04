

from datetime import datetime
import os
import pickle
from pathlib import Path

from backend.client.bcrp_client import get_exchange_rates

class BCRPBusiness:
    BCRP_RATES_PATH = Path(os.getenv("BCRP_RATES_PATH"))

    @classmethod
    def build_exchange_rates(cls, start_date: str, end_date: str) -> None:    

        """
        Construye una lista de diccionarios con el tipo de cambio interbancario BCRP
        para un rango de fechas.

        Args:
            start_date (str): Fecha inicial en formato YYYY-MM-DD.
            end_date (str): Fecha final en formato YYYY-MM-DD.

        Returns:
            None, pero guarda los tipos de cambio en un archivo cache bcrp_rates.pickle.
        """
        try: #se actualizan las fechas faltantes hasta cubrir el rango solicitado
            with open(cls.BCRP_RATES_PATH, "rb") as f:
                original_rates = pickle.load(f)
                #tenern cuenta que las dates vienen en formato dd-mm-yyyy string

                original_start_date = min([datetime.strptime(d, "%Y-%m-%d").date() for d in original_rates.keys()])
                original_end_date = max([datetime.strptime(d, "%Y-%m-%d").date() for d in original_rates.keys()])

                change = False

                if original_start_date > datetime.strptime(start_date, "%Y-%m-%d").date():
                    # Si la fecha de inicio solicitada es anterior a la fecha mínima en el archivo,
                    # obtenemos los tipos de cambio desde la fecha solicitada hasta la fecha mínima.
                    new_rates = get_exchange_rates(start_date, original_start_date.strftime("%Y-%m-%d"))
                    original_rates.update({list(rate.keys())[0]: list(rate.values())[0] for rate in new_rates})
                    change = True
                if original_end_date < datetime.strptime(end_date, "%Y-%m-%d").date():
                    # Si la fecha de fin solicitada es posterior a la fecha máxima en el archivo,
                    # obtenemos los tipos de cambio desde la fecha máxima hasta la fecha solicitada.
                    new_rates = get_exchange_rates(original_end_date.strftime("%Y-%m-%d"), end_date)
                    original_rates.update(new_rates)
                    change = True
                # Guardar los tipos de cambio actualizados en el archivo
                if change:
                    with open(cls.BCRP_RATES_PATH, "wb") as f:
                        pickle.dump(original_rates, f)

        except FileNotFoundError:
            original_rates = get_exchange_rates(start_date, end_date)
            with open(cls.BCRP_RATES_PATH, "wb") as f:
                pickle.dump(original_rates, f)



    @classmethod
    def retrieve_exchange_rates(cls, start_date: str, end_date: str) -> dict:
        """
        Recupera los tipos de cambio interbancarios BCRP para un rango de fechas
        desde el archivo cache bcrp_rates.pickle.

        Args:
            start_date (str): Fecha inicial en formato YYYY-MM-DD.
            end_date (str): Fecha final en formato YYYY-MM-DD.

        Returns:
            dict: Diccionario con una entrada por cada día del rango:
            {
                "2025-01-20": {"buy": 3.75, "sell": 3.76},
                "2025-01-21": {"buy": 3.75, "sell": 3.76},
                ...
            }
        """
        cls.build_exchange_rates(start_date, end_date)
        with open(cls.BCRP_RATES_PATH, "rb") as f:
            rates = pickle.load(f)

        # Filtrar los tipos de cambio para el rango de fechas solicitado
        filtered_rates = {
            date: rates[date]
            for date in rates.keys()
            if datetime.strptime(start_date, "%Y-%m-%d").date() <= datetime.strptime(date, "%Y-%m-%d").date() <= datetime.strptime(end_date, "%Y-%m-%d").date()
        }

        return filtered_rates
        
