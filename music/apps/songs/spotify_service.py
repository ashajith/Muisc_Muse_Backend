import requests
import base64
from django.conf import settings
from django.core.cache import cache

SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_BASE_URL = "https://api.spotify.com/v1"


def get_cached_token():
    token = cache.get("spotify_token")
    if token:
        return token

    auth_str = f"{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()

    response = requests.post(
        SPOTIFY_TOKEN_URL,
        headers={"Authorization": f"Basic {b64_auth}"},
        data={"grant_type": "client_credentials"},
        timeout=20,
    )

    if response.status_code != 200:
        print("TOKEN ERROR:", response.text)
        return None

    data = response.json()
    token = data.get("access_token")
    cache.set("spotify_token", token, timeout=3500)
    return token


def spotify_request(endpoint, params=None):
    token = get_cached_token()
    if not token:
        return None

    response = requests.get(
        f"{SPOTIFY_BASE_URL}/{endpoint}",
        headers={"Authorization": f"Bearer {token}"},
        params=params,
        timeout=20,
    )

    if response.status_code != 200:
        print("SPOTIFY ERROR:", response.status_code, response.text)
        return None

    return response.json()


# TRACKS
def get_spotify_tracks(query="top songs", limit=10):
    data = spotify_request("search", {"q": query, "type": "track", "limit": limit})
    if not data:
        return []

    return [
        {
            "id": item["id"],
            "title": item["name"],
            "artist": item["artists"][0]["name"],
            "cover_image": item["album"]["images"][0]["url"] if item["album"]["images"] else None,
        }
        for item in data.get("tracks", {}).get("items", [])
    ]


# ARTISTS
def get_artists(limit=8):
    artist_queries = [
        "Arijit Singh", "Shreya Ghoshal", "A.R. Rahman",
        "Taylor Swift", "Bruno Mars", "The Weeknd",
        "Udit Narayan", "Lata Mangeshkar"
    ]
    artists = []
    for query in artist_queries[:limit]:
        data = spotify_request("search", {"q": query, "type": "artist", "limit": 1})
        if not data:
            continue
        items = data.get("artists", {}).get("items", [])
        if not items or not items[0]["images"]:
            continue
        artist = items[0]
        artists.append({
            "name": artist["name"],
            "image": artist["images"][0]["url"],
        })
    return artists


# PLAYLISTS
# PLAYLISTS
def get_playlists(limit=10):
    playlist_queries = [
        "Bollywood Party Hits",
        "Top Hindi Songs 2026",
        "Punjabi Hits",
        "Arijit Singh Best Songs",
        "Romantic Bollywood",
        "90s Hindi Hits",
        "Workout Hindi Songs",
        "Chill Bollywood",
        "Item Songs Bollywood",
        "Bollywood Love Songs",
    ]

    playlists = []
    for query in playlist_queries[:limit]:
        data = spotify_request("search", {
            "q": query, "type": "track", "limit": 1, "market": "IN"
        })
        if not data:
            continue
        items = data.get("tracks", {}).get("items", [])
        if not items or not items[0]:
            continue
        track = items[0]
        playlists.append({
            "id": query.replace(" ", "-").lower(),
            "name": query,
            "image": track["album"]["images"][0]["url"] if track.get("album", {}).get("images") else None,
            "description": "",
        })
    return playlists


def _map_track_to_song(track, date_added=None):
    if not track or track.get("type") != "track":
        return None

    return {
        "id": track["id"],
        "title": track["name"],
        "artist": {
            "name": ", ".join(a["name"] for a in track.get("artists", []))
        },
        "album": track.get("album", {}).get("name", ""),
        "image": (
            track["album"]["images"][0]["url"]
            if track.get("album", {}).get("images")
            else None
        ),
        "duration": track["duration_ms"] // 1000,
        "explicit": track.get("explicit", False),
        "date_added": date_added,
        "audio_url": track.get("preview_url"),
    }


# PLAYLIST DETAIL
def get_playlist_detail(playlist_id):
    # Convert fake ID back to query string
    query = playlist_id.replace("-", " ")

    # Search tracks by query
    tracks_data = spotify_request("search", {
        "q": query,
        "type": "track",
        "limit": 10,
        "market": "IN",
    })

    songs = []
    if tracks_data:
        for track in tracks_data.get("tracks", {}).get("items", []):
            if not track:
                continue
            songs.append({
                "id": track["id"],
                "title": track["name"],
                "artist": {
                    "name": ", ".join(a["name"] for a in track.get("artists", []))
                },
                "album": track.get("album", {}).get("name", ""),
                "image": (
                    track["album"]["images"][0]["url"]
                    if track.get("album", {}).get("images")
                    else None
                ),
                "duration": track["duration_ms"] // 1000,
                "explicit": track.get("explicit", False),
                "date_added": None,
                "audio_url": track.get("preview_url"),
            })

    return {
        "playlist": {
            "id": playlist_id,
            "name": query.title(),
            "description": "",
            "image": songs[0]["image"] if songs else None,
        },
        "songs": songs,
    }