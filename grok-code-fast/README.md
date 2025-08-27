# F1 News Dashboard

A dynamic and stylish web application for collecting and displaying the latest Formula 1 news, built with a modern object-oriented architecture.

## Features


## Requirements


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
## 🏎️ F1 News Dashboard (Grok Code Fast)

> **A visually stunning, real-time Formula 1 news and standings portal!**

---

## 🚦 Features

- **Multi-source News**: Aggregates F1 news from BBC, ESPN, Sky Sports, Autosport, and The Race
- **Live Standings**: Driver & constructor tables with fallback data
- **Modern UI**: Responsive, Bootstrap-powered, with gradients and smooth animations
- **Dynamic Content**: JavaScript-driven, auto-refreshes news every 5 minutes
- **Source Attribution**: Every article is clearly credited
- **Robust Error Handling**: Fallbacks for missing data
- **OOP Architecture**: Modular, maintainable, and extensible

---

## 🛠️ Technical Solution

- **Flask** backend with a clean, object-oriented structure
- **Service Layer**: Handles news aggregation, parsing, and standings
- **Bootstrap & Custom CSS**: For a sleek, modern look
- **JavaScript**: For dynamic updates and smooth UX
- **BeautifulSoup**: For robust HTML parsing
- **Fallback Data**: Ensures the dashboard is never empty

---

## 🗂️ Project Structure

```text
grok-code-fast/
├── run.py              # Entrypoint
├── requirements.txt    # Dependencies
├── config.py           # App config
├── app/
│   ├── __init__.py
│   ├── models.py       # Data models
│   ├── routes.py       # Flask routes
│   ├── services.py     # News & standings logic
│   ├── static/
│   │   ├── script.js
│   │   └── style.css
│   └── templates/
│       └── index.html
├── test_app.py         # Tests
└── ...
```

---

## ⚡ Quick Start

1. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
2. **Run the app:**
   ```sh
   python run.py
   ```
3. **Open** [http://localhost:5000](http://localhost:5000) in your browser.

---

## 🎨 Style
- Responsive, mobile-friendly, and visually engaging
- Custom gradients, smooth transitions, and Bootstrap components

---

## 📄 License
MIT

- `/` - Main dashboard page
- `/api/news` - JSON endpoint for news data
- `/api/driver-standings` - JSON endpoint for driver standings
- `/api/constructor-standings` - JSON endpoint for constructor standings
