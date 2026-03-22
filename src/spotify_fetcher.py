import os
import time
import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

# Load API keys từ file .env vào environment variables
# Điều này phải được gọi trước khi bất kỳ os.getenv() nào được dùng
load_dotenv()


def get_spotify_client():
    """
    Create and return an authenticated Spotify client.

    SpotifyClientCredentials automatically handles token refresh —
    when the 1-hour access token expires, spotipy will silently
    fetch a new one without you needing to do anything.
    This is one of the key benefits of using a wrapper library
    over calling the raw HTTP endpoints yourself.
    """
    client_id=os.getenv("SPOTIFY_CLIENT_ID")
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    token = auth_manager.get_access_token(as_dict=False)
    sp = spotipy.Spotify(auth=token)
    return sp

def fetch_playlist_tracks(playlist_id: str, sp=None) -> pd.DataFrame:
    """
    Fetch all tracks from a Spotify playlist and return their audio features.

    This is the core function. It works in two steps:

    Step 1: Get the list of tracks in the playlist. This gives us basic
    info like track name, artist, and popularity — but NOT audio features.

    Step 2: For each batch of tracks, call the audio_features() endpoint
    separately. Spotify separates these endpoints intentionally — you
    must make a second round of API calls to get danceability, energy, etc.

    Why batches? Spotify's audio_features() endpoint accepts up to 100
    track IDs per call. Processing in batches of 100 minimizes the number
    of API calls, which helps stay within Spotify's rate limits.
    """
    if sp is None:
        sp = get_spotify_client()

    tracks_data = []

    # --- Step 1: Paginate through the playlist ---
    # Spotify returns at most 100 tracks per request.
    # We keep calling with an increasing offset until results run out.
    offset = 0
    while True:
        response = sp.playlist_items(
            playlist_id,
            offset=offset,
            limit=100,
            market="US",  # market can affect which tracks are returned (e.g. region-locked content)
            fields="items(track(id,name,popularity,duration_ms)),next"
        )

        items = response.get("items", [])
        if not items:
            break  # no more tracks — exit the loop

        for item in items:
            track = item.get("track")
            # Some playlist slots can be empty (e.g. deleted tracks)
            if track and track.get("id"):
                tracks_data.append({
                    "track_id": track["id"],
                    "song_name": track["name"],
                    "song_popularity": track["popularity"],
                    "song_duration_ms": track["duration_ms"]
                })

        offset += len(items)

        # Respect Spotify's rate limits — pause briefly between pages
        # Without this, Spotify may return a 429 (Too Many Requests) error
        time.sleep(0.1)

    if not tracks_data:
        return pd.DataFrame()

    # --- Step 2: Fetch audio features in batches of 100 ---
    track_ids = [t["track_id"] for t in tracks_data]
    audio_features_list = []

    for i in range(0, len(track_ids), 100):
        batch = track_ids[i:i + 100]
        features = sp.audio_features(batch)
        audio_features_list.extend(features)
        time.sleep(0.1)  # rate limit protection

    # --- Step 3: Merge basic info with audio features ---
    tracks_df = pd.DataFrame(tracks_data)

    # audio_features() can return None for some tracks (e.g. podcasts)
    # We filter those out before building the features dataframe
    features_df = pd.DataFrame([
        f for f in audio_features_list if f is not None
    ])

    # Keep only the columns we actually use in our analysis
    features_df = features_df[[
        "id", "danceability", "energy", "key", "loudness",
        "audio_mode", "speechiness", "acousticness",
        "instrumentalness", "liveness", "valence",
        "tempo", "time_signature"
    ]].rename(columns={
        "id": "track_id",
        "valence": "audio_valence",  # match column name in our existing code
        "audio_mode": "audio_mode"
    })

    # Merge on track_id, then drop it — we don't need it downstream
    result = tracks_df.merge(features_df, on="track_id").drop(columns=["track_id"])

    return result


def fetch_top_charts(region: str = "global", limit: int = 50) -> pd.DataFrame:
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
    playlist_ids = {
        "global": "37i9dQZEVXbMDoHDwVN2tF",  # Top 50 Global
        "vietnam": "37i9dQZEVXbLdGSmz6xilI",  # Top 50 Vietnam
        "us": "37i9dQZEVXbLRQDuF5jeBp",  # Top 50 USA
        "uk": "37i9dQZEVXbLnolsZ8PSNw",  # Top 50 UK
    }

    playlist_id = playlist_ids.get(region, playlist_ids["global"])
    return fetch_playlist_tracks(playlist_id)