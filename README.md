# 🎵 Music Trend Dashboard

> An interactive data analytics dashboard analyzing **13,051 Spotify tracks** to uncover what makes a song go viral — built with Python, Streamlit, and Plotly. Features a live data pipeline with multi-source fallback.

🔗 **[Live Demo](https://music-dashboard-cucsdatj.streamlit.app/)** &nbsp;|&nbsp; ⭐ Star this repo if you find it useful!

---

## 📌 Project Overview

What separates a viral song from one that nobody hears? Is it the beat, the mood, the loudness — or something else entirely?

This project approaches that question as a data problem. Starting from a raw dataset of 13,051 Spotify tracks, I built a full end-to-end data analytics pipeline: cleaning and validating the data, designing and running 9 targeted analyses, and presenting the findings through an interactive web dashboard that anyone can explore without writing a single line of code.

The dashboard is organized around three analytical threads. The first examines the **technical DNA of viral songs** — comparing audio features like danceability, energy, and acousticness across popularity tiers. The second explores **emotion and music** — using Spotify's valence and energy scores to map songs onto emotional quadrants inspired by Russell's Circumplex Model of Affect. The third takes a **structural deep dive** into duration, loudness, and recording type.

---

## 🔍 Key Findings

**Viral songs are significantly more danceable.** Tracks in the top popularity tier (81–100) have an average danceability of 0.699, vs 0.616 for the lowest tier — a 13% difference and the strongest structural predictor in the dataset.

**Sad songs outperform happy ones.** Songs with low valence averaged 49.38 in popularity vs 47.77 for upbeat songs — consistent with psychological research on the "sad music paradox."

**Dark and intense music dominates streaming.** "Sad & Slow" and "Dark & Intense" rank first and second in average popularity across the four emotional quadrants, while "Happy & Calm" ranks last at 44.74.

**The sweet spot for song length is 3–5 minutes.** Both brackets average ~49.4 in popularity, while tracks under 2 minutes or over 5 minutes underperform.

**Louder masters perform better.** Songs above -5 dB average 50.72 in popularity vs 45.58 for moderate-loudness tracks — supporting the "loudness war" trend in modern production.

**No single feature predicts popularity on its own.** The highest Pearson correlation was only 0.051 (danceability). Viral success is multidimensional and cannot be reduced to a single formula.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     app.py (UI Layer)                   │
│         Streamlit dashboard · Plotly charts             │
│         Sidebar filters · Animated metric cards         │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│               src/queries.py (Analysis Layer)           │
│         9 analytical functions · Correlation            │
│         Emotional quadrants · Song profiles             │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│              src/load_data.py (Data Layer)              │
│     Cleaning · Validation · Feature engineering         │
│     Source routing: CSV → Spotify → Last.fm             │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│                    Data Sources                         │
│    🟢 Spotify API → 🟡 Last.fm API → 🔴 Local CSV       │
│           (multi-source fallback pipeline)              │
└─────────────────────────────────────────────────────────┘
```

---

## 🔄 Live Data Pipeline

The dashboard supports three data sources with **automatic cascading fallback**:

```
User selects "Live Charts"
        │
        ▼
🟢 Try Spotify API
        │ fail (401 API restriction)
        ▼
🟡 Try Last.fm API
        │ fail (502 server error)
        ▼
🔴 Fall back to Local CSV
        │
        ▼
Dashboard always renders ✅
```

This **graceful degradation** pattern ensures the dashboard never crashes due to external API failures. The terminal log shows exactly which source was used and why any fallback occurred.

---

## ⚠️ Known API Restrictions (as of March 2026)

**Spotify API:** In late 2024, Spotify restricted editorial playlist access and tightened rate limits for apps in Development Mode. The `playlist_items()` endpoint for official playlists (e.g. Top 50 Global) now requires user-level authentication (Authorization Code Flow) rather than Client Credentials Flow, returning `401 Valid user authentication required`. The Search API also enforces stricter limits in Development Mode. Resolving this fully requires either applying for Extended Quota Mode or implementing Authorization Code Flow with PKCE.

**Last.fm API:** Last.fm is generally more permissive but occasionally returns `502 Bad Gateway` during periods of server instability. These are transient and resolve on retry. Importantly, Last.fm does not provide Spotify-style audio features (danceability, energy, valence, etc.) — only play counts and user-generated tags. In Last.fm mode, popularity rankings reflect real chart data, but audio feature charts use dataset population averages as placeholders and should not be interpreted as per-track measurements.

---

## 🛠️ Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| Data source (static) | Kaggle Spotify Tracks Dataset | Core analysis dataset |
| Data source (live) | Spotify Web API + spotipy | Live chart data |
| Data source (fallback) | Last.fm API + pylast | Fallback live chart data |
| Data cleaning | Python, Pandas | Validation, feature engineering |
| Analysis | Pandas, NumPy | Groupby, correlation, classification |
| Visualization | Plotly Express | Interactive charts |
| Dashboard | Streamlit | Web application framework |
| Animations | CSS keyframes, JS, streamlit-lottie | UI effects |
| Statistical modeling | statsmodels | OLS trendline |
| Environment | python-dotenv | Secure API key handling |
| Deployment | Streamlit Cloud | Public hosting |
| Version control | Git, GitHub | Source control |

---

## 📁 Project Structure

```
music-dashboard/
│
├── data/
│   └── song_data.csv                  # Raw dataset (13,051 tracks)
│
├── notebooks/
│   └── data_exploration.ipynb      # EDA and function testing
│
├── src/
│   ├── load_data.py                   # Data acquisition, cleaning, routing
│   ├── queries.py                     # 9 analytical functions
│   ├── spotify_fetcher.py             # Spotify API integration
│   └── lastfm_fetcher.py             # Last.fm API fallback
│
├── app.py                             # Streamlit dashboard entry point
├── requirements.txt                   # Python dependencies
├── .env                               # API keys (NOT committed to Git)
├── .gitignore
└── README.md
```

---

## ⚙️ Setup & Installation

```bash
# Clone the repo
git clone https://github.com/cucSdatJ/music-dashboard.git
cd music-dashboard

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Optional: set up API keys in a .env file
# SPOTIFY_CLIENT_ID=your_id
# SPOTIFY_CLIENT_SECRET=your_secret
# LASTFM_API_KEY=your_key

# Run the dashboard
python -m streamlit run app.py
```

The dashboard runs fully without API keys — simply select "Local Dataset" in the sidebar.

---

## 💡 What I Learned

The hardest part of data analysis is not writing code — it is asking the right questions before opening the dataset. The most interesting findings came from questions designed deliberately, not from running generic statistics on every column.

Building the live data pipeline taught an equally important engineering lesson: external APIs fail, and good systems handle failure gracefully. The cascading fallback pattern means the dashboard always serves the user, regardless of what any third-party service is doing. This is production-ready thinking, not just portfolio thinking.

---

## 🔮 Future Improvements

**Data enrichment.** Adding artist and genre columns would enable segmented analysis — the formula for a viral hip-hop track likely differs significantly from pop, and the current aggregate view masks those differences.

**Time-series tracking.** The most valuable capability live data could provide is not a today's chart snapshot, but a historical record of popularity over time. A scheduled ETL job (GitHub Actions + PostgreSQL) that pulls and stores daily chart data would enable questions no static CSV can answer: "how long do songs stay in the top 50?", "which songs rise fastest?"

**Resolve Spotify API restrictions.** Implementing Authorization Code Flow with PKCE would restore access to editorial playlist data and enable per-user personalization features currently blocked by the Development Mode restrictions.

**Predictive modeling.** A Random Forest or XGBoost model would provide feature importance scores capturing non-linear relationships that Pearson correlation misses. Given the weak correlations already found, the expected prediction accuracy is intentionally modest — the feature importance output is the valuable artifact, not the predictions.

**Artist fame as a control variable.** Artist popularity is likely a major confounding variable — a mediocre song by a famous artist will outscore a great song by an unknown one. Controlling for this would significantly improve the analytical rigor of every finding in the current dashboard.

---

## 👤 Author

**Benedict Huynh** — Computer Science student, Year 3.

Interested in Data Analytics, Data Engineering, and Software Engineering roles.

[![GitHub](https://img.shields.io/badge/GitHub-cucSdatJ-black?style=flat&logo=github)](https://github.com/cucSdatJ)

---

*Built with Python · Streamlit · Plotly · Spotify API · Last.fm API · Dataset: Kaggle Spotify Tracks*