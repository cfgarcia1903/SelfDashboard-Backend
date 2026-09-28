from argparse import ArgumentParser
from dotenv import load_dotenv
from flask import Flask

from backend.controllers.etoro_controller import etoro_api
from backend.config import Config
from backend.routes import main_api


def create_app(config_object=None):
    """Application factory used by Flask, tests, and local development."""
    load_dotenv()  # Load environment variables from .env file

    app = Flask(__name__)
    app.config.from_object(config_object or Config)

    app.register_blueprint(main_api)
    app.register_blueprint(etoro_api, url_prefix="/api/etoro")

    return app


if __name__ == "__main__":
    parser = ArgumentParser(description="Self Dashboard backend")
    parser.add_argument("--port", type=int, default=5001)
    args = parser.parse_args()
    create_app().run(host="127.0.0.1", port=args.port, debug=True)
