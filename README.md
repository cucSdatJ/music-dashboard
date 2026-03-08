# 🎵 Music Trend Dashboard

> An interactive data analytics dashboard analyzing **13,051 Spotify tracks** to uncover what makes a song go viral — built with Python, Streamlit, and Plotly.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.x-3F4F75?logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 Project Overview

The **Music Trend Dashboard** is a data analytics portfolio project that digs into the audio DNA of over 13,000 Spotify tracks to answer one question: *what actually makes a song popular?*

The dashboard provides three lenses for exploration:

| Tab | Focus |
|-----|-------|
| 🧬 **Viral Song DNA** | Compare audio features (tempo, danceability, acousticness, etc.) across popularity tiers |
| 💜 **Emotion & Music** | Explore valence, energy, and emotional quadrants (happy, angry, sad, peaceful) |
| 🔬 **Deep Dive** | Analyze track duration, loudness distributions, and recording type (studio vs. live) |

Additional UI highlights:
- Animated metric cards rendered with `streamlit.components.v1.html()`
- Lottie animation header for a polished look
- CSS fade-in entry effects
- Interactive sidebar filters (genre, year range, popularity tier)

---

## 🔍 Key Findings & Insights

1. **Danceability & Energy Drive Virality** — Tracks in the top popularity tier score significantly higher on danceability and energy compared to lower tiers. The sweet spot sits around 0.70–0.85 for both features.

2. **The "Happy-Energetic" Quadrant Dominates Charts** — Songs with high valence *and* high energy (upper-right emotional quadrant) consistently appear more often among viral tracks, confirming that upbeat, feel-good music has a structural advantage on streaming platforms.

3. **Acousticness is Inversely Correlated with Popularity** — Highly acoustic tracks tend to land in lower popularity tiers. Electronic and produced sounds dominate the top tier.

4. **Sweet Spot for Duration** — The most popular tracks cluster between **2:30 and 3:45 minutes**. Both very short and very long tracks underperform on average.

5. **Loudness Matters, But Has a Ceiling** — Top-tier tracks are louder on average (closer to 0 dBFS), but there is a clear ceiling effect — overly loud, heavily compressed tracks do not out-perform moderately loud ones.

6. **Studio Recordings Outperform Live Recordings** — Studio tracks account for the vast majority of high-popularity songs, suggesting production quality is a meaningful factor.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.9+ |
| Dashboard framework | [Streamlit](https://streamlit.io/) |
| Interactive charts | [Plotly Express & Graph Objects](https://plotly.com/python/) |
| Data processing | [Pandas](https://pandas.pydata.org/) |
| Animations | [streamlit-lottie](https://github.com/andfanilo/streamlit-lottie) |
| Styling | Custom CSS injected via `st.markdown` |

---

## 📁 Project Structure

```
music-dashboard/
├── app.py                  # Main Streamlit application & dashboard layout
├── src/
│   ├── __init__.py
│   ├── load_data.py        # Data ingestion & cleaning pipeline
│   └── queries.py          # All analysis / aggregation functions
├── data/
│   └── spotify_tracks.csv  # Raw dataset (13,051 tracks)
├── assets/
│   └── lottie_music.json   # Lottie animation file for the header
├── requirements.txt        # Python dependencies
└── README.md
```

---

## 🚀 Setup Instructions

### Prerequisites

- Python 3.9 or higher
- `pip` package manager

### 1. Clone the repository

```bash
git clone https://github.com/cucSdatJ/music-dashboard.git
cd music-dashboard
```

### 2. Create and activate a virtual environment

```bash
# macOS / Linux
python -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the dashboard

```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

### 5. (Optional) Dataset

Place the Spotify tracks CSV file at `data/spotify_tracks.csv`. If you are using a different path, update the `DATA_PATH` constant at the top of `src/load_data.py`.

---

## 📸 Screenshots

> *Screenshots will be added once the app is deployed.*

### Dashboard Header & Sidebar Filters
<!-- Replace with actual screenshot -->
![Header placeholder](https://via.placeholder.com/900x200?text=Dashboard+Header+%26+Sidebar)

### Tab 1 — Viral Song DNA
<!-- Replace with actual screenshot -->
![Viral Song DNA placeholder](https://via.placeholder.com/900x450?text=Viral+Song+DNA+Tab)

### Tab 2 — Emotion & Music
<!-- Replace with actual screenshot -->
![Emotion & Music placeholder](https://via.placeholder.com/900x450?text=Emotion+%26+Music+Tab)

### Tab 3 — Deep Dive
<!-- Replace with actual screenshot -->
![Deep Dive placeholder](https://via.placeholder.com/900x450?text=Deep+Dive+Tab)

---

## 📄 License

This project is released under the [MIT License](LICENSE).

---

*Built with ❤️ as a data analytics portfolio project.*
