import pandas as pd

# ─────────────────────────────────────────────
# QUESTION 1: What does a viral song look like?
# Compare average audio features across popularity groups
# ─────────────────────────────────────────────
def feature_comparison_by_group(df):
    """
    Groups songs by popularity tier and computes the average value
    of each audio feature per group.
    This tells us: do viral songs tend to be more danceable? More energetic?
    """
    # These are the audio features we want to compare
    features = [
        "danceability", "energy", "acousticness",
        "speechiness", "liveness", "audio_valence", "tempo"
    ]

    result = (
        df.groupby("popularity_group", observed=True)[features]
        .mean()
        .round(3)
        .reset_index()
    )

    return result


# ─────────────────────────────────────────────
# QUESTION 2: Do happy songs get more plays than sad songs?
# Analyze audio_valence vs popularity
# ─────────────────────────────────────────────
def valence_vs_popularity(df):
    """
    Divides songs into 'Happy' (valence >= 0.5) and 'Sad' (valence < 0.5)
    then compares their average popularity scores.
    audio_valence: closer to 1.0 = happy/upbeat, closer to 0.0 = sad/dark
    """
    # Create a new mood label column based on valence threshold
    df = df.copy()  # avoid modifying the original dataframe
    df["mood"] = df["audio_valence"].apply(
        lambda v: "Happy (valence ≥ 0.5)" if v >= 0.5 else "Sad (valence < 0.5)"
    )

    result = (
        df.groupby("mood")["song_popularity"]
        .agg(
            avg_popularity="mean",
            song_count="count",
            median_popularity="median"
        )
        .round(2)
        .reset_index()
    )

    return result


# ─────────────────────────────────────────────
# QUESTION 3: Do shorter or longer songs perform better?
# Analyze duration_min vs popularity
# ─────────────────────────────────────────────
def duration_vs_popularity(df):
    """
    Bins songs into duration brackets (e.g. 1-2 min, 2-3 min, etc.)
    and computes average popularity per bracket.
    Helps answer: is there a "sweet spot" song length for popularity?
    """
    # pd.cut() divides continuous duration values into labeled brackets
    df = df.copy()
    df["duration_bracket"] = pd.cut(
        df["duration_min"],
        bins=[0, 2, 3, 4, 5, 10],
        labels=["< 2 min", "2–3 min", "3–4 min", "4–5 min", "> 5 min"]
    )

    result = (
        df.groupby("duration_bracket", observed=True)["song_popularity"]
        .agg(
            avg_popularity="mean",
            song_count="count"
        )
        .round(2)
        .reset_index()
    )

    return result


# ─────────────────────────────────────────────
# QUESTION 4: Which feature correlates most with popularity?
# Compute correlation matrix
# ─────────────────────────────────────────────
def correlation_with_popularity(df):
    """
    Calculates the Pearson correlation coefficient between song_popularity
    and every numeric audio feature.
    Correlation ranges from -1.0 to 1.0:
      +1.0 = as feature increases, popularity increases
      -1.0 = as feature increases, popularity decreases
       0.0 = no relationship
    """
    numeric_cols = [
        "danceability", "energy", "acousticness", "instrumentalness",
        "liveness", "loudness", "speechiness", "tempo",
        "audio_valence", "duration_min"
    ]

    # Calculate correlation of each feature against song_popularity only
    result = (
        df[numeric_cols + ["song_popularity"]]
        .corr()["song_popularity"]
        .drop("song_popularity")   # remove self-correlation (always = 1.0)
        .sort_values(ascending=False)
        .round(3)
        .reset_index()
    )
    result.columns = ["feature", "correlation"]

    return result


# ─────────────────────────────────────────────
# QUESTION 5: Do louder songs perform better?
# Analyze loudness (in dB) vs popularity
# ─────────────────────────────────────────────
def loudness_vs_popularity(df):
    """
    Loudness in this dataset is measured in decibels (dB), typically
    ranging from -60 to 0. Values closer to 0 mean louder songs.
    We bin the values into brackets to find if there's a "sweet spot".
    """
    df = df.copy()
    df["loudness_bracket"] = pd.cut(
        df["loudness"],
        bins=[-60, -20, -10, -5, 0],
        labels=["Very Quiet (< -20dB)", "Moderate (-20 to -10dB)",
                "Loud (-10 to -5dB)", "Very Loud (> -5dB)"]
    )

    result = (
        df.groupby("loudness_bracket", observed=True)["song_popularity"]
        .agg(avg_popularity="mean", song_count="count")
        .round(2)
        .reset_index()
    )
    return result


