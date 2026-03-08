import pandas as pd
from pathlib import Path
DATA_PATH = Path(__file__).parent.parent / "data" / "song_data.csv"
def load_and_clean():
    df = pd.read_csv(DATA_PATH)

    # Drop rows missing critical columns — even though this dataset has none,
    # this is good defensive programming practice for any future data updates
    df = df.dropna(subset=["song_name", "song_popularity"])

    # Remove duplicate songs by name, keeping only the first occurrence
    df = df.drop_duplicates(subset=["song_name"], keep="first")

    # Remove songs with tempo = 0, which is physically impossible and signals bad data
    df = df[df["tempo"] > 0]

    # Remove songs shorter than 30 seconds (30,000 ms) — likely data errors or sound effects
    df = df[df["song_duration_ms"] >= 30000]

    # Remove songs longer than 10 minutes (600,000 ms) — likely live versions or podcasts
    # that would skew the duration analysis
    df = df[df["song_duration_ms"] <= 600000]

    # Convert duration from milliseconds to minutes for easier human interpretation
    df["duration_min"] = (df["song_duration_ms"] / 60000).round(2)

    # Create a categorical popularity column by dividing scores into 4 meaningful groups
    # This is basic feature engineering — turning a continuous number into a useful label
    # pd.cut() assigns each song to a bin based on its popularity score
    df["popularity_group"] = pd.cut(
        df["song_popularity"],
        bins=[0, 30, 60, 80, 100],
        labels=["Low (0–30)", "Medium (31–60)", "High (61–80)", "Viral (81–100)"]
    )

    # Reset the index after filtering so row numbers are clean and sequential (0, 1, 2, ...)
    # Without this, deleted rows leave "gaps" in the index which can cause bugs later
    df = df.reset_index(drop=True)

    # Print a quick summary to confirm the cleaning worked as expected
    print(f"✅ Clean dataset: {len(df):,} songs")
    print(f"   Average popularity: {df['song_popularity'].mean():.1f}")
    print(f"   Viral songs (>80): {(df['song_popularity'] > 80).sum():,}")

    return df