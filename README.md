# ⚽ Football Player Performance Analytics Dashboard

An interactive, portfolio-quality football (soccer) analytics dashboard built using **Python, Streamlit, Pandas, NumPy, and Plotly**.

Analyze player performance, compare statistics, explore interactive visualizations, and download filtered datasets through a modern football-themed dashboard.

> ⚠️ **Data Disclaimer:** All player statistics in this application are synthetic (computer-generated using `numpy.random.seed(42)`). They are intended for demonstration purposes only and do not represent real-world football results or any actual player's performance.

---

## 📁 Project Structure

```text
FOOTBALL-ANALYTICS-DASHBOARD/
│
├── app.py                  # Main Streamlit application
├── football_players.csv    # Synthetic football dataset
├── generate_data.py        # Dataset generation script
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## 🚀 Features

| Page | What you get |
|---|---|
| 📊 Overview | 5 KPI cards, Top-10 bar charts, searchable statistics table and CSV download |
| ⚽ Player Analysis | Multi-player comparison, Goals vs Assists scatter plot, Shots vs Goals scatter plot with trendline |

### Key Highlights

- Interactive football performance analytics.
- Player statistics and performance comparison.
- Dynamic charts using Plotly.
- Searchable and filterable player data.
- CSV export functionality.
- Dark football-inspired dashboard theme.
- Synthetic dataset containing 864 rows, 21 columns and 3 seasons.

---

## 🛠️ Setup & Run Locally

### Prerequisites

- Python 3.9 or higher
- pip (comes with Python)
- Git (optional, for cloning)

### 1 — Clone the repository

```bash
git clone https://github.com/atharva-07t/FOOTBALL-ANALYTICS-DASHBOARD.git

cd FOOTBALL-ANALYTICS-DASHBOARD
```

### 2 — Create a virtual environment (recommended)

```bash
python -m venv .venv
```

**Windows:**

```bash
.venv\Scripts\activate
```

**macOS / Linux:**

```bash
source .venv/bin/activate
```

### 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### 4 — (Optional) Regenerate the dataset

The CSV dataset is already included. Run this only if you want to generate a fresh copy.

```bash
python generate_data.py
```

### 5 — Launch the application

```bash
streamlit run app.py
```

The application will open in your browser:

http://localhost:8501

---

## 📦 Dependencies

| Package | Minimum Version | Purpose |
|---|---|---|
| Streamlit | 1.35.0 | Web application framework |
| Pandas | 2.1.0 | Data manipulation |
| NumPy | 1.26.0 | Numerical operations and data generation |
| Plotly | 5.22.0 | Interactive charts |

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---

## 📊 Dataset Schema

The dataset contains 864 rows, 21 columns and statistics across three seasons.

| Column | Type | Description |
|---|---|---|
| player_id | int | Unique player identifier |
| player_name | str | Synthetic player name |
| age | int | Player age (17–38) |
| nationality | str | Country |
| team | str | Club name |
| position | str | GK / DEF / MID / FWD |
| season | str | 2021-22, 2022-23, 2023-24 |
| matches_played | int | Matches played |
| minutes_played | int | Total minutes on pitch |
| goals | int | Goals scored |
| assists | int | Assists provided |
| shots | int | Total shots |
| shots_on_target | int | Shots on target |
| pass_accuracy | float | Pass completion rate (0–1) |
| key_passes | int | Passes leading to a shot |
| tackles | int | Successful tackles |
| interceptions | int | Ball interceptions |

---

## 📐 KPI & Rating Formula

All KPIs are calculated at runtime from the filtered dataset.

The player rating formula is:

```python
rating = 5.0
       + min(goals * 0.15, 2.0)
       + min(assists * 0.10, 1.5)
       + pass_accuracy * 1.50
       + min(clean_sheets * 0.10, 1.0)
       - yellow_cards * 0.05
       - red_cards * 0.20
       + noise(mu=0, sigma=0.15)

rating = clipped to [5.0, 9.5]
```

*Note: The rating formula is a demonstration metric, not an official football rating system.*

---

## 🎨 UI Theme

The dashboard uses a modern, dark football-inspired visual theme.

| Element | Value |
|---|---|
| Background | `#0d1117` |
| Surface Cards | `#1a2332` |
| Accent Green | `#00ff87` |
| Plotly Template | `plotly_dark` |

---

## ☁️ Deploy to Streamlit Community Cloud

You can deploy this dashboard online for free using Streamlit Community Cloud.

1. Push your complete project to a public GitHub repository.
2. Visit [Streamlit Community Cloud](https://share.streamlit.io/).
3. Sign in using your GitHub account.
4. Click **New app**.
5. Select your repository:
   `atharva-07t/FOOTBALL-ANALYTICS-DASHBOARD`
6. Select the `main` branch.
7. Set the main file path to `app.py`.
8. Click **Deploy**.

Your dashboard will be hosted online once deployment succeeds.

---

## 👨‍💻 Author

**Atharva Thakur**

GitHub: [@atharva-07t](https://github.com/atharva-07t)

Project Repository: [Football Analytics Dashboard](https://github.com/atharva-07t/FOOTBALL-ANALYTICS-DASHBOARD)

---

⭐ If you find this project interesting, consider giving the repository a star!

**Built with Python and a passion for football analytics.** ⚽
