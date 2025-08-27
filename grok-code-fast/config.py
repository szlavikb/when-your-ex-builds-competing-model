"""
Configuration settings for the F1 News Dashboard application.
"""
import os


class Config:
    """Base configuration class."""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # F1 Data Service URLs
    NEWS_URLS = [
        'https://feeds.bbci.co.uk/sport/formula1/rss.xml',
        'https://www.espn.com/espn/rss/f1/news',  # May require different headers
        'https://www.skysports.com/rss/12040',
        'https://www.autosport.com/rss/feed/f1',  # Updated URL path
        'https://the-race.com/feed/',
        # Additional reliable F1 news sources
        'https://www.motorsport.com/rss/f1/news/',
        'https://www.gpblog.com/en/rss.xml',
        'https://www.planetf1.com/feed/'
    ]
    DRIVERS_URL = 'https://www.formula1.com/en/drivers.html'
    CONSTRUCTORS_URL = 'https://www.formula1.com/en/teams.html'

    # Request timeout settings
    REQUEST_TIMEOUT = 10


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'prod-secret-key-change-in-production'


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True


# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(config_name=None):
    """Get configuration class based on environment."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    return config.get(config_name, config['default'])