# ─────────────────────────────────────────────
# QUESTION 6: Do live recordings perform worse than studio tracks?
# Analyze liveness vs popularity
# ─────────────────────────────────────────────
def liveness_vs_popularity(df):
    """
    Liveness > 0.8 is Spotify's threshold for detecting a live recording.
    This question tests whether listeners prefer polished studio sound
    over the raw energy of a live performance.
    """
    df = df.copy()
    # Spotify considers liveness > 0.8 as "likely live"
    df["recording_type"] = df["liveness"].apply(
        lambda x: "Live Recording (liveness > 0.8)"
        if x > 0.8 else "Studio Recording (liveness ≤ 0.8)"
    )

    result = (
        df.groupby("recording_type")["song_popularity"]
        .agg(avg_popularity="mean", song_count="count", median_popularity="median")
        .round(2)
        .reset_index()
    )
    return result


# ─────────────────────────────────────────────
# QUESTION 7: Major key vs Minor key — which is more popular?
# Analyze audio_mode vs popularity
# ─────────────────────────────────────────────
def mode_vs_popularity(df):
    """
    audio_mode = 1 means the song is in a Major key (typically bright, happy)
    audio_mode = 0 means Minor key (typically darker, more emotional)
    This complements Q2 (valence) by looking at musical structure
    rather than just perceived mood.
    """
    df = df.copy()
    df["key_mode"] = df["audio_mode"].map({1: "Major (bright)", 0: "Minor (dark)"})

    result = (
        df.groupby("key_mode")["song_popularity"]
        .agg(avg_popularity="mean", song_count="count", median_popularity="median")
        .round(2)
        .reset_index()
    )
    return result


# ─────────────────────────────────────────────
# QUESTION 8: The 4 emotional zones of music
# Combine energy + valence to create mood quadrants
# ─────────────────────────────────────────────
def emotional_quadrant_analysis(df):
    """
    This is inspired by Russell's Circumplex Model of Affect in psychology,
    which maps emotions on two axes: valence (positive/negative) and
    arousal (high/low energy). We apply this to music:

      High energy + High valence = "Happy & Energetic" (e.g. party pop)
      High energy + Low valence  = "Dark & Intense"    (e.g. metal, aggressive rap)
      Low energy  + High valence = "Happy & Calm"      (e.g. acoustic pop, chill)
      Low energy  + Low valence  = "Sad & Slow"        (e.g. sad ballads, ambient)

    This is a much richer way to describe a song's emotional character
    than looking at valence or energy alone.
    """
    df = df.copy()

    # Use 0.5 as the midpoint threshold for both axes
    def assign_quadrant(row):
        high_energy = row["energy"] >= 0.5
        high_valence = row["audio_valence"] >= 0.5
        if high_energy and high_valence:
            return "Happy & Energetic"
        elif high_energy and not high_valence:
            return "Dark & Intense"
        elif not high_energy and high_valence:
            return "Happy & Calm"
        else:
            return "Sad & Slow"

    df["emotional_zone"] = df.apply(assign_quadrant, axis=1)

    result = (
        df.groupby("emotional_zone")["song_popularity"]
        .agg(avg_popularity="mean", song_count="count", median_popularity="median")
        .round(2)
        .reset_index()
        .sort_values("avg_popularity", ascending=False)
    )
    return result


# ─────────────────────────────────────────────
# QUESTION 9: Does combining danceability + energy create a "hit profile"?
# Define song "profiles" using multiple features at once
# ─────────────────────────────────────────────
def song_profile_analysis(df):
    """
    Instead of looking at one feature at a time, this function combines
    danceability, energy, and acousticness to create 3 song "profiles".

    Think of it like personality types for songs:
      - "Club Banger":    high danceability (≥0.7) AND high energy (≥0.7)
      - "Acoustic Chill": high acousticness (≥0.6) AND low energy (< 0.5)
      - "Everything Else": songs that don't fit either profile clearly

    This tests whether having a clear, strong identity helps a song succeed.
    """
    df = df.copy()

    def assign_profile(row):
        is_club = row["danceability"] >= 0.7 and row["energy"] >= 0.7
        is_acoustic = row["acousticness"] >= 0.6 and row["energy"] < 0.5
        if is_club:
            return "Club Banger (high dance + high energy)"
        elif is_acoustic:
            return "Acoustic Chill (high acoustic + low energy)"
        else:
            return "Mixed / Other"

    df["song_profile"] = df.apply(assign_profile, axis=1)

    result = (
        df.groupby("song_profile")["song_popularity"]
        .agg(avg_popularity="mean", song_count="count", median_popularity="median")
        .round(2)
        .reset_index()
        .sort_values("avg_popularity", ascending=False)
    )
    return result