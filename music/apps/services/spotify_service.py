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
def get_playlists(limit=10):
    playlist_queries = [
        "Top Hits India", "Bollywood Hits", "Today's Top Hits",
        "Chill Hits", "Party Hits", "Romance Hits",
        "90s Hits", "Workout Hits", "Pop Hits", "Punjabi Hits",
    ]
    playlists = []
    for query in playlist_queries[:limit]:
        data = spotify_request("search", {
            "q": query, "type": "playlist", "limit": 5, "market": "IN"
        })
        if not data:
            continue

        items = data.get("playlists", {}).get("items", [])
        if not items:
            continue

        playlist = next((item for item in items if item and item.get("id")), None)
        if not playlist:
            continue

        playlists.append({
            "id": playlist["id"],
            "name": playlist["name"],
            "image": playlist["images"][0]["url"] if playlist.get("images") else None,
            "description": playlist.get("description", ""),
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
        "audio_url": None,
    }


# PLAYLIST DETAIL
def get_playlist_detail(playlist_id):
    playlist_data = spotify_request(f"playlists/{playlist_id}", {
        "market": "IN",
    })

    if not playlist_data:
        return None

    tracks_data = spotify_request(f"playlists/{playlist_id}/tracks", {
        "market": "IN",
        "limit": 50,
    })

    songs = []
    if tracks_data:
        for item in tracks_data.get("items", []):
            mapped = _map_track_to_song(item.get("track"), item.get("added_at"))
            if mapped:
                songs.append(mapped)

    # Some Spotify app modes can read playlist metadata but not playlist tracks.
    # Fallback to track search by playlist name so playlist detail is still usable.
    if not songs:
        fallback_tracks = spotify_request("search", {
            "q": playlist_data.get("name", ""),
            "type": "track",
            "limit": 10,
            "market": "IN",
        })
        if fallback_tracks:
            for track in fallback_tracks.get("tracks", {}).get("items", []):
                mapped = _map_track_to_song(track)
                if mapped:
                    songs.append(mapped)

    return {
        "playlist": {
            "id": playlist_data["id"],
            "name": playlist_data["name"],
            "description": playlist_data.get("description", ""),
            "image": (
                playlist_data["images"][0]["url"]
                if playlist_data.get("images")
                else None
            ),
        },
        "songs": songs,
    }
