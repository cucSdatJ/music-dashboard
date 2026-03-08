import sys
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests
import streamlit.components.v1 as components

def load_lottie(url: str):
    """
    Fetch a Lottie animation JSON from lottiefiles.com.
    Returns None if the request fails so the app doesn't crash
    if the user is offline or the URL changes.
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# Load a music-themed Lottie animation for the header
lottie_music = load_lottie(
    "https://assets2.lottiefiles.com/packages/lf20_ikk4jhps.json"
)

# Add the project root to the Python path so we can import from src/
sys.path.append(".")
from src.load_data import load_and_clean
from src.queries import (
    feature_comparison_by_group,
    valence_vs_popularity,
    duration_vs_popularity,
    correlation_with_popularity,
    loudness_vs_popularity,
    liveness_vs_popularity,
    mode_vs_popularity,
    emotional_quadrant_analysis,
    song_profile_analysis
)

# ─────────────────────────────────────────────
# PAGE CONFIG
# This must be the very first Streamlit call in the script —
# placing any other st.* call before it will raise an error.
# layout="wide" tells Streamlit to use the full browser width,
# which gives our charts more room to breathe.
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Music Trend Dashboard",
    page_icon="🎵",
    layout="wide"
)

# ─────────────────────────────────────────────
# CUSTOM CSS ANIMATIONS
# We inject raw CSS into the Streamlit page using st.markdown.
# unsafe_allow_html=True is required to render actual HTML/CSS —
# without it, Streamlit would display the tags as plain text.
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── GLOBAL FONT & BACKGROUND ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── FADE + SLIDE UP: applied to every main block ──
   Every element fades in and slides up 20px when the page loads.
   animation-fill-mode: both means the element starts invisible
   before the animation begins, preventing a "flash" of content. */
[data-testid="stVerticalBlock"] > div {
    animation: fadeSlideUp 0.6s ease forwards;
    opacity: 0;
}

/* Stagger each block so they appear one after another, not all at once.
   nth-child selectors target blocks by their position in the layout. */
[data-testid="stVerticalBlock"] > div:nth-child(1) { animation-delay: 0.1s; }
[data-testid="stVerticalBlock"] > div:nth-child(2) { animation-delay: 0.2s; }
[data-testid="stVerticalBlock"] > div:nth-child(3) { animation-delay: 0.3s; }
[data-testid="stVerticalBlock"] > div:nth-child(4) { animation-delay: 0.4s; }
[data-testid="stVerticalBlock"] > div:nth-child(5) { animation-delay: 0.5s; }

@keyframes fadeSlideUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* ── METRIC CARDS: Glow on hover ──
   The [data-testid="metric-container"] selector targets Streamlit's
   built-in metric cards. We add a glowing border on hover to make
   the dashboard feel interactive even when nothing is clicked. */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 16px;
    transition: all 0.3s ease;
    cursor: default;
}

[data-testid="metric-container"]:hover {
    border-color: #7c3aed;
    box-shadow: 0 0 20px rgba(124, 58, 237, 0.4);
    transform: translateY(-3px);  /* subtle lift effect */
}

/* ── SIDEBAR: Glassmorphism effect ──
   Glassmorphism = frosted glass look, very popular in modern UI.
   backdrop-filter creates the blur effect behind the element. */
[data-testid="stSidebar"] {
    background: rgba(15, 15, 30, 0.85) !important;
    backdrop-filter: blur(10px);
    border-right: 1px solid rgba(255, 255, 255, 0.08);
}

/* ── TITLE: Gradient text animation ──
   The title text cycles through a purple-to-blue gradient. */
h1 {
    background: linear-gradient(135deg, #a78bfa, #60a5fa, #34d399);
    background-size: 200% 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradientShift 4s ease infinite;
}

@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* ── TABS: Animated underline on active tab ── */
[data-testid="stTabs"] button {
    transition: color 0.3s ease;
    position: relative;
}

[data-testid="stTabs"] button::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0;
    width: 0; height: 2px;
    background: linear-gradient(90deg, #7c3aed, #60a5fa);
    transition: width 0.3s ease;
}

[data-testid="stTabs"] button:hover::after,
[data-testid="stTabs"] button[aria-selected="true"]::after {
    width: 100%;
}

/* ── PLOTLY CHARTS: Smooth container appearance ── */
[data-testid="stPlotlyChart"] {
    border-radius: 12px;
    overflow: hidden;
    transition: box-shadow 0.3s ease;
}

[data-testid="stPlotlyChart"]:hover {
    box-shadow: 0 8px 32px rgba(124, 58, 237, 0.2);
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LOAD DATA
# @st.cache_data is a performance decorator. Without it, Streamlit
# re-runs the entire script (including reading the CSV) every time
# the user interacts with a slider or dropdown. With it, the cleaned
# dataframe is stored in memory and reused across interactions.
# ─────────────────────────────────────────────
@st.cache_data
def get_data():
    return load_and_clean()

df = get_data()

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
# Animated header: Lottie on the left, title text on the right
header_left, header_right = st.columns([1, 3])
with header_left:
    if lottie_music:
        st_lottie(lottie_music, height=120, key="header_anim")
with header_right:
    st.title("🎵 Music Trend Dashboard")
    st.markdown(
        "Analyzing **13,051 songs** to uncover what makes "
        "a track successful on Spotify."
    )

# ─────────────────────────────────────────────
# SIDEBAR — global filters
# These sliders apply to every chart on the dashboard simultaneously.
# This is more powerful than static reports: the viewer can narrow
# the data to a specific subset and watch all charts update at once.
# ─────────────────────────────────────────────
st.sidebar.header("🎛️ Filters")

# Popularity range filter
popularity_range = st.sidebar.slider(
    "Filter by Popularity",
    min_value=0, max_value=100,
    value=(0, 100),
    help="Drag to show only songs within this popularity range"
)

# Energy range filter
energy_range = st.sidebar.slider(
    "Filter by Energy",
    min_value=0.0, max_value=1.0,
    value=(0.0, 1.0), step=0.05
)

# Apply both filters to create the filtered dataframe used by all charts
df_filtered = df[
    (df["song_popularity"].between(*popularity_range)) &
    (df["energy"].between(*energy_range))
]

# Show how many songs remain after filtering so the user understands
# the size of the subset they are looking at
st.sidebar.metric(
    "Songs after filtering",
    f"{len(df_filtered):,}",
    delta=f"{len(df_filtered) - len(df):,} vs total"
)


# ─────────────────────────────────────────────
# ANIMATED METRIC CARDS
# We use st.components.v1.html() instead of st.markdown() because
# st.markdown() strips <script> tags in newer Streamlit versions.
# components.html() renders inside a sandboxed iframe where JavaScript
# is fully supported — this is the correct approach for any HTML+JS.
# ─────────────────────────────────────────────
total_songs = len(df_filtered)
avg_pop = df_filtered['song_popularity'].mean()
viral_count = int((df_filtered['song_popularity'] > 80).sum())
avg_dance = df_filtered['danceability'].mean()

components.html(f"""
<!DOCTYPE html>
<html>
<head>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    * {{ margin: 0; padding: 0; box-sizing: border-box; }}

    body {{
        font-family: 'Inter', sans-serif;
        background: transparent;
    }}

    .grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        padding: 8px;
    }}

    .card {{
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        opacity: 0;
        animation: fadeSlideUp 0.6s ease forwards;
        cursor: default;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }}

    .card:hover {{
        transform: translateY(-4px);
    }}

    /* Each card has a unique color theme */
    .card-1 {{
        background: linear-gradient(135deg, #1a1a2e, #0f3460);
        border: 1px solid rgba(124,58,237,0.3);
        animation-delay: 0.1s;
    }}
    .card-1:hover {{ box-shadow: 0 0 24px rgba(124,58,237,0.4); }}

    .card-2 {{
        background: linear-gradient(135deg, #1a1a2e, #1e3a5f);
        border: 1px solid rgba(96,165,250,0.3);
        animation-delay: 0.2s;
    }}
    .card-2:hover {{ box-shadow: 0 0 24px rgba(96,165,250,0.4); }}

    .card-3 {{
        background: linear-gradient(135deg, #1a1a2e, #3b1a1a);
        border: 1px solid rgba(239,68,68,0.3);
        animation-delay: 0.3s;
    }}
    .card-3:hover {{ box-shadow: 0 0 24px rgba(239,68,68,0.4); }}

    .card-4 {{
        background: linear-gradient(135deg, #1a1a2e, #1a3a2e);
        border: 1px solid rgba(52,211,153,0.3);
        animation-delay: 0.4s;
    }}
    .card-4:hover {{ box-shadow: 0 0 24px rgba(52,211,153,0.4); }}

    .emoji {{
        font-size: 2.2rem;
        margin-bottom: 8px;
    }}

    /* The fire emoji pulses continuously to draw attention */
    .pulse {{
        animation: pulse 1.5s ease infinite;
        display: inline-block;
    }}

    .number {{
        font-size: 2rem;
        font-weight: 700;
        margin: 8px 0;
    }}

    .label {{
        color: #94a3b8;
        font-size: 0.82rem;
        letter-spacing: 0.5px;
    }}

    .c1 {{ color: #a78bfa; }}
    .c2 {{ color: #60a5fa; }}
    .c3 {{ color: #f87171; }}
    .c4 {{ color: #34d399; }}

    @keyframes fadeSlideUp {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to   {{ opacity: 1; transform: translateY(0); }}
    }}

    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); }}
        50%       {{ transform: scale(1.25); }}
    }}
</style>
</head>
<body>
<div class="grid">

    <div class="card card-1">
        <div class="emoji">🎵</div>
        <div class="number c1" id="n1">0</div>
        <div class="label">Total Songs</div>
    </div>

    <div class="card card-2">
        <div class="emoji">⭐</div>
        <div class="number c2" id="n2">0</div>
        <div class="label">Avg Popularity / 100</div>
    </div>

    <div class="card card-3">
        <div class="emoji"><span class="pulse">🔥</span></div>
        <div class="number c3" id="n3">0</div>
        <div class="label">Viral Songs (&gt;80)</div>
    </div>

    <div class="card card-4">
        <div class="emoji">💃</div>
        <div class="number c4" id="n4">0.00</div>
        <div class="label">Avg Danceability</div>
    </div>

</div>

<script>
    // countUp animates a number from 0 to its target over `duration` ms.
    // easeOutQuart gives a fast start and smooth slow finish —
    // much more satisfying to watch than a linear count.
    function countUp(id, target, duration, decimals) {{
        const el = document.getElementById(id);
        const start = performance.now();
        function tick(now) {{
            const progress = Math.min((now - start) / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 4);
            const value = eased * target;
            el.textContent = decimals > 0
                ? value.toFixed(decimals)
                : Math.round(value).toLocaleString();
            if (progress < 1) requestAnimationFrame(tick);
        }}
        requestAnimationFrame(tick);
    }}

    // Wait for cards to finish fading in before starting the counters
    setTimeout(() => {{
        countUp("n1", {total_songs}, 1500, 0);
        countUp("n2", {avg_pop:.1f}, 1500, 1);
        countUp("n3", {viral_count}, 1500, 0);
        countUp("n4", {avg_dance:.4f}, 1500, 2);
    }}, 500);
</script>
</body>
</html>
""", height=160)  # adjust height if cards feel cramped

# ─────────────────────────────────────────────
# TABS
# Organizing charts into tabs prevents the page from becoming one
# endless scroll. Each tab groups related questions together, making
# it easier for the viewer to follow the analytical narrative.
# ─────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "🧬 Viral Song DNA",
    "😊 Emotion & Music",
    "🔬 Deep Dive"
])


# ═══════════════════════════════════════════
# TAB 1: Viral Song DNA
# Core question: what audio features separate viral songs from the rest?
# ═══════════════════════════════════════════
with tab1:
    st.header("🧬 The DNA of a Viral Song")
    st.markdown(
        "Compare audio features across popularity tiers to identify "
        "the characteristics that define a successful track."
    )

    # Chart 1A: Feature comparison across popularity groups
    # The selectbox makes this chart interactive — the viewer can
    # explore each feature themselves rather than being shown a fixed view.
    st.subheader("Audio Features by Popularity Group")
    feature_data = feature_comparison_by_group(df_filtered)

    selected_feature = st.selectbox(
        "Select a feature to compare:",
        options=["danceability", "energy", "acousticness",
                 "speechiness", "liveness", "audio_valence", "tempo"],
        index=0
    )

    fig1 = px.bar(
        feature_data,
        x="popularity_group",
        y=selected_feature,
        color="popularity_group",
        title=f"Average '{selected_feature}' by Popularity Group",
        color_discrete_sequence=px.colors.sequential.Viridis,
        text_auto=".3f"
    )
    fig1.update_layout(showlegend=False, xaxis_title="Popularity Group")
    st.plotly_chart(fig1, use_container_width=True)

    # Chart 1B: Correlation bar chart
    # Green = positively correlated with popularity (higher = more popular)
    # Red   = negatively correlated (higher = less popular)
    # The vertical line at x=0 is a visual anchor to make direction obvious.
    st.subheader("Feature Correlation with Popularity")
    corr_data = correlation_with_popularity(df_filtered)

    corr_data["direction"] = corr_data["correlation"].apply(
        lambda x: "Positive correlation" if x > 0 else "Negative correlation"
    )
    fig2 = px.bar(
        corr_data,
        x="correlation", y="feature",
        orientation="h",
        color="direction",
        color_discrete_map={
            "Positive correlation": "#2ecc71",
            "Negative correlation": "#e74c3c"
        },
        title="Pearson Correlation of Each Feature with Song Popularity",
        text_auto=".3f"
    )
    fig2.add_vline(x=0, line_dash="dash", line_color="gray")
    fig2.update_layout(yaxis_title="", xaxis_title="Pearson Correlation Coefficient")
    st.plotly_chart(fig2, use_container_width=True)

    # Chart 1C: Song profiles
    # Instead of one feature at a time, this groups songs by a
    # combined multi-feature "personality" to test whether having
    # a clear sonic identity helps a song perform better.
    st.subheader("Popularity by Song Profile")
    profile_data = song_profile_analysis(df_filtered)
    fig3 = px.bar(
        profile_data,
        x="song_profile", y="avg_popularity",
        color="song_profile",
        title="Average Popularity by Song Profile",
        text_auto=".1f",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig3.update_layout(showlegend=False, xaxis_title="")
    st.plotly_chart(fig3, use_container_width=True)


# ═══════════════════════════════════════════
# TAB 2: Emotion & Music
# Core question: does the emotional character of a song affect popularity?
# ═══════════════════════════════════════════
with tab2:
    st.header("😊 Emotion & Music")
    st.markdown(
        "Explore the relationship between a song's emotional character "
        "and its popularity — some results may surprise you."
    )

    left, right = st.columns(2)

    # Chart 2A: Happy vs Sad
    # audio_valence is Spotify's measure of musical positivity.
    # Values near 1.0 sound happy/upbeat; values near 0.0 sound sad/dark.
    with left:
        st.subheader("Happy vs Sad — Who Wins?")
        valence_data = valence_vs_popularity(df_filtered)
        fig4 = px.bar(
            valence_data,
            x="mood", y="avg_popularity",
            color="mood",
            title="Average Popularity: Happy vs Sad Songs",
            text_auto=".1f",
            color_discrete_map={
                "Happy (valence ≥ 0.5)": "#f39c12",
                "Sad (valence < 0.5)": "#8e44ad"
            }
        )
        fig4.update_layout(showlegend=False, xaxis_title="")
        st.plotly_chart(fig4, use_container_width=True)

    # Chart 2B: Major vs Minor key distribution as a pie chart
    # A pie chart works well here because we only have two categories
    # and the proportion (not the magnitude) is what matters.
    with right:
        st.subheader("Major Key vs Minor Key")
        mode_data = mode_vs_popularity(df_filtered)
        fig5 = px.pie(
            mode_data,
            names="key_mode",
            values="song_count",
            title="Song Distribution by Key Mode",
            color_discrete_sequence=["#3498db", "#e74c3c"]
        )
        st.plotly_chart(fig5, use_container_width=True)

    # Chart 2C: Emotional quadrants
    # This is the most theoretically grounded chart in the dashboard.
    # It applies Russell's Circumplex Model of Affect — a well-known
    # psychology framework — to music data. Mentioning this in an
    # interview shows you can connect data science to real-world theory.
    st.subheader("The 4 Emotional Zones of Music")
    st.caption(
        "Based on Russell's Circumplex Model of Affect — songs are classified "
        "on two axes: Energy (high/low) and Valence (positive/negative)"
    )
    quad_data = emotional_quadrant_analysis(df_filtered)
    fig6 = px.bar(
        quad_data,
        x="emotional_zone", y="avg_popularity",
        color="emotional_zone",
        title="Average Popularity by Emotional Zone",
        text_auto=".1f",
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig6.update_layout(showlegend=False, xaxis_title="")
    st.plotly_chart(fig6, use_container_width=True)

    # Chart 2D: Scatter plot — valence vs popularity
    # This is the only chart that shows every individual song rather than
    # just group averages. The OLS trend line will visually confirm what
    # Q4's correlation numbers already told us: the relationship between
    # valence and popularity is very weak (near-horizontal line).
    st.subheader("Scatter Plot: Valence vs Popularity")
    st.caption(
        "Each dot represents one song. Unlike bar charts that show averages, "
        "this reveals the full spread and distribution of the data."
    )

    # Sample 2,000 points to avoid slowing down the browser with 13k dots
    df_sample = df_filtered.sample(min(2000, len(df_filtered)), random_state=42)
    fig7 = px.scatter(
        df_sample,
        x="audio_valence", y="song_popularity",
        opacity=0.4,
        trendline="ols",  # OLS = Ordinary Least Squares regression line
        title="Valence vs Popularity (sample of 2,000 songs)",
        labels={
            "audio_valence": "Valence (0 = sad, 1 = happy)",
            "song_popularity": "Popularity"
        }
    )
    st.plotly_chart(fig7, use_container_width=True)


# ═══════════════════════════════════════════
# TAB 3: Deep Dive
# Core question: how do structural song properties affect popularity?
# ═══════════════════════════════════════════
with tab3:
    st.header("🔬 Deep Dive")

    left2, right2 = st.columns(2)

    # Chart 3A: Duration vs Popularity
    # Tests whether there is a "sweet spot" song length for streaming success.
    with left2:
        st.subheader("Song Duration vs Popularity")
        dur_data = duration_vs_popularity(df_filtered)
        fig8 = px.bar(
            dur_data,
            x="duration_bracket", y="avg_popularity",
            title="Average Popularity by Song Length",
            text_auto=".1f",
            color="avg_popularity",
            color_continuous_scale="Blues"
        )
        fig8.update_layout(xaxis_title="Duration", coloraxis_showscale=False)
        st.plotly_chart(fig8, use_container_width=True)

    # Chart 3B: Loudness vs Popularity
    # Loudness is measured in dB (decibels). Values closer to 0 are louder.
    # This tests the "loudness war" hypothesis in modern music production.
    with right2:
        st.subheader("Loudness vs Popularity")
        loud_data = loudness_vs_popularity(df_filtered)
        fig9 = px.bar(
            loud_data,
            x="loudness_bracket", y="avg_popularity",
            title="Average Popularity by Loudness (dB)",
            text_auto=".1f",
            color="avg_popularity",
            color_continuous_scale="Reds"
        )
        fig9.update_layout(xaxis_title="Loudness", coloraxis_showscale=False)
        st.plotly_chart(fig9, use_container_width=True)

    # Chart 3C: Live vs Studio
    # Spotify flags tracks with liveness > 0.8 as likely live recordings.
    # This tests whether the polished quality of studio recordings
    # gives songs an advantage on streaming platforms.
    st.subheader("Studio vs Live Recordings")
    live_data = liveness_vs_popularity(df_filtered)
    fig10 = px.bar(
        live_data,
        x="recording_type", y="avg_popularity",
        color="recording_type",
        title="Average Popularity: Studio vs Live Recordings",
        text_auto=".1f",
        color_discrete_sequence=["#27ae60", "#e67e22"]
    )
    fig10.update_layout(showlegend=False, xaxis_title="")
    st.plotly_chart(fig10, use_container_width=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.divider()
st.caption(
    "Built with Python · Streamlit · Plotly  |  "
    "Dataset: Kaggle · Spotify  |  Author: Benedict Huynh"
)