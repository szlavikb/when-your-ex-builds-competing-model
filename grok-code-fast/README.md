# F1 News Dashboard

A dynamic and stylish web application for collecting and displaying the latest Formula 1 news, built with a modern object-oriented architecture.

## Features

- **Multiple News Sources**: Aggregates F1 news from BBC, ESPN, Sky Sports, Autosport, and The Race
- **Real-time Standings**: Driver and constructor standings with fallback data
- **Modern, responsive UI** with Bootstrap styling
- **Dynamic content loading** with JavaScript
- **Auto-refresh functionality** (news every 5 minutes)
- **Source attribution** for news articles
- **Robust error handling** with fallback data
- **Gradient backgrounds and smooth animations**
- **Object-oriented architecture** with modular design

## Requirements

- Python 3.7+
- Flask
- requests
- beautifulsoup4

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python run.py
```

Open your browser and navigate to `http://localhost:5000`

## Project Structure

```
grok-code-fast/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Data models (NewsItem, Driver, Constructor)
│   ├── services.py          # Business logic (F1DataService)
│   ├── routes.py            # Flask routes
│   ├── static/
│   │   ├── script.js        # JavaScript for dynamic content
│   │   └── style.css        # Custom CSS styles
│   └── templates/
│       └── index.html       # Main HTML template
├── config.py                # Configuration settings
├── run.py                   # Entry point
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Architecture

The application follows a modular, object-oriented design:

- **Models** (`app/models.py`): Define data structures for F1 data
- **Services** (`app/services.py`): Handle business logic for fetching data
- **Routes** (`app/routes.py`): Define Flask endpoints
- **Configuration** (`config.py`): Centralized configuration management
- **App Factory** (`app/__init__.py`): Create and configure the Flask app

## API

- `/` - Main dashboard page
- `/api/news` - JSON endpoint for news data
- `/api/driver-standings` - JSON endpoint for driver standings
- `/api/constructor-standings` - JSON endpoint for constructor standings
