import os
import time
import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from pathlib import Path

# Load API keys từ file .env vào environment variables
# Điều này phải được gọi trước khi bất kỳ os.getenv() nào được dùng
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

def get_spotify_client():
    """
    Create and return an authenticated Spotify client.

    SpotifyClientCredentials automatically handles token refresh —
    when the 1-hour access token expires, spotipy will silently
    fetch a new one without you needing to do anything.
    This is one of the key benefits of using a wrapper library
    over calling the raw HTTP endpoints yourself.
    """
    auth_manager = SpotifyClientCredentials(client_id=os.getenv("SPOTIFY_CLIENT_ID"), client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"))
    return spotipy.Spotify(auth_manager=auth_manager)


def fetch_top_charts(region: str = "global", limit: int = 20) -> pd.DataFrame:
    """
    Fetch current top tracks from a well-known Spotify charts playlist.

    Spotify doesn't expose a dedicated "charts" endpoint, but they maintain
    official editorial playlists like "Top 50 Global" that are updated daily.
    These playlist IDs are fixed and publicly documented.

    This means: when you call this function today vs tomorrow, you get
    different songs — making your dashboard truly live and current.
    """
    # Well-known Spotify editorial playlist IDs
    # These are stable — Spotify updates the content but keeps the same ID
    sp = get_spotify_client()
    region_config = {
        "global": {"query": "year:2024", "market": "US"},
        "vietnam": {"query": "genre:v-pop", "market": "VN"},
        "us": {"query": "genre:pop", "market": "US"},
        "uk": {"query": "genre:pop", "market": "GB"},
    }
    config = region_config.get(region, region_config["global"])
    tracks_data = []

    offsets = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180]
    for offset in offsets:
        try:
            results = sp.search(q=config["query"], type="track", market=config["market"], limit=limit, offset=offset)
            items = results.get("tracks", {}).get("items", [])
            if not items:
                break  # No more tracks to fetch
            for track in items:
                if track and track.get("id"):
                    tracks_data.append({
                    "track_id": track["id"],
                    "song_name": track["name"],
                    "song_popularity": track["popularity"],
                    "song_duration": track["duration_ms"]
                    })
                time.sleep(0.1)  # Sleep to respect rate limits
        except Exception as e:
            print(f"⚠️ Search error at offset {offset}: {e}")
            break
    if not tracks_data:
        print("⚠️ No tracks fetched from Spotify.")
        return pd.DataFrame()

    tracks_df = (
        pd.DataFrame(tracks_data).drop_duplicates(subset=["track_id"]).reset_index(drop=True)
    )

    print(f"✅ Fetched {len(tracks_df):,} unique tracks from Spotify ({region} charts).")

    tracks_ids = tracks_df["track_id"].tolist()
    audio_features_list = []
    for i in range(0, len(tracks_ids), 100):
        batch_ids = tracks_ids[i:i + 100]
        try:
            features = sp.audio_features(batch_ids)
            audio_features_list.extend(features or [])
            time.sleep(0.1)  # Sleep to respect rate limits
        except Exception as e:
            print(f"⚠️ Audio features error for batch starting at index {i}: {e}")
            continue
    if not audio_features_list:
        return pd.DataFrame()

    features_df = pd.DataFrame([f for f in audio_features_list if f is not None])

    features_df = features_df[[
        "id", "danceability", "energy", "key", "loudness",
        "mode", "speechiness", "acousticness",
        "instrumentalness", "liveness", "valence",
        "tempo", "time_signature"
    ]].rename(columns={"id": "track_id", "valence": "audio_valence"})

    result = (tracks_df.merge(features_df, on="track_id").drop(columns=["track_id"]).reset_index(drop=True))
    print(f"   ✅ Ready: {len(result)} tracks with full audio features")
    return result
