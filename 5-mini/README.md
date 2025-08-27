F1 Live — News & Standings (Flask)

Quick start (Windows, cmd.exe):

1. Create a virtual environment (recommended):

```
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Run the app:

```
python app.py
```

4. Open http://127.0.0.1:5000 in your browser.

Notes:
- News is aggregated from public RSS feeds; standings come from the Ergast API.
- The app caches requests for 2 minutes to avoid rate limits.
- To add more feeds, edit `FEEDS` in `app.py`.

Project layout (maintainable OOP structure):

```
./
	app.py                # thin entrypoint
	f1_app/               # package
		__init__.py
		cache.py            # SimpleCache class
		aggregator.py       # FeedAggregator class
		standings.py        # StandingsFetcher class
		server.py           # Flask app factory and wiring
	templates/
		index.html
	static/
		style.css
```
