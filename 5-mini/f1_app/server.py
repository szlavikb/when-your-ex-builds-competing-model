import logging
from flask import Flask, render_template, jsonify
from .cache import SimpleCache
from .aggregator import FeedAggregator
from .standings import StandingsFetcher
import json
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('f1_app')


def create_app(feeds=None):
    app = Flask(__name__, static_folder='static', template_folder='templates')
    cache = SimpleCache(ttl=120)
    if feeds is None:
        feeds = [
            'https://www.planetf1.com/feed/',
            'https://www.autosport.com/feed/',
            'https://www.motorsport.com/rss/all/',
        ]
    aggregator = FeedAggregator(feeds)
    standings = StandingsFetcher()

    @app.route('/')
    def index():
        logger.info('Rendering index')
        return render_template('index.html')

    @app.route('/api/news')
    def api_news():
        logger.info('Request /api/news')
        data = cache.get_or_load('news', aggregator.fetch)
        meta = {
            'last_fetch': getattr(aggregator, 'last_fetch', None),
            'last_error': getattr(aggregator, 'last_error', None),
        }
        # if live fetch returned nothing, attempt to load sample data
        if not data:
            try:
                sample_path = os.path.join(os.getcwd(), 'data', 'sample_news.json')
                with open(sample_path, 'r', encoding='utf-8') as f:
                    sample = json.load(f)
                return jsonify({'items': sample.get('items', []), 'meta': {**meta, 'sample_used': True}})
            except Exception:
                pass
        return jsonify({'items': data, 'meta': meta})

    @app.route('/api/standings')
    def api_standings():
        logger.info('Request /api/standings')
        data = cache.get_or_load('standings', standings.fetch)
        meta = {
            'last_fetch': getattr(standings, 'last_fetch', None),
            'last_error': getattr(standings, 'last_error', None),
        }
        if (not data) or (not data.get('drivers') and not data.get('constructors')):
            try:
                sample_path = os.path.join(os.getcwd(), 'data', 'sample_standings.json')
                with open(sample_path, 'r', encoding='utf-8') as f:
                    sample = json.load(f)
                return jsonify({'data': sample, 'meta': {**meta, 'sample_used': True}})
            except Exception:
                pass
        return jsonify({'data': data, 'meta': meta})

    @app.route('/debug/log')
    def debug_log():
        log_path = os.path.join(os.getcwd(), 'logs', 'debug.log')
        if not os.path.exists(log_path):
            return jsonify({'log': '', 'note': 'no log file'}), 200
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                content = f.read()
            # return last 1000 chars
            return jsonify({'log_tail': content[-1000:], 'note': 'tail of debug.log'}), 200
        except Exception as e:
            return jsonify({'log': '', 'error': str(e)}), 500

    return app


app = create_app()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
