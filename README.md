# 🎵 Music Trend Dashboard

> An interactive data analytics dashboard analyzing **13,051 Spotify tracks** to uncover what makes a song go viral — built with Python, Streamlit, and Plotly.

🔗 **[Live Demo](https://music-dashboard-cucsdatj.streamlit.app/)** &nbsp;|&nbsp; ⭐ Star this repo if you find it useful!

---

## 📌 Project Overview

What separates a viral song from one that nobody hears? Is it the beat, the mood, the loudness — or something else entirely?

This project approaches that question as a data problem. Starting from a raw dataset of 13,051 Spotify tracks, I built a full end-to-end data analytics pipeline: cleaning and validating the data, designing and running 9 targeted analyses, and presenting the findings through an interactive web dashboard that anyone can explore without writing a single line of code.

The dashboard is organized around three analytical threads. The first examines the **technical DNA of viral songs** — comparing audio features like danceability, energy, and acousticness across popularity tiers to find what separates top-performing tracks from the rest. The second explores **emotion and music** — using Spotify's valence and energy scores to map songs onto emotional quadrants inspired by Russell's Circumplex Model of Affect, then testing whether emotional character predicts popularity. The third takes a **structural deep dive** into duration, loudness, and recording type to find practical patterns in what streaming listeners prefer.

---

## 🔍 Key Findings

These are the real insights extracted from the data — not assumed, but discovered through analysis.

**Viral songs are significantly more danceable.** Tracks in the top popularity tier (81–100) have an average danceability score of 0.699, compared to 0.616 for the lowest tier — a 13% difference that was the strongest structural predictor of popularity in the dataset.

**Sad songs outperform happy ones.** Songs with low valence (sad/dark mood) averaged a popularity score of 49.38, meaningfully higher than the 47.77 average for upbeat songs. This finding aligns with psychological research on the "sad music paradox" — people frequently turn to music to process negative emotions, not just to feel good.

**Dark and intense music dominates streaming.** When songs are classified into four emotional quadrants (combining energy and valence axes), "Sad & Slow" and "Dark & Intense" tracks rank first and second in average popularity, while "Happy & Calm" ranks last at 44.74. The stereotype that pop music is universally upbeat does not hold in this data.

**The sweet spot for song length is 3–5 minutes.** Songs in the 3–4 minute and 4–5 minute brackets both average around 49.4 in popularity, while tracks shorter than 2 minutes or longer than 5 minutes underperform — consistent with radio and streaming industry norms.

**Louder masters perform better.** Songs with loudness above -5 dB average a popularity of 50.72, while moderate-loudness tracks (-20 to -10 dB) average only 45.58. This supports the well-documented "loudness war" trend in modern music production.

**No single feature predicts popularity on its own.** The highest Pearson correlation between any audio feature and popularity was only 0.051 (danceability). This finding is itself meaningful: viral success is multidimensional and cannot be reduced to a single formula.

---

## 🛠️ Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| Data source | Kaggle (Spotify Tracks Dataset) | Raw data |
| Data cleaning | Python, Pandas | EDA, validation, feature engineering |
| Analysis | Pandas, NumPy | Groupby aggregations, correlation analysis |
| Visualization | Plotly Express | Interactive charts |
| Dashboard | Streamlit | Web application framework |
| Animations | CSS keyframes, JavaScript, streamlit-lottie | UI effects |
| Statistical modeling | statsmodels | OLS trendline on scatter plot |
| Deployment | Streamlit Cloud | Free public hosting |
| Version control | Git, GitHub | Source control |

---

## 📁 Project Structure

```
music-dashboard/
│
├── data/
│   └── song_data.csv           # Raw dataset (13,051 Spotify tracks)
│
├── notebooks/
│   └── 01_data_exploration.ipynb  # EDA and function testing
│
├── src/
│   ├── load_data.py            # Data cleaning and feature engineering
│   └── queries.py              # All 9 analysis functions
│
├── app.py                      # Streamlit dashboard (main entry point)
├── requirements.txt            # Python dependencies
└── README.md
```

The architecture follows a **separation of concerns** principle: `load_data.py` handles all data validation and cleaning, `queries.py` contains pure analytical logic, and `app.py` is responsible only for rendering. This means each layer can be tested, modified, or replaced independently.

---

## 📊 Dashboard Features

The dashboard has three tabs, each telling a different chapter of the same story.

**Viral Song DNA** contains an interactive bar chart where users can select any audio feature and compare its average across all four popularity tiers, a horizontal correlation chart colored by direction (green = positive, red = negative), and a song profile comparison that groups tracks into archetypes like "Club Banger" and "Acoustic Chill."

**Emotion & Music** contains a Happy vs Sad popularity comparison, a Major vs Minor key distribution pie chart, the four emotional quadrant analysis, and a scatter plot of all 2,000 sampled songs with an OLS regression trendline to visualize correlation strength visually.

**Deep Dive** contains duration bracket analysis, loudness level analysis, and a live vs studio recording comparison.

All charts respond to **two global sidebar filters** — popularity range and energy range — so the viewer can dynamically narrow the dataset and watch every chart update simultaneously.

---

## ⚙️ Setup & Installation

To run this project locally, clone the repository and set up a Python virtual environment.

```bash
# Clone the repo
git clone https://github.com/cucSdatJ/music-dashboard.git
cd music-dashboard

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

The dashboard will open automatically at `http://localhost:8501`.

---

## 📈 Analysis Functions (`src/queries.py`)

Each of the 9 analysis functions is documented with its analytical intent. Here is a summary of what each one answers.

`feature_comparison_by_group` answers: do viral songs have measurably different audio profiles than unpopular ones? `valence_vs_popularity` answers: do happy songs outperform sad songs on streaming? `duration_vs_popularity` answers: is there an optimal song length for popularity? `correlation_with_popularity` answers: which single feature has the strongest linear relationship with popularity? `loudness_vs_popularity` answers: does the loudness war hypothesis hold in this dataset? `liveness_vs_popularity` answers: do listeners prefer studio recordings over live ones? `mode_vs_popularity` answers: does major vs minor key affect popularity? `emotional_quadrant_analysis` answers: which of the four emotional archetypes (based on Russell's model) performs best? `song_profile_analysis` answers: do songs with a clear, strong sonic identity outperform mixed-profile tracks?

---

## 💡 What I Learned

This project taught me that the hardest part of data analysis is not writing code — it is asking the right questions before writing any code at all. The most interesting findings (the sad music paradox, the emotional quadrant rankings) came from questions I designed deliberately, not from running generic statistics on every column.

I also learned the difference between a number and an insight. A correlation of 0.051 between danceability and popularity is a number. The insight is that no single feature predicts viral success, which means trying to engineer a hit song by optimizing one variable at a time is fundamentally the wrong strategy.

---

## 🔮 Future Improvements

Given more time and data, there are three directions I would explore. First, integrating live data from the Spotify API to replace the static CSV with a real-time pipeline that updates daily. Second, building a simple ML model (Random Forest or XGBoost) to predict popularity from audio features, which would let me quantify feature importance more rigorously than Pearson correlation allows. Third, adding artist and genre dimensions — the current dataset lacks those columns, which limits the depth of segmentation possible.

---

## 👤 Author

**Benedict Huynh** — Computer Science student, Year 3.

Interested in Data Analytics, Data Engineering, and Software Engineering roles.

[![GitHub](https://img.shields.io/badge/GitHub-cucSdatJ-black?style=flat&logo=github)](https://github.com/cucSdatJ)

---

*Built with Python · Streamlit · Plotly · Dataset: Kaggle Spotify Tracks*
