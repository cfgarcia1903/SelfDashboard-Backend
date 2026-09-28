import os

def get_etoro_credentials(user: dict):
    return {"public": os.getenv("ETORO_PUBLIC_KEY"),
            "private": os.getenv("ETORO_PRIVATE_KEY")}
