# =============================================================================
# PITCHVISION — Football Intelligence Platform
# app.py  |  Streamlit + Plotly
# All data is synthetic. See README.md for details.
# =============================================================================

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ── Path resolution ──────────────────────────���────────────────────────────────
_HERE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(_HERE, "football_players.csv")

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PITCHVISION | Football Intelligence",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Design tokens ─────────────────────────────────────────────────────────────
BG_PRIMARY   = "#080D14"
BG_SECONDARY = "#101923"
BG_CARD      = "#141F2B"
BG_CARD_EL   = "#1A2835"
ACCENT_G     = "#00E6A0"
ACCENT_B     = "#39BDF8"
TEXT_P       = "#F4F7FA"
TEXT_S       = "#91A0AE"
BORDER       = "#263442"
WARN         = "#FFB547"
DANGER       = "#FF5C6C"

POS_COLORS = {"GK": "#39BDF8", "DEF": "#00E6A0", "MID": "#FFB547", "FWD": "#FF5C6C"}
POSITIONS  = ["GK", "DEF", "MID", "FWD"]
TEAMS      = [
    "FC Ironforge", "Redstone United", "Blackwater City", "Silverpeak FC",
    "Goldcrest Athletic", "Northvale FC", "Eastbridge Town", "Westholm Rovers",
]
SEASONS    = ["2022-23", "2023-24"]

REQUIRED_COLUMNS = [
    "player_id", "player_name", "team", "season", "position", "age", "appearances",
    "minutes_played", "goals", "assists", "shots", "shots_on_target", "pass_accuracy",
    "tackles", "yellow_cards", "red_cards", "clean_sheets", "rating",
]

PLAYER_NAMES = [
    "Marco Delvecchio","Luis Carvalho","Antoine Moreau","Kai Hoffmann","Jamal Osei",
    "Rafael Mendoza","Tomás Novák","Pierre Lecomte","Yusuf Adeyemi","Sven Lindqvist",
    "Carlos Ruíz","Dimitri Papadopoulos","Niko Braun","Emeka Okonkwo","Felipe Souza",
    "Aleksei Volkov","Hamid Rahimi","Lorenzo Mancini","Kwame Asante","Bogdan Petrescu",
    "Anders Eriksen","Mateus Ferreira","Christoph Bauer","Ibrahima Diallo","Renato Greco",
    "Vladislav Kozlov","Omar Farouk","Luca Bianchi","Sébastien Blanc","Arjun Nair",
    "Thiago Alves","Patrick Oduya","Mikael Strand","Georgi Petrov","Callum Fraser",
    "Enzo Martinelli","Davi Barbosa","Rustam Nazarov","Jean-Claude Mbeki","Hiroshi Tanaka",
    "Rodrigo Vega","Florian Huber","Samuel Owusu","Nikolaj Christensen","Arnav Sharma",
    "Matteo Russo","Cédric Fontaine","Oluwaseun Abiodun","Dragos Ionescu","Pavel Horáček",
    "Erling Dahl","Giovanni Vitale","Alexei Morozov","Kweku Mensah","Álvaro Prieto",
    "Fabian Wenzel","Bouba Traoré","Riku Mäkinen","Leandro Figueiredo","Hassan Al-Rashid",
    "Tomáš Kratochvíl","Javier Morales","Desmond Acheampong","Nils Bergström","Romain Gillet",
    "Sulley Muntari","Petar Živković","Davide Colombo","Yannick Essien","Anton Kuznetsov",
    "Bruno Carvalho","Zlatan Perić","Marcus Osei","Frederik Moldt","Amadou Coulibaly",
    "Rahul Verma","Stéphane Lefebvre","Viktor Horváth","Chukwuemeka Obi","Iker Alonso",
    "Nuno Teixeira","Lasse Kjær","Mohammad Hossein","Gianluca Serra","Kofi Agyemang",
    "Søren Nygaard","Dmytro Kovalenko","Enrique Castro","Lionel Dupont","Sekou Camara",
    "Thorsten Kiefer","Andrei Popescu","Marko Nikolić","Thibault Renard","Femi Adeyinka",
    "Jae-won Oh","Lukas Voss","Hamza Benali","Daniil Sorokin","Olaf Magnusson",
    "Ricardo Pires","Cedric Osei","Vlad Georgescu","Simon Larsson","Alejandro Fuentes",
    "Nasser Al-Khatib","Stephan Gruber","Emmanuel Okafor","Ondrej Blaha","Yohannes Tekeste",
    "Marco van Dijk","Jules Rousseau","Abiodun Olawale","Kasper Thygesen","Olusegun Bello",
    "Ercan Yildiz","Maxim Bondarenko","Diego Herrera","Fabio Montagna","Kwabena Boateng",
]

# =============================================================================
# GLOBAL CSS — PITCHVISION Design System
# =============================================================================
def inject_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Manrope:wght@400;500;600;700;800&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Inter', 'Manrope', sans-serif !important;
}

/* ── App background ── */
.stApp {
    background-color: #080D14 !important;
    background-image:
        radial-gradient(ellipse at 10% 15%, rgba(0,230,160,0.055) 0%, transparent 50%),
        radial-gradient(ellipse at 90% 80%, rgba(57,189,248,0.045) 0%, transparent 50%);
    background-attachment: fixed;
    color: #F4F7FA !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer { visibility: hidden; }

/* Do NOT touch header[data-testid="stHeader"] at all —
   the native sidebar collapse/expand button lives there and must stay intact */

.stDeployButton                         { display: none !important; }
[data-testid="stToolbar"]               { display: none !important; }
[data-testid="stDecoration"]            { display: none !important; }
[data-testid="stStatusWidget"]          { display: none !important; }

/* ── Kill Streamlit's default top padding on main ── */
.main > div:first-child { padding-top: 0 !important; }
section.main > div { padding-top: 0 !important; }
div[class*="appview-container"] { padding-top: 0 !important; }

/* ── Main content padding ── */
.main .block-container {
    padding: 1rem 2rem 3rem 2rem !important;
    max-width: 1440px !important;
    margin-top: 0 !important;
}

/* ────────────────────────────────────────────────
   SIDEBAR
──────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0C1520 0%, #101923 60%, #0C1520 100%) !important;
    border-right: 1px solid #263442 !important;
    min-width: 260px !important;
}

/* ── Sidebar collapse/expand toggle button ──────────────────────────
   Streamlit renders this button in TWO places:
   1. INSIDE the open sidebar (to close it)   → data-testid="stSidebarCollapseButton"
   2. OUTSIDE as a fixed overlay (to re-open) → same test-id but outside stSidebar

   We force BOTH to always be visible.
── */
[data-testid="stSidebarCollapseButton"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    z-index: 999999 !important;
}
[data-testid="stSidebarCollapseButton"] button {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    background: #141F2B !important;
    border: 1px solid #3a5068 !important;
    border-radius: 8px !important;
    width: 2.25rem !important;
    height: 2.25rem !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 0 !important;
    cursor: pointer !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.6) !important;
    transition: border-color 0.2s, background 0.2s !important;
}
[data-testid="stSidebarCollapseButton"] button:hover {
    background: rgba(0,230,160,0.1) !important;
    border-color: #00E6A0 !important;
}
[data-testid="stSidebarCollapseButton"] svg {
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
    fill: #00E6A0 !important;
    stroke: #00E6A0 !important;
    width: 1.1rem !important;
    height: 1.1rem !important;
}

/* ── Hide ONLY the radio group "nav" label — not all widget labels ── */
[data-testid="stSidebar"] [data-testid="stRadio"] > label {
    display: none !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}
