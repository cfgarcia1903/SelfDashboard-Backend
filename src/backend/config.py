import os


class Config:
    """Base configuration shared by local development and tests."""

    JSON_SORT_KEYS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")


class TestingConfig(Config):
    TESTING = True


class DevelopmentConfig(Config):
    DEBUG = True