from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).parent.parent / "data" / "song_data.csv"


def load_and_clean(source: str = "csv", region: str = "global") -> pd.DataFrame:
    """
    Load and clean song data from either a local CSV or the live Spotify API.

    The `source` parameter acts as a switch:
      "csv" — reads from the static local file (fast, offline, reproducible)
      "api" — pulls fresh data from Spotify (slow, requires credentials, always current)

    Regardless of which source is used, the returned DataFrame has the
    same column names and structure — so queries.py and app.py never need
    to know or care where the data came from. This is the key design insight.
    """
    if source == "api":
        # Import here (not at top of file) to avoid requiring spotipy
        # for users who only want to use the CSV source
        from src.spotify_fetcher import fetch_top_charts
        print(f"🌐 Fetching live data from Spotify ({region} charts)...")
        df = fetch_top_charts(region=region)
    else:
        df = pd.read_csv(DATA_PATH)

    # --- All cleaning logic below is identical regardless of source ---
    df = df.dropna(subset=["song_name", "song_popularity"])
    df = df.drop_duplicates(subset=["song_name"], keep="first")
    df = df[df["tempo"] > 0]
    df = df[df["song_duration_ms"] >= 30000]
    df = df[df["song_duration_ms"] <= 600000]
    df["duration_min"] = (df["song_duration_ms"] / 60000).round(2)
    df["popularity_group"] = pd.cut(
        df["song_popularity"],
        bins=[0, 30, 60, 80, 100],
        labels=["Low (0–30)", "Medium (31–60)", "High (61–80)", "Viral (81–100)"]
    )
    df = df.reset_index(drop=True)

    print(f"✅ Clean dataset: {len(df):,} songs (source: {source})")
    return df