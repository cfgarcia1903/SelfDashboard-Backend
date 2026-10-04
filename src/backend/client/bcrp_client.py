import requests
from datetime import datetime, timedelta


def get_exchange_rates(start_date, end_date) -> dict:
    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.strptime(end_date, "%Y-%m-%d").date()

    query_start = start - timedelta(days=7)

    url = (
        "https://estadisticas.bcrp.gob.pe/estadisticas/series/api/"
        f"PD04639PD-PD04640PD/json/{query_start}/{end}"
    )

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    months = {
        "Ene": 1, "Feb": 2, "Mar": 3, "Abr": 4,
        "May": 5, "Jun": 6, "Jul": 7, "Ago": 8,
        "Set": 9, "Oct": 10, "Nov": 11, "Dic": 12,
    }

    rates = {}

    for period in response.json()["periods"]:
        day, month, year = period["name"].split(".")
        buy, sell = period["values"]

        if buy == "n.d." or sell == "n.d.":
            continue

        date = datetime(
            2000 + int(year),
            months[month],
            int(day),
        ).date()

        rates[date] = {
            "buy": float(buy),
            "sell": float(sell),
        }

    # Obtener el último valor disponible antes o en el inicio del rango.
    previous_rates = {
        date: rate
        for date, rate in rates.items()
        if date <= start
    }

    last_valid_rate = (
        previous_rates[max(previous_rates)]
        if previous_rates
        else None
    )

    result = {}
    current_date = start

    while current_date <= end:
        if current_date in rates:
            last_valid_rate = rates[current_date]

        if last_valid_rate is not None:
            result[current_date.strftime("%Y-%m-%d")] = last_valid_rate.copy()

        current_date += timedelta(days=1)

    return result