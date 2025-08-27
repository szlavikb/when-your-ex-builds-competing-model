# 🏁 UI Comparison: 5-mini vs grok-code-fast

<div align="center">
	<img src="https://img.shields.io/badge/F1-News-red?style=for-the-badge&logo=formula1" alt="F1 News"/>
	<img src="https://img.shields.io/badge/Comparison-UI-blueviolet?style=for-the-badge" alt="UI Comparison"/>
</div>

# 🏆 F1 News & Standings — Project Overview

Welcome to the ultimate Formula 1 dashboard repository! This project contains two unique, stylish, and technically robust F1 news and standings web apps:

- [5-mini](./5-mini/README.md) — Minimalist, OOP Flask app for live news and standings
- [grok-code-fast](./grok-code-fast/README.md) — Modern, visually rich dashboard with advanced features

---

## 📂 Project Structure

```
when-your-ex-builds-competing-model/
├── 5-mini/           # Minimalist F1 Flask app
├── grok-code-fast/   # Modern, feature-rich F1 dashboard
├── comparison.md     # Project comparison notes
├── index.html        # Sample HTML demo for GitHub Pages
└── .gitignore        # Git exclusions
```

---

## 🚦 Quick Links

- [5-mini Technical README](./5-mini/README.md)
- [grok-code-fast Technical README](./grok-code-fast/README.md)
- [🌐 HTML Demo (see below for setup)](https://szlavikb.github.io/when-your-ex-builds-competing-model/)

---

## ✨ About

Both apps are built with Python and Flask, but each takes a different approach to architecture, UI, and feature set. Explore each subproject for detailed technical documentation, setup instructions, and code.

---

## 🎯 Task Given to Both Models

<details>
<summary><strong>Prompt</strong></summary>

> <span style="color:#e67e22"><b>"Create a web UI which is stylish and dynamic and include the F1 news and the current standings in Python."</b></span>

</details>

---

## ✨ Results & Detailed Comparison

| 🚦 <span style="color:#e67e22">Feature/Aspect</span> | 🏎️ <span style="color:#2980b9">5-mini</span> | 🏆 <span style="color:#27ae60">grok-code-fast</span> |
|:----------------------|:-----------------------------------------------------------------------|:-------------------------------------------------------------------------------|
| **Backend**           | Flask (Python)                                                         | Flask (Python)                                                                 |
| **Frontend**          | HTML (Jinja2), Custom CSS                                              | HTML (Jinja2), <span style="color:#7952b3">Bootstrap 5</span> (CDN), <span style="color:#f39c12">JS</span> |
| **UI Frameworks**     | None                                                                   | Bootstrap 5, Font Awesome                                                      |
| **Data Source**       | Local JSON files (`data/sample_news.json`, `data/sample_standings.json`)| Models/services in `app/`                                                      |
| **Main Structure**    | `app.py`, `f1_app/`, `templates/index.html`                            | `run.py`, `app/` (models, routes, services), `app/templates/index.html`         |
| **Header**            | Simple brand and refresh button                                        | Modern, dark background, icon, subtitle                                        |
| **Navigation**        | Direct, no tabs                                                        | Tabbed navigation (News, Drivers, Constructors)                                |
| **News Section**      | List, error/empty state handling                                       | Tab with Bootstrap cards/components, icons, responsive                         |
| **Standings Section** | Drivers/Constructors, error/empty state handling                       | Tabs for Drivers/Constructors, tables/lists, icons, responsive                 |
| **Styling**           | Minimal, custom CSS                                                    | Bootstrap 5, Font Awesome, custom CSS                                          |
| **Responsiveness**    | Basic                                                                  | Mobile-friendly, responsive                                                    |
| **Functionality**     | Fetches/caches news & standings, simple navigation                     | Interactive, clear separation via tabs, visually appealing                     |

---

## 📝 Summary & Recommendation

- <span style="color:#27ae60"><b>grok-code-fast</b></span> provides a more modern, user-friendly, and visually appealing UI. The use of <span style="color:#7952b3">Bootstrap</span> and <span style="color:#f39c12">JS</span> makes it highly recommendable for most users.
- <span style="color:#2980b9"><b>5-mini</b></span> is functional and clear but lacks the polish and usability enhancements of a modern UI framework. It is best suited for simple, minimalistic needs.

<div align="center">
<b>🏆 Overall, <span style="color:#27ae60">grok-code-fast</span> is the better and more understandable UI for most users.</b>
</div>
