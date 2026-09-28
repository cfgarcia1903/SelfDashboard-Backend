from backend.app import create_app
from backend.config import TestingConfig


def test_app_factory_exposes_health_check():
    app = create_app(TestingConfig)
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_domain_routes_are_explicitly_not_implemented():
    app = create_app(TestingConfig)
    client = app.test_client()

    response = client.get("/api/etoro/portfolios/1")

    assert response.status_code == 501