"""
Flask routes for the F1 News Dashboard application.
"""
from flask import render_template, jsonify
from .services import F1DataService


def create_routes(app):
    """Register all routes with the Flask app."""
    # Create F1 service with configuration
    news_urls = app.config.get('NEWS_URLS')
    drivers_url = app.config.get('DRIVERS_URL')
    constructors_url = app.config.get('CONSTRUCTORS_URL')
    timeout = app.config.get('REQUEST_TIMEOUT', 10)

    f1_service = F1DataService(
        news_urls=news_urls,
        drivers_url=drivers_url,
        constructors_url=constructors_url,
        timeout=timeout
    )

    @app.route('/')
    def index():
        """Render the main dashboard page."""
        return render_template('index.html')

    @app.route('/api/news')
    def api_news():
        """API endpoint for F1 news."""
        news = f1_service.get_f1_news()
        return jsonify([item.to_dict() for item in news])

    @app.route('/api/driver-standings')
    def api_driver_standings():
        """API endpoint for driver standings."""
        standings = f1_service.get_driver_standings()
        return jsonify([driver.to_dict() for driver in standings])

    @app.route('/api/constructor-standings')
    def api_constructor_standings():
        """API endpoint for constructor standings."""
        standings = f1_service.get_constructor_standings()
        return jsonify([constructor.to_dict() for constructor in standings])
