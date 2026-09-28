from flask import Blueprint


main_api = Blueprint("main_api", __name__)


@main_api.get("/health")
def health_check():
    """Return the minimum liveness response for the application."""
    return {"status": "ok"}, 200
