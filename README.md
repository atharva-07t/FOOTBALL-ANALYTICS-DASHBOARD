# ⚽ Football Player Performance Analytics Dashboard

> **Data Disclaimer:** All player names, clubs, and statistics in this project are entirely synthetic and generated programmatically for demonstration purposes. They do not represent real players, clubs, or football results.

## Overview

An interactive football (soccer) analytics dashboard built with Python and Streamlit. Explore player performance, compare teams, and analyze statistics across positions and seasons.

## Features

- **Overview** — KPI cards (total players, goals, assists, minutes, avg rating) + Top 10 scorers
- **Player Analysis** — Goals vs Assists scatter, Shots vs Goals efficiency, multi-player comparison
- **Team Analysis** — Team goals/assists bars, player counts, radar comparison
- **Position Analysis** — Avg stats by position, rating distribution, squad composition
- **Sidebar filters** — Season, Team, Position, Player, Min. Appearances
- **Searchable stats table** with CSV download

## Tech Stack

- Python 3.9+
- Streamlit
- Pandas & NumPy
- Plotly Express & Plotly Graph Objects

## Quick Start

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd football-analytics
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app.py
```

The app opens automatically at `http://localhost:8501`

## Deploy to Streamlit Community Cloud

1. Push this project to a public GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click **New app** → select your repo → set **Main file path** to `app.py`
4. Click **Deploy** — your app is live in ~2 minutes

## Project Structure

```
football-analytics/
├── app.py                  # Main Streamlit application
├── football_players.csv    # Synthetic dataset (seed=42, reproducible)
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Regenerating the Dataset

The dataset is pre-generated and committed. To regenerate it, run:
```bash
python -c "import app; app.generate_and_save_data()"
```

## Screenshots

> Add screenshots here after first run.

## License

MIT
