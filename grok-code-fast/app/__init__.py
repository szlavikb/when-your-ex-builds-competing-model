"""
Flask application factory for F1 News Dashboard.
"""
from flask import Flask
from .routes import create_routes


def create_app(config_class=None):
    """
    Application factory function.

    Args:
        config_class: Configuration class to use (optional)

    Returns:
        Flask application instance
    """
    app = Flask(__name__)

    # Load configuration
    if config_class:
        app.config.from_object(config_class)
    else:
        # Load default development config
        from ..config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)

    # Register routes
    create_routes(app)

    return app