/* Hide stWidgetLabel only when it is the direct child of the radio wrapper */
[data-testid="stSidebar"] [data-testid="stRadio"] [data-testid="stWidgetLabel"] {
    display: none !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* sidebar brand block */
.pv-brand {
    background: linear-gradient(160deg, #0D1E2C 0%, #111E2B 100%);
    border-bottom: 1px solid #1E3040;
    padding: 22px 20px 18px;
    margin-top: 0;
    margin-bottom: 4px;
}
.pv-logo {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 6px;
}
.pv-logo-icon {
    width: 38px; height: 38px;
    background: linear-gradient(145deg, #0A6B4A 0%, #00E6A0 100%);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
    box-shadow: 0 2px 12px rgba(0,230,160,0.25);
}
.pv-app-name {
    font-family: 'Manrope', sans-serif !important;
    font-size: 1.2rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    color: #F4F7FA;
    text-transform: uppercase;
    line-height: 1;
}
.pv-app-sub {
    font-size: 0.65rem;
    color: #4E6478;
    letter-spacing: 0.08em;
    margin-top: 4px;
    text-transform: uppercase;
    font-weight: 500;
}
.pv-synth-tag {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: rgba(0,230,160,0.07);
    border: 1px solid rgba(0,230,160,0.2);
    border-radius: 6px;
    padding: 4px 10px;
    font-size: 0.63rem;
    color: #00E6A0;
    font-weight: 600;
    letter-spacing: 0.06em;
    margin-top: 10px;
}

/* sidebar section header */
.pv-sidebar-section {
    font-size: 0.65rem;
    font-weight: 700;
    color: #4A6070;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 16px 20px 8px;
    border-top: 1px solid rgba(38,52,66,0.5);
    margin-top: 4px;
}

/* ── NAV RADIO — full visibility rewrite ── */

/* Container: vertical stack with tight gap */
[data-testid="stSidebar"] [data-testid="stRadio"] > div {
    display: flex !important;
    flex-direction: column !important;
    gap: 3px !important;
    padding: 0 10px !important;
}

/* Each radio wrapper — make it block and styled */
[data-testid="stSidebar"] [data-testid="stRadio"] [data-baseweb="radio"] {
    display: flex !important;
    align-items: center !important;
    padding: 10px 14px !important;
    border-radius: 10px !important;
    border: 1px solid transparent !important;
    cursor: pointer !important;
    transition: background 0.18s ease, border-color 0.18s ease !important;
    background: transparent !important;
    width: 100% !important;
}

/* Hover state on the whole row */
[data-testid="stSidebar"] [data-testid="stRadio"] [data-baseweb="radio"]:hover {
    background: rgba(0,230,160,0.08) !important;
    border-color: rgba(0,230,160,0.2) !important;
}

/* Hide the actual radio dot circle */
[data-testid="stSidebar"] [data-testid="stRadio"] [data-baseweb="radio"] > div:first-child {
    display: none !important;
}

/* The text label — HIGH CONTRAST, always visible */
[data-testid="stSidebar"] [data-testid="stRadio"] [data-baseweb="radio"] > div:last-child,
[data-testid="stSidebar"] [data-testid="stRadio"] [data-baseweb="radio"] span,
[data-testid="stSidebar"] [data-testid="stRadio"] [data-baseweb="radio"] p,
[data-testid="stSidebar"] [data-testid="stRadio"] label span {
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    color: #C8D6E0 !important;
    letter-spacing: 0.01em !important;
    line-height: 1.4 !important;
}

/* Selected state — full row highlight */
[data-testid="stSidebar"] [data-testid="stRadio"] [data-baseweb="radio"][aria-checked="true"] {
    background: rgba(0,230,160,0.12) !important;
    border-color: rgba(0,230,160,0.3) !important;
}

/* Selected text — bright green */
[data-testid="stSidebar"] [data-testid="stRadio"] [data-baseweb="radio"][aria-checked="true"] > div:last-child,
[data-testid="stSidebar"] [data-testid="stRadio"] [data-baseweb="radio"][aria-checked="true"] span,
[data-testid="stSidebar"] [data-testid="stRadio"] [data-baseweb="radio"][aria-checked="true"] p {
    color: #00E6A0 !important;
    font-weight: 600 !important;
}

/* Legacy label selector fallback (older Streamlit builds) */
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    display: flex !important;
    align-items: center !important;
    padding: 10px 14px !important;
    border-radius: 10px !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    color: #C8D6E0 !important;
    cursor: pointer !important;
    transition: all 0.18s ease !important;
    border: 1px solid transparent !important;
    width: 100% !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: rgba(0,230,160,0.08) !important;
    color: #00E6A0 !important;
    border-color: rgba(0,230,160,0.2) !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label > div,
[data-testid="stSidebar"] [data-testid="stRadio"] label > span {
    color: inherit !important;
    font-weight: inherit !important;
}

/* sidebar divider */
.pv-divider {
    height: 1px;
    background: #263442;
    margin: 10px 20px;
}

/* sidebar filter labels — visible, styled */
[data-testid="stSidebar"] label {
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    color: #7A90A0 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}
/* Make sure filter widget labels are shown */
[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-testid="stWidgetLabel"],
[data-testid="stSidebar"] [data-testid="stMultiSelect"] [data-testid="stWidgetLabel"],
[data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stWidgetLabel"] {
    display: flex !important;
    visibility: visible !important;
    height: auto !important;
    margin: 0 !important;
    padding: 8px 0 4px 0 !important;
}

/* sidebar select/multiselect */
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #141F2B !important;
    border: 1px solid #263442 !important;
    border-radius: 10px !important;
    color: #F4F7FA !important;
    font-size: 0.84rem !important;
    transition: border-color 0.2s !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] > div:focus-within {
    border-color: #00E6A0 !important;
    box-shadow: 0 0 0 3px rgba(0,230,160,0.1) !important;
}
/* multiselect tags */
[data-testid="stSidebar"] span[data-baseweb="tag"] {
    background: rgba(0,230,160,0.12) !important;
    border: 1px solid rgba(0,230,160,0.3) !important;
    border-radius: 6px !important;
    color: #00E6A0 !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
}

/* sidebar slider */
[data-testid="stSidebar"] [data-baseweb="slider"] [role="slider"] {
    background: #00E6A0 !important;
    border-color: #00E6A0 !important;
}
[data-testid="stSidebar"] [data-baseweb="slider"] div[data-testid="stSliderTrackFill"] {
    background: linear-gradient(90deg, #0A6B4A, #00E6A0) !important;
}

/* sidebar footer */
.pv-sidebar-footer {
    font-size: 0.65rem;
    color: #263442;
    text-align: center;
    padding: 12px 20px 20px;
    border-top: 1px solid #1A2835;
    margin-top: 16px;
    letter-spacing: 0.04em;
}
.pv-sidebar-footer span { color: #39BDF8; }

/* ── Clear filters button ── */
[data-testid="stSidebar"] [data-testid="stButton"] > button {
    width: 100%;
    background: rgba(255,92,108,0.08) !important;
    border: 1px solid rgba(255,92,108,0.25) !important;
    border-radius: 10px !important;
    color: #FF5C6C !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    padding: 7px 16px !important;
    letter-spacing: 0.04em !important;
    transition: all 0.2s !important;
}
[data-testid="stSidebar"] [data-testid="stButton"] > button:hover {
    background: rgba(255,92,108,0.15) !important;
    border-color: rgba(255,92,108,0.45) !important;
}

/* ────────────────────────────────────────────────
   TOP HEADER
──────────────────────────────────────────────── */
.pv-header {
    background: linear-gradient(135deg, #0D1D2B 0%, #121E2C 50%, #0D1D2B 100%);
    border: 1px solid #1E3040;
    border-radius: 16px;
    padding: 18px 24px;
    margin: 0 0 16px 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    position: relative;
    overflow: hidden;
}
.pv-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(ellipse at 0% 50%, rgba(0,230,160,0.04) 0%, transparent 60%);
    pointer-events: none;
}
.pv-header::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #00E6A0 0%, #39BDF8 50%, transparent 100%);
    opacity: 0.5;
}
.pv-header-left { flex: 1; min-width: 0; }
.pv-header-eyebrow {
    font-size: 0.62rem;
    font-weight: 700;
    color: #00E6A0;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 8px;
    opacity: 0.85;
}
.pv-header-title {
    font-family: 'Manrope', sans-serif;
    font-size: 1.35rem;
    font-weight: 800;
    color: #F4F7FA;
    letter-spacing: -0.02em;
    line-height: 1.15;
    margin-bottom: 5px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.pv-header-subtitle {
    font-size: 0.78rem;
    color: #4E6478;
    font-weight: 400;
    line-height: 1.5;
    max-width: 420px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.pv-header-badges {
    display: flex;
    gap: 7px;
    flex-wrap: wrap;
    justify-content: flex-end;
    align-items: center;
    flex-shrink: 0;
}
.pv-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 11px;
    border-radius: 8px;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.03em;
    white-space: nowrap;
}
.pv-badge-green {
    background: rgba(0,230,160,0.08);
    border: 1px solid rgba(0,230,160,0.22);
    color: #00E6A0;
}
.pv-badge-blue {
    background: rgba(57,189,248,0.08);
    border: 1px solid rgba(57,189,248,0.22);
    color: #39BDF8;
}
.pv-badge-warn {
    background: rgba(0,230,160,0.06);
    border: 1px solid rgba(0,230,160,0.18);
    color: #5EC9A0;
}
.pv-badge-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: currentColor;
    flex-shrink: 0;
}

/* ────────────────────────────────────────────────
   PAGE SECTION HEADER
──────────────────────────────────────────────── */
.pv-section-header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin: 16px 0 14px;
    padding-bottom: 12px;
    border-bottom: 1px solid rgba(38,52,66,0.7);
}
.pv-section-icon {
    width: 32px; height: 32px;
    background: rgba(0,230,160,0.1);
    border: 1px solid rgba(0,230,160,0.2);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px;
    flex-shrink: 0;
    line-height: 1;
}
.pv-section-title {
    font-family: 'Manrope', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #E8F0F4;
    letter-spacing: -0.01em;
}
.pv-section-sub {
    font-size: 0.72rem;
    color: #4E6478;
    font-weight: 400;
    margin-top: 2px;
}

/* ────────────────────────────────────────────────
   KPI CARDS
──────────────────────────────────────────────── */
.kpi-card {
    background: linear-gradient(160deg, #121D29 0%, #172030 100%);
    border: 1px solid #1E3040;
    border-radius: 14px;
    padding: 20px 20px 16px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.25s ease, box-shadow 0.25s ease, transform 0.2s ease;
    cursor: default;
    height: 100%;
}
.kpi-card:hover {
    border-color: rgba(0,230,160,0.3);
    box-shadow: 0 6px 24px rgba(0,0,0,0.35), 0 0 16px rgba(0,230,160,0.05);
    transform: translateY(-2px);
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: var(--kpi-accent, linear-gradient(90deg, #00E6A0, transparent));
    opacity: 0.8;
}
.kpi-card-glow {
    position: absolute;
    top: -30px; right: -30px;
    width: 90px; height: 90px;
    background: radial-gradient(circle, var(--kpi-glow-color, rgba(0,230,160,0.08)) 0%, transparent 70%);
    pointer-events: none;
}
.kpi-icon {
    font-size: 1.25rem;
    margin-bottom: 12px;
    display: block;
    line-height: 1;
}
.kpi-value {
    font-family: 'Manrope', sans-serif;
    font-size: 1.9rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1;
    margin-bottom: 7px;
}
.kpi-label {
    font-size: 0.68rem;
    font-weight: 700;
    color: #4E6478;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 8px;
}
.kpi-sub {
    font-size: 0.68rem;
    color: #39BDF8;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 5px;
    padding-top: 8px;
    border-top: 1px solid rgba(38,52,66,0.6);
}

/* ────────────────────────────────────────────────
   CHART CONTAINERS
──────────────────────────────────────────────── */
.chart-card {
    background: #141F2B;
    border: 1px solid #263442;
    border-radius: 16px;
    padding: 6px;
    transition: border-color 0.25s, box-shadow 0.25s;
}
.chart-card:hover {
    border-color: rgba(0,230,160,0.2);
    box-shadow: 0 4px 20px rgba(0,0,0,0.35);
}
[data-testid="stPlotlyChart"] {
    background: transparent !important;
    border: 1px solid #263442 !important;
    border-radius: 14px !important;
    overflow: hidden !important;
    transition: border-color 0.25s, box-shadow 0.25s !important;
}
[data-testid="stPlotlyChart"]:hover {
    border-color: rgba(0,230,160,0.25) !important;
    box-shadow: 0 6px 24px rgba(0,0,0,0.4) !important;
}

/* ────────────────────────────────────────────────
   PLAYER PROFILE CARDS
──────────────────────────────────────────────── */
.player-card {
    background: linear-gradient(145deg, #141F2B, #1A2835);
    border: 1px solid #263442;
    border-radius: 14px;
    padding: 16px 18px;
    transition: all 0.2s ease;
    position: relative;
    overflow: hidden;
}
.player-card:hover {
    border-color: rgba(0,230,160,0.3);
    box-shadow: 0 6px 24px rgba(0,0,0,0.4);
    transform: translateY(-2px);
}
.player-card-pos-badge {
    display: inline-block;
    padding: 2px 9px;
    border-radius: 20px;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.player-card-name {
    font-family: 'Manrope', sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    color: #F4F7FA;
    margin-bottom: 2px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.player-card-team {
    font-size: 0.72rem;
    color: #91A0AE;
    margin-bottom: 12px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.player-card-stats {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 8px;
}
.player-card-stat {
    text-align: center;
    background: rgba(8,13,20,0.4);
    border-radius: 8px;
    padding: 6px 4px;
}
.player-card-stat-val {
    font-size: 1rem;
    font-weight: 700;
    color: #00E6A0;
    line-height: 1.1;
}
.player-card-stat-lbl {
    font-size: 0.6rem;
    color: #91A0AE;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 2px;
}
.player-card-rating {
    position: absolute;
    top: 14px; right: 16px;
    font-family: 'Manrope', sans-serif;
    font-size: 1.1rem;
    font-weight: 800;
    color: #FFB547;
}

/* ────────────────────────────────────────────────
   TEAM RANK TABLE
──────────────────────────────────────────────── */
.rank-table { width: 100%; border-collapse: collapse; }
.rank-table th {
    font-size: 0.65rem;
    font-weight: 700;
    color: #91A0AE;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding: 8px 12px;
    background: #101923;
    border-bottom: 1px solid #263442;
    text-align: left;
}
.rank-table td {
    font-size: 0.82rem;
    color: #F4F7FA;
    padding: 10px 12px;
    border-bottom: 1px solid rgba(38,52,66,0.6);
}
.rank-table tr:hover td { background: rgba(0,230,160,0.03); }
.rank-table .rank-num {
    font-family: 'Manrope', sans-serif;
    font-weight: 700;
    color: #91A0AE;
    font-size: 0.8rem;
}
.rank-table .rank-first td { color: #00E6A0; }
.rank-bar-wrap { background: #101923; border-radius: 4px; height: 5px; min-width: 60px; }
.rank-bar { height: 5px; border-radius: 4px;
    background: linear-gradient(90deg, #0A6B4A, #00E6A0); }

/* ────────────────────────────────────────────────
   POSITION CARDS
──────────────────────────────────────────────── */
.pos-card {
    background: linear-gradient(145deg, #141F2B, #1A2835);
    border: 1px solid #263442;
    border-radius: 14px;
    padding: 18px 20px;
    text-align: center;
    transition: all 0.22s ease;
    position: relative;
    overflow: hidden;
}
.pos-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 28px rgba(0,0,0,0.4);
}
.pos-card-icon { font-size: 1.8rem; margin-bottom: 8px; display: block; }
.pos-card-name {
    font-family: 'Manrope', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #F4F7FA;
    margin-bottom: 12px;
}
.pos-card-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px;
}
.pos-card-stat {
    background: rgba(8,13,20,0.5);
    border-radius: 8px;
    padding: 7px 5px;
}
.pos-card-stat-val {
    font-size: 1rem;
    font-weight: 700;
    line-height: 1.1;
}
.pos-card-stat-lbl {
    font-size: 0.58rem;
    color: #91A0AE;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-top: 2px;
}

/* ────────────────────────────────────────────────
   DATA TABLE
──────────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    background: #141F2B !important;
    border: 1px solid #263442 !important;
    border-radius: 14px !important;
    overflow: hidden !important;
}

/* search input */
[data-testid="stTextInput"] input {
    background: #141F2B !important;
    border: 1px solid #263442 !important;
    border-radius: 10px !important;
    color: #F4F7FA !important;
    font-size: 0.875rem !important;
    padding: 10px 16px !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #00E6A0 !important;
    box-shadow: 0 0 0 3px rgba(0,230,160,0.1) !important;
    outline: none !important;
}
[data-testid="stTextInput"] input::placeholder { color: #263442 !important; }

/* ────────────────────────────────────────────────
   BUTTONS
──────────────────────────────────────────────── */
[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, #0A6B4A 0%, #00E6A0 100%) !important;
    color: #080D14 !important;
    font-weight: 700 !important;
    font-size: 0.84rem !important;
    letter-spacing: 0.04em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    box-shadow: 0 4px 16px rgba(0,230,160,0.25) !important;
    transition: all 0.2s !important;
}
[data-testid="stDownloadButton"] > button:hover {
    box-shadow: 0 6px 24px rgba(0,230,160,0.4) !important;
    transform: translateY(-1px) !important;
}

/* ────────────────────────────────────────────────
   ALERTS & MESSAGES
──────────────────────────────────────────────── */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border-left-width: 3px !important;
    font-size: 0.84rem !important;
    background: rgba(20,31,43,0.8) !important;
}

/* ────────────────────────────────────────────────
   CAPTION & MISC
──────────────────────────────────────────────── */
[data-testid="stCaptionContainer"] {
    color: #91A0AE !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
}
hr {
    border: none !important;
    border-top: 1px solid #263442 !important;
    margin: 20px 0 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #080D14; }
::-webkit-scrollbar-thumb { background: #263442; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #00E6A0; }

/* ── Spinner ── */
[data-testid="stSpinner"] > div { border-top-color: #00E6A0 !important; }

/* ── Multiselect outside sidebar ── */
span[data-baseweb="tag"] {
    background: rgba(0,230,160,0.1) !important;
    border: 1px solid rgba(0,230,160,0.25) !important;
    color: #00E6A0 !important;
    font-weight: 600 !important;
    font-size: 0.75rem !important;
    border-radius: 6px !important;
}

/* ────────────────────────────────────────────────
   RESPONSIVENESS — fluid layout across all screens
──────────────────────────────────────────────── */

/* Tablet (≤1024px) */
@media (max-width: 1024px) {
    .main .block-container { padding: 0.5rem 1.2rem 2rem !important; }
    .pv-header {
        flex-direction: column !important;
        align-items: flex-start !important;
        padding: 16px 18px !important;
        margin: 0 0 14px !important;
    }
    .pv-header-badges { justify-content: flex-start !important; margin-top: 10px !important; }
    .pv-header-title  { font-size: 1.2rem !important; white-space: normal !important; }
    .kpi-value        { font-size: 1.6rem !important; }
}

/* Mobile (≤768px) */
@media (max-width: 768px) {
    .main .block-container { padding: 0 0.8rem 2rem !important; }
    .pv-header {
        padding: 14px 16px !important;
        border-radius: 12px !important;
        margin: 12px 0 16px !important;
    }
    .pv-header-title    { font-size: 1.05rem !important; }
    .pv-header-subtitle { font-size: 0.75rem !important; }
    .pv-badge           { font-size: 0.62rem !important; padding: 4px 8px !important; }
    .kpi-card  { padding: 14px 14px 12px !important; border-radius: 12px !important; }
    .kpi-value { font-size: 1.35rem !important; }
    .kpi-label { font-size: 0.63rem !important; }
    .kpi-icon  { font-size: 1.05rem !important; margin-bottom: 7px !important; }
    .player-card { padding: 12px 14px !important; }
    .player-card-name { font-size: 0.82rem !important; }
    .pos-card    { padding: 14px 12px !important; }
    .pos-card-icon { font-size: 1.4rem !important; }
    [data-testid="stPlotlyChart"] { border-radius: 10px !important; }
    [data-testid="stSidebar"] { min-width: 220px !important; }
    .pv-brand    { padding: 14px !important; margin-top: 0 !important; }
    .pv-app-name { font-size: 0.95rem !important; }
    [data-testid="stDataFrame"] { border-radius: 10px !important; }
    .pv-section-header { margin: 18px 0 12px !important; }
    .pv-section-title  { font-size: 0.92rem !important; }
    .rank-table th, .rank-table td { padding: 7px 8px !important; font-size: 0.74rem !important; }
}

/* Very small (≤480px) */
@media (max-width: 480px) {
    .pv-header-title { font-size: 0.92rem !important; }
    .kpi-value       { font-size: 1.15rem !important; }
    .pv-header-badges .pv-badge:not(:first-child) { display: none !important; }
}
</style>
""", unsafe_allow_html=True)


# =============================================================================
# HELPER UTILITIES
# =============================================================================
def fmt_num(n):
    """Format large numbers: 12500 → 12.5K, 1200000 → 1.2M."""
    n = int(n)
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 10_000:
        return f"{n/1_000:.1f}K"
    return f"{n:,}"


def apply_chart_style(fig, title="", height=360):
    """Apply PITCHVISION Plotly dark theme to any figure."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=height,
        font=dict(family="Inter, sans-serif", color="#91A0AE", size=11),
        margin=dict(l=16, r=16, t=44, b=16),
        title=dict(
            text=title,
            font=dict(family="Manrope, sans-serif", size=13, color="#F4F7FA"),
            x=0.0, xanchor="left", pad=dict(l=6, t=6),
        ),
        legend=dict(
            bgcolor="rgba(8,13,20,0.7)",
            bordercolor="#263442",
            borderwidth=1,
            font=dict(size=11, color="#91A0AE"),
        ),
        xaxis=dict(
            gridcolor="rgba(38,52,66,0.6)",
            zerolinecolor="rgba(38,52,66,0.8)",
            tickfont=dict(size=10, color="#91A0AE"),
            title_font=dict(size=10, color="#91A0AE"),
        ),
        yaxis=dict(
            gridcolor="rgba(38,52,66,0.6)",
            zerolinecolor="rgba(38,52,66,0.8)",
            tickfont=dict(size=10, color="#91A0AE"),
            title_font=dict(size=10, color="#91A0AE"),
        ),
        hoverlabel=dict(
            bgcolor="#141F2B",
            bordercolor="#263442",
            font=dict(family="Inter, sans-serif", size=12, color="#F4F7FA"),
        ),
    )
    fig.update_traces(selector=dict(type="bar"), marker_line_width=0)
    return fig


def pos_badge_style(pos):
    """Return CSS colour values for a position badge."""
    return {
        "GK":  ("rgba(57,189,248,0.15)",  "rgba(57,189,248,0.4)",  "#39BDF8"),
        "DEF": ("rgba(0,230,160,0.12)",   "rgba(0,230,160,0.35)",  "#00E6A0"),
        "MID": ("rgba(255,181,71,0.12)",  "rgba(255,181,71,0.35)", "#FFB547"),
        "FWD": ("rgba(255,92,108,0.12)",  "rgba(255,92,108,0.35)", "#FF5C6C"),
    }.get(pos, ("rgba(255,255,255,0.1)", "rgba(255,255,255,0.3)", "#F4F7FA"))


def render_header(total_players, seasons_active):
    """Render the top hero header banner."""
    season_text = " · ".join(sorted(seasons_active)) if seasons_active else "All Seasons"
    st.markdown(f"""
<div class="pv-header">
  <div class="pv-header-left">
    <div class="pv-header-eyebrow">PITCHVISION &nbsp;·&nbsp; Football Intelligence Platform</div>
    <div class="pv-header-title">Football Intelligence Dashboard</div>
    <div class="pv-header-subtitle">Explore player performances, compare statistics, and uncover insights across teams and positions.</div>
  </div>
  <div class="pv-header-badges">
    <div class="pv-badge pv-badge-green"><span class="pv-badge-dot"></span>Filters Active</div>
    <div class="pv-badge pv-badge-blue">{season_text}</div>
    <div class="pv-badge pv-badge-warn">Synthetic Data</div>
    <div class="pv-badge pv-badge-blue">{total_players} Players</div>
  </div>
</div>
""", unsafe_allow_html=True)


def section_header(icon, title, subtitle=""):
    sub_html = f'<div class="pv-section-sub">{subtitle}</div>' if subtitle else ""
    st.markdown(f"""
<div class="pv-section-header">
  <div class="pv-section-icon">{icon}</div>
  <div>
    <div class="pv-section-title">{title}</div>
    {sub_html}
  </div>
</div>
""", unsafe_allow_html=True)


def empty_state(msg="No data matches the current filters. Try adjusting the sidebar."):
    st.markdown(f"""
<div style="text-align:center; padding: 48px 24px;
    background: #141F2B; border: 1px dashed #263442;
    border-radius: 16px; margin: 16px 0;">
  <div style="font-size:2.5rem; margin-bottom:12px;">⚽</div>
  <div style="font-family:'Manrope',sans-serif; font-size:1rem;
    font-weight:700; color:#F4F7FA; margin-bottom:6px;">No Data Available</div>
  <div style="font-size:0.84rem; color:#91A0AE;">{msg}</div>
</div>
""", unsafe_allow_html=True)


# =============================================================================
# DATA GENERATION & LOADING
# =============================================================================
def generate_and_save_data(filepath=None):
    """Generate reproducible synthetic dataset and write to CSV."""
    if filepath is None:
        filepath = CSV_PATH
    import csv
    np.random.seed(42)
    rows, player_idx, player_id = [], 0, 1

    for season in SEASONS:
        positions = ["GK"] * 6 + ["DEF"] * 18 + ["MID"] * 21 + ["FWD"] * 15
        for i, pos in enumerate(positions):
            name = PLAYER_NAMES[player_idx]
            team = TEAMS[i % 8]
            age = int(np.random.randint(18, 37))
            appearances = int(np.random.randint(10, 39))
            minutes_played = round(appearances * int(np.random.randint(60, 91)) / 10) * 10
            yellow_cards = int(np.random.randint(0, 11))
            red_cards = int(np.random.randint(0, 3))

            if pos == "GK":
                goals, assists = 0, int(np.random.randint(0, 2))
                shots = int(np.random.randint(0, 3))
                shots_on_target = int(np.random.randint(0, 2))
                tackles = int(np.random.randint(5, 21))
                clean_sheets = int(np.random.randint(2, 16))
                pass_accuracy = round(float(np.random.uniform(55, 75)), 1)
                rating = round(float(np.random.uniform(6.0, 8.5)), 1)
            elif pos == "DEF":
                goals = int(np.random.randint(0, 5))
                assists = int(np.random.randint(0, 6))
                shots = int(np.random.randint(2, 16))
                shots_on_target = int(min(shots, np.random.randint(1, 9)))
                tackles = int(np.random.randint(20, 81))
                clean_sheets = int(np.random.randint(1, 11))
                pass_accuracy = round(float(np.random.uniform(65, 85)), 1)
                rating = round(float(np.random.uniform(6.0, 8.5)), 1)
            elif pos == "MID":
                goals = int(np.random.randint(2, 15))
                assists = int(np.random.randint(3, 16))
                shots = int(np.random.randint(10, 51))
                shots_on_target = int(min(shots, np.random.randint(4, 26)))
                tackles = int(np.random.randint(10, 51))
                clean_sheets = 0
                pass_accuracy = round(float(np.random.uniform(70, 92)), 1)
                rating = round(float(np.random.uniform(6.0, 9.0)), 1)
            else:
                goals = int(np.random.randint(5, 31))
                assists = int(np.random.randint(2, 13))
                shots = int(np.random.randint(30, 101))
                shots_on_target = int(min(shots, np.random.randint(12, 56)))
                tackles = int(np.random.randint(2, 21))
                clean_sheets = 0
                pass_accuracy = round(float(np.random.uniform(60, 82)), 1)
                rating = round(float(np.random.uniform(6.5, 9.5)), 1)

            rows.append([
                player_id, name, team, season, pos, age, appearances, minutes_played,
                goals, assists, shots, shots_on_target, pass_accuracy, tackles,
                yellow_cards, red_cards, clean_sheets, rating,
            ])
            player_idx += 1
            player_id += 1

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(REQUIRED_COLUMNS)
        writer.writerows(rows)


@st.cache_data
def load_data(filepath=None):
    """Load, validate, and clean the CSV dataset."""
    if filepath is None:
        filepath = CSV_PATH
    df = pd.read_csv(filepath, encoding="utf-8")
    missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_cols:
        st.error(f"⚠️ CSV is missing required columns: {missing_cols}")
        st.stop()
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    nan_count = df[numeric_cols].isna().sum().sum()
    if nan_count > 0:
        st.warning(f"{nan_count} missing values detected and filled with 0.")
        df[numeric_cols] = df[numeric_cols].fillna(0)
    # Derived column
    df["conversion_rate"] = np.where(
        df["shots"] > 0, (df["goals"] / df["shots"] * 100).round(1), 0.0
    )
    return df


# =============================================================================
# SIDEBAR — PITCHVISION brand + filters + navigation
# =============================================================================
def render_sidebar(df):
    """Render sidebar. Returns (filtered_df, page_name)."""

    # Brand block
    st.sidebar.markdown("""
<div class="pv-brand">
  <div class="pv-logo">
    <div class="pv-logo-icon">⚽</div>
    <div>
      <div class="pv-app-name">PitchVision</div>
    </div>
  </div>
  <div class="pv-app-sub">Football Intelligence Platform</div>
  <div class="pv-synth-tag">SYNTHETIC DATA &nbsp;·&nbsp; DEMO ONLY</div>
</div>
""", unsafe_allow_html=True)

    # Navigation
    st.sidebar.markdown('<div class="pv-sidebar-section">Navigation</div>', unsafe_allow_html=True)
    page = st.sidebar.radio(
        label="nav",
        options=[
            "📊  Overview",
            "🔍  Player Analysis",
            "🏆  Team Analysis",
            "📐  Position Analysis",
            "📋  Stats Explorer",
        ],
        label_visibility="collapsed",
    )

    st.sidebar.markdown('<div class="pv-divider"></div>', unsafe_allow_html=True)

    # ── Filters ──────────────────────────────────────────────────────────────
    st.sidebar.markdown('<div class="pv-sidebar-section">Filters</div>', unsafe_allow_html=True)

    season_opts = ["All Seasons"] + sorted(df["season"].unique().tolist())
    sel_season = st.sidebar.selectbox("Season", options=season_opts, index=0)

    all_teams = sorted(df["team"].unique().tolist())
    sel_teams = st.sidebar.multiselect("Team", options=all_teams, default=all_teams)

    all_pos = POSITIONS
    sel_pos = st.sidebar.multiselect("Position", options=all_pos, default=all_pos)

    # Apply season / team / position
    filtered = df.copy()
    if sel_season != "All Seasons":
        filtered = filtered[filtered["season"] == sel_season]
    if sel_teams:
        filtered = filtered[filtered["team"].isin(sel_teams)]
    if sel_pos:
        filtered = filtered[filtered["position"].isin(sel_pos)]

    all_players = sorted(filtered["player_name"].unique().tolist())
    sel_players = st.sidebar.multiselect("Player", options=all_players, default=all_players)

    max_apps = int(df["appearances"].max()) if not df.empty else 38
    st.sidebar.markdown("""
<div style="
    font-size:0.72rem; font-weight:700; color:#91A0AE;
    text-transform:uppercase; letter-spacing:0.08em;
    padding: 10px 0 4px 2px; display:flex; align-items:center; gap:6px;">
    <span style="color:#00E6A0;">⏱</span> Min. Appearances
</div>
<div style="font-size:0.65rem; color:#3E5468; margin-bottom:2px; padding-left:2px;">
    Filter players with at least this many games played
</div>
""", unsafe_allow_html=True)
    min_apps = st.sidebar.slider(
        "Min. Appearances",
        min_value=1,
        max_value=max_apps,
        value=1,
        label_visibility="collapsed",
        help=f"Slide to filter players who appeared in at least N matches (max: {max_apps})",
    )

    if sel_players:
        filtered = filtered[filtered["player_name"].isin(sel_players)]
    filtered = filtered[filtered["appearances"] >= min_apps]

    # Active filter indicator
    active_filters = []
    if sel_season != "All Seasons":
        active_filters.append(sel_season)
    if len(sel_teams) < len(all_teams):
        active_filters.append(f"{len(sel_teams)} teams")
    if len(sel_pos) < len(POSITIONS):
        active_filters.append("+".join(sel_pos))

    if active_filters:
        st.sidebar.markdown(
            f'<div style="padding: 6px 20px;"><span style="font-size:0.68rem;'
            f'color:#00E6A0;font-weight:600;">● Active: {", ".join(active_filters)}</span></div>',
            unsafe_allow_html=True,
        )

    # Clear filters button
    st.sidebar.markdown('<div style="padding: 4px 12px 2px;">', unsafe_allow_html=True)
    if st.sidebar.button("✕  Clear All Filters"):
        st.rerun()
    st.sidebar.markdown("</div>", unsafe_allow_html=True)

    if filtered.empty:
        st.sidebar.warning("No players match the current filters.")

    # Footer
    st.sidebar.markdown(
        '<div class="pv-sidebar-footer">PITCHVISION v2.0 · <span>2026</span></div>',
        unsafe_allow_html=True,
    )

    return filtered, page


# =============================================================================
# PAGE 1 — OVERVIEW
# =============================================================================
def page_overview(df):
    section_header("📊", "Season Overview", "Key performance metrics and top performers across the filtered dataset")

    if df.empty:
        empty_state()
        return

    # ── KPI Cards ─────────────────────────────────────────────────────────────
    total_players  = len(df)
    total_goals    = int(df["goals"].sum())
    total_assists  = int(df["assists"].sum())
    total_minutes  = int(df["minutes_played"].sum())
    avg_rating     = df["rating"].mean()
    top_scorer     = df.loc[df["goals"].idxmax(), "player_name"]
    top_assister   = df.loc[df["assists"].idxmax(), "player_name"]

    c1, c2, c3, c4, c5 = st.columns(5)
    cards = [
        (c1, "👥", fmt_num(total_players), "Total Players",    f"{df['team'].nunique()} teams", "#00E6A0", "rgba(0,230,160,0.1)"),
        (c2, "⚽", fmt_num(total_goals),   "Total Goals",      f"Top: {top_scorer.split()[0]}", "#FF5C6C", "rgba(255,92,108,0.1)"),
        (c3, "🎯", fmt_num(total_assists), "Total Assists",    f"Top: {top_assister.split()[0]}", "#39BDF8", "rgba(57,189,248,0.1)"),
        (c4, "⏱", fmt_num(total_minutes), "Minutes Played",   f"{fmt_num(total_minutes//total_players)} avg/player", "#FFB547", "rgba(255,181,71,0.1)"),
        (c5, "⭐", f"{avg_rating:.2f}",    "Avg Player Rating","Out of 10.0", "#00E6A0", "rgba(0,230,160,0.1)"),
    ]
    for col, icon, val, label, sub, accent, glow in cards:
        with col:
            st.markdown(f"""
<div class="kpi-card" style="--kpi-accent: linear-gradient(90deg, {accent}, transparent);
     --kpi-glow-color: {glow};">
  <div class="kpi-card-glow"></div>
  <span class="kpi-icon">{icon}</span>
  <div class="kpi-value" style="color:{accent};">{val}</div>
  <div class="kpi-label">{label}</div>
  <div class="kpi-sub">{sub}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)

    # ── Top 10 Goal Scorers & Top 10 Assist Providers ─────────────────────────
    col_l, col_r = st.columns(2, gap="medium")

    with col_l:
        top10g = df.nlargest(10, "goals")[["player_name", "team", "goals", "position"]].sort_values("goals", ascending=True)
        fig = px.bar(
            top10g, x="goals", y="player_name", orientation="h",
            color="goals",
            color_continuous_scale=[[0, "#0A4D2E"], [0.5, "#00A56E"], [1, "#00E6A0"]],
            hover_data={"goals": True, "team": True, "position": True, "player_name": False},
        )
        fig.update_coloraxes(showscale=False)
        fig.update_traces(hovertemplate="<b>%{y}</b><br>Goals: %{x}<extra></extra>")
        apply_chart_style(fig, "🥇 Top 10 Goal Scorers")
        fig.update_layout(yaxis_title="", xaxis_title="Goals")
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        top10a = df.nlargest(10, "assists")[["player_name", "team", "assists", "position"]].sort_values("assists", ascending=True)
        fig2 = px.bar(
            top10a, x="assists", y="player_name", orientation="h",
            color="assists",
            color_continuous_scale=[[0, "#0A2D4D"], [0.5, "#1A7FB5"], [1, "#39BDF8"]],
            hover_data={"assists": True, "team": True, "position": True, "player_name": False},
        )
        fig2.update_coloraxes(showscale=False)
        fig2.update_traces(hovertemplate="<b>%{y}</b><br>Assists: %{x}<extra></extra>")
        apply_chart_style(fig2, "🎯 Top 10 Assist Providers")
        fig2.update_layout(yaxis_title="", xaxis_title="Assists")
        st.plotly_chart(fig2, use_container_width=True)

    # ── Rating Distribution + Team Overview ───────────────────────────────────
    col_l2, col_r2 = st.columns([1, 1], gap="medium")

    with col_l2:
        fig3 = px.histogram(
            df, x="rating", color="position", nbins=20,
            barmode="overlay", opacity=0.78,
            color_discrete_map=POS_COLORS,
            category_orders={"position": POSITIONS},
        )
        fig3.update_traces(hovertemplate="Rating: %{x:.1f}<br>Count: %{y}<extra></extra>")
        apply_chart_style(fig3, "⭐ Player Rating Distribution", height=320)
        fig3.update_layout(xaxis_title="Rating", yaxis_title="Players", bargap=0.05)
        st.plotly_chart(fig3, use_container_width=True)

    with col_r2:
        team_g = df.groupby("team").agg(Goals=("goals","sum"), Assists=("assists","sum")).reset_index()
        team_g = team_g.sort_values("Goals", ascending=False)
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            name="Goals", x=team_g["team"], y=team_g["Goals"],
            marker_color="#00E6A0", marker_line_width=0,
            hovertemplate="<b>%{x}</b><br>Goals: %{y}<extra></extra>",
        ))
        fig4.add_trace(go.Bar(
            name="Assists", x=team_g["team"], y=team_g["Assists"],
            marker_color="#39BDF8", marker_line_width=0,
            hovertemplate="<b>%{x}</b><br>Assists: %{y}<extra></extra>",
        ))
        fig4.update_layout(barmode="group")
        apply_chart_style(fig4, "🏟️ Team Goals & Assists Overview", height=320)
        fig4.update_layout(xaxis_tickangle=-30, xaxis_title="", yaxis_title="Count")
        st.plotly_chart(fig4, use_container_width=True)

    # ── Goals vs Assists Scatter ───────────────────────────────────────────────
    section_header("📈", "Goals vs Assists Distribution", "All players in the filtered set")
    fig5 = px.scatter(
        df, x="goals", y="assists",
        color="position", size="minutes_played", size_max=18,
        custom_data=["player_name", "team", "season", "rating"],
        color_discrete_map=POS_COLORS,
        category_orders={"position": POSITIONS},
    )
    fig5.update_traces(
        hovertemplate=(
            "<b>%{customdata[0]}</b>  ·  %{customdata[1]}<br>"
            "%{customdata[2]}  |  Rating: %{customdata[3]}<br>"
            "Goals: %{x}   Assists: %{y}<extra></extra>"
        ),
        marker=dict(line=dict(width=0.5, color="rgba(255,255,255,0.1)")),
    )
    apply_chart_style(fig5, "", height=380)
    fig5.update_layout(xaxis_title="Goals", yaxis_title="Assists")
    st.plotly_chart(fig5, use_container_width=True)


# =============================================================================
# PAGE 2 — PLAYER ANALYSIS
# =============================================================================
def page_players(df):
    section_header("🔍", "Player Analysis", "Scouting intelligence — compare, analyse, and explore individual performances")

    if df.empty:
        empty_state()
        return

    # ── Scatter: Goals vs Assists ──────────────────────────────────────────────
    col_l, col_r = st.columns(2, gap="medium")

    with col_l:
        fig_ga = px.scatter(
            df, x="goals", y="assists",
            color="position", size="minutes_played", size_max=20,
            custom_data=["player_name", "team", "season", "rating"],
            color_discrete_map=POS_COLORS,
            category_orders={"position": POSITIONS},
        )
        fig_ga.update_traces(
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "%{customdata[1]} · %{customdata[2]}<br>"
                "Goals: %{x} · Assists: %{y}<br>"
                "Rating: %{customdata[3]}<extra></extra>"
            ),
            marker=dict(line=dict(width=0.5, color="rgba(255,255,255,0.1)")),
        )
        apply_chart_style(fig_ga, "⚽ Goals vs Assists")
        fig_ga.update_layout(xaxis_title="Goals", yaxis_title="Assists")
        st.plotly_chart(fig_ga, use_container_width=True)

    with col_r:
        fig_sg = px.scatter(
            df, x="shots", y="goals",
            color="position", size="shots_on_target", size_max=20,
            custom_data=["player_name", "team", "conversion_rate", "shots_on_target"],
            color_discrete_map=POS_COLORS,
            category_orders={"position": POSITIONS},
        )
        fig_sg.update_traces(
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "%{customdata[1]}<br>"
                "Shots: %{x} · Goals: %{y}<br>"
                "On Target: %{customdata[3]} · Conv: %{customdata[2]}%<extra></extra>"
            ),
            marker=dict(line=dict(width=0.5, color="rgba(255,255,255,0.1)")),
        )
        apply_chart_style(fig_sg, "🎯 Shots vs Goals — Conversion Efficiency")
        fig_sg.update_layout(xaxis_title="Total Shots", yaxis_title="Goals Scored")
        st.plotly_chart(fig_sg, use_container_width=True)

    # ── Player Profile Cards ───────────────────────────────────────────────────
    section_header("🃏", "Player Spotlight", "Top performers in the filtered selection")
    top5 = df.nlargest(5, "rating")
    cols = st.columns(5, gap="small")
    for i, (_, row) in enumerate(top5.iterrows()):
        pos = row["position"]
        bg, border, color = pos_badge_style(pos)
        with cols[i]:
            st.markdown(f"""
<div class="player-card">
  <span class="player-card-rating">{row['rating']}</span>
  <span class="player-card-pos-badge"
    style="background:{bg};border:1px solid {border};color:{color};">{pos}</span>
  <div class="player-card-name">{row['player_name']}</div>
  <div class="player-card-team">{row['team']}</div>
  <div class="player-card-stats">
    <div class="player-card-stat">
      <div class="player-card-stat-val" style="color:{color};">{int(row['goals'])}</div>
      <div class="player-card-stat-lbl">Goals</div>
    </div>
    <div class="player-card-stat">
      <div class="player-card-stat-val" style="color:#39BDF8;">{int(row['assists'])}</div>
      <div class="player-card-stat-lbl">Assists</div>
    </div>
    <div class="player-card-stat">
      <div class="player-card-stat-val" style="color:#FFB547;">{int(row['appearances'])}</div>
      <div class="player-card-stat-lbl">Apps</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── Player Comparison ──────────────────────────────────────────────────────
    section_header("⚖️", "Player Comparison", "Select 2–5 players for a head-to-head analysis")

    all_players = sorted(df["player_name"].unique().tolist())
    defaults = all_players[:2] if len(all_players) >= 2 else all_players
    selected = st.multiselect(
        "Choose players to compare", options=all_players,
        default=defaults, key="player_compare_select",
        help="Select 2 to 5 players"
    )

    if len(selected) < 2:
        st.info("Select at least 2 players to compare.")
        return
    if len(selected) > 5:
        st.warning("Please select a maximum of 5 players.")
        selected = selected[:5]

    cmp_df = df[df["player_name"].isin(selected)].copy()
    COMPARE_COLORS = ["#00E6A0", "#39BDF8", "#FFB547", "#FF5C6C", "#C084FC"]

    # Radar chart
    radar_stats = ["goals", "assists", "shots_on_target", "tackles", "pass_accuracy", "rating"]
    radar_labels = ["Goals", "Assists", "Shots on Target", "Tackles", "Pass Accuracy", "Rating"]

    # Normalize 0-1 per column using full df for context
    norm_df = df[radar_stats].copy()
    mins = norm_df.min()
    maxs = norm_df.max()
    denom = (maxs - mins).replace(0, 1)

    fig_radar = go.Figure()
    for idx, player in enumerate(selected):
        prow = cmp_df[cmp_df["player_name"] == player]
        if prow.empty:
            continue
        prow = prow.iloc[0]
        vals = [(prow[s] - mins[s]) / denom[s] for s in radar_stats]
        vals_closed = vals + [vals[0]]
        labels_closed = radar_labels + [radar_labels[0]]
        clr = COMPARE_COLORS[idx % len(COMPARE_COLORS)]
        # Convert hex color to rgba for fill
        hex_map = {
            "#00E6A0": "rgba(0,230,160,0.08)",
            "#39BDF8": "rgba(57,189,248,0.08)",
            "#FFB547": "rgba(255,181,71,0.08)",
            "#FF5C6C": "rgba(255,92,108,0.08)",
            "#C084FC": "rgba(192,132,252,0.08)",
        }
        fill_clr = hex_map.get(clr, "rgba(255,255,255,0.05)")
        fig_radar.add_trace(go.Scatterpolar(
            r=vals_closed, theta=labels_closed,
            fill="toself", name=player,
            line_color=clr,
            fillcolor=fill_clr,
            opacity=0.85,
        ))

    fig_radar.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 1], gridcolor="#263442",
                            tickfont=dict(size=9, color="#91A0AE"), showticklabels=False),
            angularaxis=dict(gridcolor="#263442", tickfont=dict(size=11, color="#91A0AE")),
        ),
        showlegend=True,
    )
    apply_chart_style(fig_radar, "🕸️ Player Attribute Radar", height=440)
    st.plotly_chart(fig_radar, use_container_width=True)

    # Grouped bar comparison
    stat_cols = ["goals", "assists", "shots_on_target", "tackles", "rating"]
    stat_disp = ["Goals", "Assists", "Shots on Target", "Tackles", "Rating"]
    melted = cmp_df[["player_name"] + stat_cols].melt(
        id_vars="player_name", value_vars=stat_cols,
        var_name="stat", value_name="value",
    )
    melted["stat"] = melted["stat"].map(dict(zip(stat_cols, stat_disp)))

    player_color_map = {p: COMPARE_COLORS[i % len(COMPARE_COLORS)] for i, p in enumerate(selected)}
    fig_cmp = px.bar(
        melted, x="stat", y="value", color="player_name", barmode="group",
        color_discrete_map=player_color_map,
    )
    fig_cmp.update_traces(hovertemplate="<b>%{data.name}</b><br>%{x}: %{y}<extra></extra>")
    apply_chart_style(fig_cmp, "📊 Head-to-Head Statistics", height=340)
    fig_cmp.update_layout(xaxis_title="", yaxis_title="Value",
                          legend_title_text="Player")
    st.plotly_chart(fig_cmp, use_container_width=True)

    # Comparison summary table
    section_header("📋", "Comparison Summary")
    display_cols = ["player_name", "team", "position", "goals", "assists",
                    "minutes_played", "shots", "pass_accuracy", "rating"]
    display_names = ["Player", "Team", "Pos", "Goals", "Assists",
                     "Minutes", "Shots", "Pass %", "Rating"]
    cmp_show = cmp_df[display_cols].copy()
    cmp_show.columns = display_names
    st.dataframe(cmp_show.set_index("Player"), use_container_width=True)


# =============================================================================
# PAGE 3 — TEAM ANALYSIS
# =============================================================================
def page_teams(df):
    section_header("🏆", "Team Analysis", "Club-level performance intelligence across goals, assists, and player quality")

    if df.empty:
        empty_state()
        return

    # Aggregate
    team_stats = (
        df.groupby("team").agg(
            Goals=("goals", "sum"),
            Assists=("assists", "sum"),
            Players=("player_name", "count"),
            Avg_Rating=("rating", "mean"),
            Total_Minutes=("minutes_played", "sum"),
        )
        .reset_index()
        .rename(columns={"team": "Team"})
    )
    team_stats["Avg_Rating"] = team_stats["Avg_Rating"].round(2)
    team_stats = team_stats.sort_values("Goals", ascending=False).reset_index(drop=True)
    team_stats.index += 1  # rank from 1

    # ── Top row: Goals + Assists bars ──────────────────────────────────────────
    col_l, col_r = st.columns(2, gap="medium")

    with col_l:
        fig_g = px.bar(
            team_stats.sort_values("Goals", ascending=True),
            x="Goals", y="Team", orientation="h",
            color="Goals",
            color_continuous_scale=[[0, "#083D22"], [0.5, "#00A56E"], [1, "#00E6A0"]],
        )
        fig_g.update_coloraxes(showscale=False)
        fig_g.update_traces(hovertemplate="<b>%{y}</b><br>Goals: %{x}<extra></extra>")
        apply_chart_style(fig_g, "⚽ Goals by Team")
        fig_g.update_layout(yaxis_title="", xaxis_title="Total Goals")
        st.plotly_chart(fig_g, use_container_width=True)

    with col_r:
        fig_a = px.bar(
            team_stats.sort_values("Assists", ascending=True),
            x="Assists", y="Team", orientation="h",
            color="Assists",
            color_continuous_scale=[[0, "#062840"], [0.5, "#1A7FB5"], [1, "#39BDF8"]],
        )
        fig_a.update_coloraxes(showscale=False)
        fig_a.update_traces(hovertemplate="<b>%{y}</b><br>Assists: %{x}<extra></extra>")
        apply_chart_style(fig_a, "🎯 Assists by Team")
        fig_a.update_layout(yaxis_title="", xaxis_title="Total Assists")
        st.plotly_chart(fig_a, use_container_width=True)

    # ── Second row: Players count + Avg Rating ─────────────────────────────────
    col_l2, col_r2 = st.columns(2, gap="medium")

    with col_l2:
        fig_p = px.bar(
            team_stats.sort_values("Players", ascending=True),
            x="Players", y="Team", orientation="h",
            color="Players",
            color_continuous_scale=[[0, "#1a1a3e"], [0.5, "#4a9eff"], [1, "#a8d8ff"]],
        )
        fig_p.update_coloraxes(showscale=False)
        fig_p.update_traces(hovertemplate="<b>%{y}</b><br>Players: %{x}<extra></extra>")
        apply_chart_style(fig_p, "👥 Squad Size")
        fig_p.update_layout(yaxis_title="", xaxis_title="Players")
        st.plotly_chart(fig_p, use_container_width=True)

    with col_r2:
        fig_r = px.bar(
            team_stats.sort_values("Avg_Rating", ascending=True),
            x="Avg_Rating", y="Team", orientation="h",
            color="Avg_Rating",
            color_continuous_scale=[[0, "#3d2b00"], [0.5, "#C47B00"], [1, "#FFB547"]],
        )
        fig_r.update_coloraxes(showscale=False)
        fig_r.update_traces(hovertemplate="<b>%{y}</b><br>Avg Rating: %{x:.2f}<extra></extra>")
        apply_chart_style(fig_r, "⭐ Average Team Rating")
        fig_r.update_layout(yaxis_title="", xaxis_title="Avg Rating")
        st.plotly_chart(fig_r, use_container_width=True)

    # ── Team Rankings Table ────────────────────────────────────────────────────
    section_header("📋", "Team Performance Rankings", "Sorted by total goals scored")
    max_goals = team_stats["Goals"].max() if team_stats["Goals"].max() > 0 else 1

    rows_html = ""
    for rank, row in team_stats.reset_index().iterrows():
        bar_pct = int(row["Goals"] / max_goals * 100)
        row_class = 'rank-first' if rank == 0 else ''
        rows_html += f"""
<tr class="{row_class}">
  <td><span class="rank-num">#{rank+1}</span></td>
  <td><b>{row['Team']}</b></td>
  <td style="text-align:right;">{int(row['Goals'])}</td>
  <td style="text-align:right;">{int(row['Assists'])}</td>
  <td style="text-align:right;">{int(row['Players'])}</td>
  <td style="text-align:right;">{row['Avg_Rating']:.2f}</td>
  <td style="min-width:80px;">
    <div class="rank-bar-wrap"><div class="rank-bar" style="width:{bar_pct}%;"></div></div>
  </td>
</tr>"""

    st.markdown(f"""
<div style="background:#141F2B;border:1px solid #263442;border-radius:14px;overflow:hidden;margin-top:8px;">
<table class="rank-table" style="width:100%;">
  <thead>
    <tr>
      <th>#</th><th>Team</th><th style="text-align:right;">Goals</th>
      <th style="text-align:right;">Assists</th><th style="text-align:right;">Players</th>
      <th style="text-align:right;">Avg Rating</th><th>Goal Share</th>
    </tr>
  </thead>
  <tbody>{rows_html}</tbody>
</table>
</div>
""", unsafe_allow_html=True)

    # ── Team Radar ─────────────────────────────────────────────────────────────
    section_header("🕸️", "Team Radar Comparison", "Normalised across selected teams — select teams below")
    radar_teams = st.multiselect(
        "Teams to include in radar",
        options=team_stats["Team"].tolist(),
        default=team_stats["Team"].tolist()[:6],
        key="team_radar_select",
    )

    if not radar_teams:
        st.info("Select at least one team.")
        return

    rad_df = team_stats[team_stats["Team"].isin(radar_teams)].copy()
    for col in ["Goals", "Assists", "Avg_Rating"]:
        cmin, cmax = rad_df[col].min(), rad_df[col].max()
        rad_df[f"{col}_n"] = (rad_df[col] - cmin) / (cmax - cmin + 1e-9)

    cats = ["Goals", "Assists", "Avg Rating"]
    norm_cols = ["Goals_n", "Assists_n", "Avg_Rating_n"]
    TCOLORS = ["#00E6A0", "#39BDF8", "#FFB547", "#FF5C6C", "#C084FC", "#F472B6", "#34D399", "#60A5FA"]

    fig_tr = go.Figure()
    for idx, (_, row) in enumerate(rad_df.iterrows()):
        vals = [row[c] for c in norm_cols]
        fig_tr.add_trace(go.Scatterpolar(
            r=vals + [vals[0]], theta=cats + [cats[0]],
            fill="toself", name=row["Team"],
            line_color=TCOLORS[idx % len(TCOLORS)],
            opacity=0.75,
        ))

    fig_tr.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 1], gridcolor="#263442",
                            tickfont=dict(size=9, color="#91A0AE"), showticklabels=False),
            angularaxis=dict(gridcolor="#263442", tickfont=dict(size=11, color="#91A0AE")),
        ),
        showlegend=True,
    )
    apply_chart_style(fig_tr, "🕸️ Team Radar (Normalised)", height=460)
    st.plotly_chart(fig_tr, use_container_width=True)


# =============================================================================
# PAGE 4 — POSITION ANALYSIS
# =============================================================================
def page_positions(df):
    section_header("📐", "Position Analysis", "Role-based performance breakdown across GK, DEF, MID and FWD")

    if df.empty:
        empty_state()
        return

    POS_META = {
        "GK":  {"icon": "🧤", "label": "Goalkeepers",  "color": "#39BDF8"},
        "DEF": {"icon": "🛡️", "label": "Defenders",    "color": "#00E6A0"},
        "MID": {"icon": "⚙️", "label": "Midfielders",  "color": "#FFB547"},
        "FWD": {"icon": "⚡", "label": "Forwards",     "color": "#FF5C6C"},
    }

    pos_stats = (
        df.groupby("position").agg(
            Count=("player_name", "count"),
            Avg_Goals=("goals", "mean"),
            Avg_Assists=("assists", "mean"),
            Avg_Tackles=("tackles", "mean"),
            Avg_Rating=("rating", "mean"),
            Avg_Minutes=("minutes_played", "mean"),
            Avg_Pass=("pass_accuracy", "mean"),
        )
        .reset_index()
        .rename(columns={"position": "Position"})
        .round(2)
    )

    # ── Position Summary Cards ─────────────────────────────────────────────────
    card_cols = st.columns(4, gap="small")
    for i, pos in enumerate(POSITIONS):
        row = pos_stats[pos_stats["Position"] == pos]
        if row.empty:
            continue
        row = row.iloc[0]
        meta = POS_META[pos]
        clr = meta["color"]
        with card_cols[i]:
            st.markdown(f"""
<div class="pos-card" style="border-top: 3px solid {clr};">
  <span class="pos-card-icon">{meta['icon']}</span>
  <div class="pos-card-name">{meta['label']}</div>
  <div class="pos-card-grid">
    <div class="pos-card-stat">
      <div class="pos-card-stat-val" style="color:{clr};">{int(row['Count'])}</div>
      <div class="pos-card-stat-lbl">Players</div>
    </div>
    <div class="pos-card-stat">
      <div class="pos-card-stat-val" style="color:#FFB547;">{row['Avg_Rating']}</div>
      <div class="pos-card-stat-lbl">Avg Rating</div>
    </div>
    <div class="pos-card-stat">
      <div class="pos-card-stat-val" style="color:#00E6A0;">{row['Avg_Goals']}</div>
      <div class="pos-card-stat-lbl">Avg Goals</div>
    </div>
    <div class="pos-card-stat">
      <div class="pos-card-stat-val" style="color:#39BDF8;">{row['Avg_Assists']}</div>
      <div class="pos-card-stat-lbl">Avg Assists</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)

    # ── Chart row 1: Avg stats bars ────────────────────────────────────────────
    c1, c2, c3 = st.columns(3, gap="medium")

    with c1:
        fig_pg = px.bar(
            pos_stats, x="Position", y="Avg_Goals",
            color="Position", color_discrete_map=POS_COLORS,
            category_orders={"Position": POSITIONS},
        )
        fig_pg.update_traces(hovertemplate="<b>%{x}</b><br>Avg Goals: %{y:.2f}<extra></extra>")
        apply_chart_style(fig_pg, "⚽ Avg Goals by Position", height=300)
        fig_pg.update_layout(xaxis_title="", yaxis_title="Avg Goals", showlegend=False)
        st.plotly_chart(fig_pg, use_container_width=True)

    with c2:
        fig_pa = px.bar(
            pos_stats, x="Position", y="Avg_Assists",
            color="Position", color_discrete_map=POS_COLORS,
            category_orders={"Position": POSITIONS},
        )
        fig_pa.update_traces(hovertemplate="<b>%{x}</b><br>Avg Assists: %{y:.2f}<extra></extra>")
        apply_chart_style(fig_pa, "🎯 Avg Assists by Position", height=300)
        fig_pa.update_layout(xaxis_title="", yaxis_title="Avg Assists", showlegend=False)
        st.plotly_chart(fig_pa, use_container_width=True)

    with c3:
        fig_pt = px.bar(
            pos_stats, x="Position", y="Avg_Tackles",
            color="Position", color_discrete_map=POS_COLORS,
            category_orders={"Position": POSITIONS},
        )
        fig_pt.update_traces(hovertemplate="<b>%{x}</b><br>Avg Tackles: %{y:.2f}<extra></extra>")
        apply_chart_style(fig_pt, "🛡️ Avg Tackles by Position", height=300)
        fig_pt.update_layout(xaxis_title="", yaxis_title="Avg Tackles", showlegend=False)
        st.plotly_chart(fig_pt, use_container_width=True)

    # ── Chart row 2: Rating + Squad donut ──────────────────────────────────────
    col_l, col_r = st.columns(2, gap="medium")

    with col_l:
        fig_pr = px.bar(
            pos_stats, x="Position", y="Avg_Rating",
            color="Position", color_discrete_map=POS_COLORS,
            category_orders={"Position": POSITIONS},
        )
        fig_pr.update_traces(hovertemplate="<b>%{x}</b><br>Avg Rating: %{y:.2f}<extra></extra>")
        apply_chart_style(fig_pr, "⭐ Avg Rating by Position", height=320)
        fig_pr.update_layout(xaxis_title="", yaxis_title="Avg Rating", showlegend=False)
        st.plotly_chart(fig_pr, use_container_width=True)

    with col_r:
        fig_donut = px.pie(
            pos_stats, values="Count", names="Position", hole=0.48,
            color="Position", color_discrete_map=POS_COLORS,
            category_orders={"names": POSITIONS},
        )
        fig_donut.update_traces(
            textfont=dict(size=12, family="Inter, sans-serif"),
            hovertemplate="<b>%{label}</b><br>Players: %{value}<br>%{percent}<extra></extra>",
            marker=dict(line=dict(color="#080D14", width=2)),
        )
        apply_chart_style(fig_donut, "🍩 Squad Composition", height=320)
        st.plotly_chart(fig_donut, use_container_width=True)

    # ── Rating distribution box plot ───────────────────────────────────────────
    fig_box = px.box(
        df, x="position", y="rating", color="position", points="all",
        color_discrete_map=POS_COLORS,
        category_orders={"position": POSITIONS},
    )
    fig_box.update_traces(
        hovertemplate="<b>%{x}</b><br>Rating: %{y}<extra></extra>",
        marker=dict(size=5, opacity=0.5, line=dict(width=0)),
    )
    apply_chart_style(fig_box, "📦 Rating Distribution by Position", height=360)
    fig_box.update_layout(xaxis_title="Position", yaxis_title="Rating", showlegend=False)
    st.plotly_chart(fig_box, use_container_width=True)

    # ── Top performer per position ─────────────────────────────────────────────
    section_header("🏅", "Top Performer per Position", "Highest rated player in each role")
    top_cols = st.columns(4, gap="small")
    for i, pos in enumerate(POSITIONS):
        pos_df = df[df["position"] == pos]
        if pos_df.empty:
            continue
        top = pos_df.loc[pos_df["rating"].idxmax()]
        meta = POS_META[pos]
        clr = meta["color"]
        bg, border, _ = pos_badge_style(pos)
        with top_cols[i]:
            st.markdown(f"""
<div class="player-card" style="border-top: 3px solid {clr};">
  <span class="player-card-rating" style="color:{clr};">{top['rating']}</span>
  <span class="player-card-pos-badge" style="background:{bg};border:1px solid {border};color:{clr};">
    {meta['icon']} {pos}
  </span>
  <div class="player-card-name">{top['player_name']}</div>
  <div class="player-card-team">{top['team']}</div>
  <div class="player-card-stats">
    <div class="player-card-stat">
      <div class="player-card-stat-val" style="color:{clr};">{int(top['goals'])}</div>
      <div class="player-card-stat-lbl">Goals</div>
    </div>
    <div class="player-card-stat">
      <div class="player-card-stat-val" style="color:#39BDF8;">{int(top['assists'])}</div>
      <div class="player-card-stat-lbl">Assists</div>
    </div>
    <div class="player-card-stat">
      <div class="player-card-stat-val" style="color:#FFB547;">{int(top['appearances'])}</div>
      <div class="player-card-stat-lbl">Apps</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# =============================================================================
# PAGE 5 — STATS EXPLORER
# =============================================================================
def render_table(df):
    section_header("📋", "Stats Explorer", "Search, sort, and export the full player statistics dataset")

    if df.empty:
        empty_state()
        return

    # Search + export row
    col_search, col_btn = st.columns([3, 1], gap="medium")
    with col_search:
        search = st.text_input(
            "Search", "", placeholder="🔍  Search by player name...",
            label_visibility="collapsed",
        )
    with col_btn:
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️  Export CSV",
            data=csv_bytes,
            file_name="pitchvision_stats.csv",
            mime="text/csv",
            use_container_width=True,
        )

    filtered = df.copy()
    if search:
        filtered = filtered[filtered["player_name"].str.contains(search, case=False, na=False)]

    st.caption(f"Showing **{len(filtered)}** of {len(df)} players")

    # Clean display columns
    display_cols = [
        "player_name", "team", "position", "season", "age", "appearances",
        "minutes_played", "goals", "assists", "shots", "shots_on_target",
        "conversion_rate", "pass_accuracy", "tackles",
        "yellow_cards", "red_cards", "clean_sheets", "rating",
    ]
    col_rename = {
        "player_name": "Player", "team": "Team", "position": "Pos",
        "season": "Season", "age": "Age", "appearances": "Apps",
        "minutes_played": "Minutes", "goals": "Goals", "assists": "Assists",
        "shots": "Shots", "shots_on_target": "On Target",
        "conversion_rate": "Conv %", "pass_accuracy": "Pass %",
        "tackles": "Tackles", "yellow_cards": "YC", "red_cards": "RC",
        "clean_sheets": "CS", "rating": "Rating",
    }
    show = filtered[display_cols].rename(columns=col_rename)
    st.dataframe(show, use_container_width=True, height=520)


# =============================================================================
# MAIN
# =============================================================================
def main():
    inject_css()

    # Ensure CSV exists
    if not os.path.exists(CSV_PATH):
        with st.spinner("⚙️ Generating synthetic dataset..."):
            generate_and_save_data()

    df = load_data()
    filtered_df, page = render_sidebar(df)

    # Top header (shown on every page)
    seasons_active = filtered_df["season"].unique().tolist() if not filtered_df.empty else []
    render_header(len(filtered_df), seasons_active)

    # Page routing
    if page == "📊  Overview":
        page_overview(filtered_df)
    elif page == "🔍  Player Analysis":
        page_players(filtered_df)
    elif page == "🏆  Team Analysis":
        page_teams(filtered_df)
    elif page == "📐  Position Analysis":
        page_positions(filtered_df)
    elif page == "📋  Stats Explorer":
        render_table(filtered_df)


if __name__ == "__main__":
    main()
