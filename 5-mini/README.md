
# 🏁 F1 Live — News & Standings (Flask)

> **A vibrant, real-time dashboard for Formula 1 fans!**

---

## 🚀 Quick Start

1. **Create a virtual environment:**
	```sh
	python -m venv .venv
	.venv\Scripts\activate
	```
2. **Install dependencies:**
	```sh
	pip install -r requirements.txt
	```
3. **Run the app:**
	```sh
	python app.py
	```
4. **Open** [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## ✨ Features

- **Live F1 News**: Aggregates the latest headlines from public RSS feeds.
- **Current Standings**: Fetches up-to-date driver & constructor standings from the Ergast API.
- **Smart Caching**: All requests are cached for 2 minutes to avoid rate limits and speed up the UI.
- **Easy Feed Expansion**: Add more news sources by editing the `FEEDS` list in `app.py`.
- **Clean OOP Design**: Modular, maintainable codebase with clear separation of concerns.
- **Minimal UI**: Simple, readable, and mobile-friendly interface.

---

## 🗂️ Project Structure

```text
5-mini/
├── app.py              # Thin entrypoint
├── requirements.txt    # Dependencies
├── data/
│   ├── sample_news.json
│   └── sample_standings.json
├── f1_app/
│   ├── __init__.py
│   ├── aggregator.py   # FeedAggregator class
│   ├── cache.py        # SimpleCache class
│   ├── server.py       # Flask app factory and wiring
│   └── standings.py    # StandingsFetcher class
├── scripts/
│   └── test_fetch.py
├── static/
│   └── style.css
└── templates/
	 └── index.html
```

---

## 🛠️ Technical Highlights

- **Flask**-based microservice
- **OOP**: Each core function (aggregation, caching, standings) is a dedicated class
- **Extensible**: Add new feeds or APIs with minimal code changes
- **Caching**: In-memory, time-based cache for efficiency

---

## 📢 Notes
- News is aggregated from public RSS feeds; standings come from the Ergast API.
- To add more feeds, edit `FEEDS` in `app.py`.
- The app caches requests for 2 minutes to avoid rate limits.

---

## 🎨 Style
- Minimalist, readable, and responsive UI
- Custom CSS for a clean look

---

## 📄 License
MIT

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
