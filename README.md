# JobAI — AI-Ranked Job Search

A small Flask web app that scrapes job listings from
[duunitori.fi](https://duunitori.fi) and uses **Google Gemini** to rank them
against your education and work experience. Enter a job title and a short
description of your background; get back a list of openings sorted from best
to worst match, each with a 1–10 score and a short rationale.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/framework-Flask%203.1-black)
![Gemini](https://img.shields.io/badge/AI-Gemini%202.5%20Flash-orange)

<!-- Screenshot of the app goes here, e.g.:
<p align="center">
  <img src="docs/screenshot.png" alt="JobAI search form" width="600">
</p>
-->

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Environment Variables](#environment-variables)
- [Running the App](#running-the-app)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Notes & Limitations](#notes--limitations)
- [License](#license)

## Features

- Fetches the 20 most recent job listings from the public duunitori.fi API
  for a given title.
- Sends the listings together with your background to **Gemini 2.5 Flash**
  for relevance ranking.
- Returns a structured, scored list with match reasoning and direct links to
  each posting.
- Minimal, no-JavaScript UI (one form, one results page).

## How It Works

```
┌────────────┐    job title    ┌──────────────┐    JSON     ┌───────────────┐
│  Browser   │ ──────────────▶ │   Flask app  │ ──────────▶ │ duunitori.fi  │
│ (index.html)│                 │   (app.py)   │             │  public API   │
└─────▲──────┘                 └──────┬───────┘             └───────────────┘
      │                               │ cleaned listings
      │                               ▼
      │ rendered results      ┌──────────────┐
      │ ◀──────────────────── │   Gemini     │
      │                       │ 2.5 Flash    │
      │                       └──────────────┘
```

1. The user submits `background` + `jobTitle` from `index.html`.
2. `src/scrape.py` calls the duunitori.fi `jobentries` endpoint and trims
   each result to the fields Gemini needs.
3. `src/gemini.py` sends a prompt asking the model to rank the listings
   against the user's background and return a JSON array.
4. `/results` extracts the JSON block from the model's reply and renders it
   via `results.html`. If no JSON can be parsed, it falls back to
   `noJobs.html`.

## Prerequisites

- **Python 3.10 or later**
- A **Google AI Studio** API key for Gemini — create one at
  [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
- Any random string for the Flask session secret

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/zzvllvzz/jobSearch.git
cd jobSearch
```

### 2. Create and activate a virtual environment

**Windows (PowerShell or cmd)**
```bash
py -3 -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

The app loads two values from a `.env` file in the project root (already
covered by `.gitignore`). Create it with your own values:

```ini
# .env
GEMINI_API_KEY=your-google-ai-studio-key-here
SESSION_SECRET_KEY=any-long-random-string
```

| Variable             | Purpose                                                   |
|----------------------|-----------------------------------------------------------|
| `GEMINI_API_KEY`     | Authenticates calls to the Gemini API.                    |
| `SESSION_SECRET_KEY` | Signs Flask's session cookie used to pass results between `/` and `/results`. |

## Running the App

With the virtual environment active and `.env` populated:

```bash
flask run
```

Then open **http://127.0.0.1:5000/** in your browser.

## Usage

1. In the **Your Background** field, describe your education, skills, and
   work experience — a sentence or two is enough.
2. In the **Job Title to Search** field, enter a single job title
   (e.g. `embedded engineer`, `junior python developer`).
3. Submit the form. A loading overlay appears while the app scrapes
   listings and waits for Gemini.
4. The results page shows the listings sorted from best to worst match,
   each with a score, rationale, and a direct link.

> Only one job title per search. The app searches both the title and the
> description fields on duunitori.fi (`search_also_descr=1`).

## Project Structure

```
jobSearch/
├── app.py              Flask app, routes, session handling
├── src/
│   ├── scrape.py       duunitori.fi API call + result cleanup
│   └── gemini.py       Gemini prompt + API call
├── templates/
│   ├── index.html          Search form
│   ├── results.html        Ranked match list
│   ├── noJobs.html         Fallback when no JSON could be parsed
│   ├── pageNotFound.html   404 handler
│   └── somethingWrong.html Generic error page
├── static/
│   ├── style.css
│   └── favicon.ico
├── requirements.txt
├── .gitignore
└── README.md
```

## Notes & Limitations

- **Finnish market only.** duunitori.fi is a Finnish job-listings site, so
  results are overwhelmingly for positions in Finland.
- **Listings volume.** The duunitori.fi API returns the most recent jobs
  matching the search; the app passes the first page of results to Gemini.
- **JSON extraction is regex-based.** The results page extracts the JSON
  array from Gemini's free-text reply with a regex. If Gemini wraps the
  response in unexpected text or formatting, the parser falls through to
  `noJobs.html` rather than crashing.
- **Single title per search.** Multi-title queries are not supported; run
  separate searches for each title.

## License

Released under the [MIT License](LICENSE).
