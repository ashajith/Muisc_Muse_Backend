import requests
from django.conf import settings
from django.core.cache import cache

YOUTUBE_BASE_URL = "https://www.googleapis.com/youtube/v3"


def youtube_request(endpoint, params):
    """Base helper — injects API key and caches nothing (caller handles caching)."""
    api_key = settings.YOUTUBE_API_KEY
    if not api_key:
        print("YOUTUBE ERROR: YOUTUBE_API_KEY is not set in settings.")
        return None

    response = requests.get(
        f"{YOUTUBE_BASE_URL}/{endpoint}",
        params={**params, "key": api_key},
        timeout=20,
    )

    if response.status_code != 200:
        print("YOUTUBE ERROR:", response.status_code, response.text)
        return None

    return response.json()


# ── TRENDING MUSIC VIDEOS ──────────────────────────────────────────────────────
def get_youtube_trending(region_code="IN", limit=10):
    """
    Returns trending music videos for the given region.
    Uses YouTube's mostPopular chart filtered to the Music category (id=10).
    Results are cached for 30 minutes.
    """
    cache_key = f"yt_trending_{region_code}_{limit}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    data = youtube_request("videos", {
        "part": "snippet,contentDetails,statistics",
        "chart": "mostPopular",
        "videoCategoryId": "10",   # Music category
        "regionCode": region_code,
        "maxResults": limit,
    })

    if not data:
        return []

    results = [
        {
            "id": item["id"],
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "cover_image": (
                item["snippet"]["thumbnails"].get("high", {}).get("url")
                or item["snippet"]["thumbnails"].get("default", {}).get("url")
            ),
            "published_at": item["snippet"].get("publishedAt"),
            "view_count": item.get("statistics", {}).get("viewCount"),
            "duration": item.get("contentDetails", {}).get("duration"),  # ISO 8601
            "youtube_url": f"https://www.youtube.com/watch?v={item['id']}",
        }
        for item in data.get("items", [])
    ]

    cache.set(cache_key, results, timeout=1800)   # 30 min
    return results


# ── SEARCH ─────────────────────────────────────────────────────────────────────
def search_youtube_music(query, limit=10):
    """
    Searches YouTube for music videos matching `query`.
    Results are cached for 15 minutes per (query, limit) pair.
    """
    cache_key = f"yt_search_{query}_{limit}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    data = youtube_request("search", {
        "part": "snippet",
        "q": query,
        "type": "video",
        "videoCategoryId": "10",
        "maxResults": limit,
    })

    if not data:
        return []

    results = [
        {
            "id": item["id"]["videoId"],
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "cover_image": (
                item["snippet"]["thumbnails"].get("high", {}).get("url")
                or item["snippet"]["thumbnails"].get("default", {}).get("url")
            ),
            "published_at": item["snippet"].get("publishedAt"),
            "youtube_url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
        }
        for item in data.get("items", [])
    ]

    cache.set(cache_key, results, timeout=900)   # 15 min
    return results


# ── ARTISTS (YouTube Channels) ─────────────────────────────────────────────────
def get_youtube_artists(limit=8):
    """
    Searches for popular music artist channels on YouTube.
    Mirrors get_artists() in spotify_service.py.
    """
    artist_queries = [
        "Arijit Singh", "Shreya Ghoshal", "A.R. Rahman",
        "Taylor Swift", "Bruno Mars", "The Weeknd",
        "Udit Narayan", "Lata Mangeshkar",
    ]

    artists = []
    for query in artist_queries[:limit]:
        cache_key = f"yt_artist_{query}"
        cached = cache.get(cache_key)
        if cached:
            artists.append(cached)
            continue

        data = youtube_request("search", {
            "part": "snippet",
            "q": query,
            "type": "channel",
            "maxResults": 1,
        })

        if not data:
            continue

        items = data.get("items", [])
        if not items:
            continue

        channel = items[0]["snippet"]
        artist = {
            "name": channel["channelTitle"],
            "image": (
                channel["thumbnails"].get("high", {}).get("url")
                or channel["thumbnails"].get("default", {}).get("url")
            ),
            "channel_id": items[0]["id"]["channelId"],
        }
        cache.set(cache_key, artist, timeout=86400)   # 24 hours
        artists.append(artist)

    return artists


# ── PLAYLISTS (YouTube Playlists) ──────────────────────────────────────────────
def get_youtube_playlists(limit=10):
    """
    Searches for popular music playlists on YouTube.
    Mirrors get_playlists() in spotify_service.py.
    """
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
        cache_key = f"yt_playlist_{query}"
        cached = cache.get(cache_key)
        if cached:
            playlists.append(cached)
            continue

        data = youtube_request("search", {
            "part": "snippet",
            "q": query,
            "type": "playlist",
            "maxResults": 1,
        })

        if not data:
            continue

        items = data.get("items", [])
        if not items:
            continue

        p = items[0]
        playlist = {
            "id": p["id"]["playlistId"],
            "name": p["snippet"]["title"],
            "image": (
                p["snippet"]["thumbnails"].get("high", {}).get("url")
                or p["snippet"]["thumbnails"].get("default", {}).get("url")
            ),
            "description": p["snippet"].get("description", ""),
            "channel": p["snippet"]["channelTitle"],
        }
        cache.set(cache_key, playlist, timeout=3600)   # 1 hour
        playlists.append(playlist)

    return playlists


# ── PLAYLIST DETAIL ────────────────────────────────────────────────────────────
def get_youtube_playlist_detail(playlist_id, limit=50):
    """
    Returns metadata + video list for a YouTube playlist.
    Mirrors get_playlist_detail() in spotify_service.py.
    """
    cache_key = f"yt_playlist_detail_{playlist_id}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    # Step 1 — Playlist metadata
    meta_data = youtube_request("playlists", {
        "part": "snippet",
        "id": playlist_id,
    })

    if not meta_data or not meta_data.get("items"):
        return None

    meta = meta_data["items"][0]["snippet"]
    playlist_info = {
        "id": playlist_id,
        "name": meta["title"],
        "description": meta.get("description", ""),
        "image": (
            meta["thumbnails"].get("high", {}).get("url")
            or meta["thumbnails"].get("default", {}).get("url")
        ),
        "channel": meta["channelTitle"],
    }

    # Step 2 — Playlist items
    items_data = youtube_request("playlistItems", {
        "part": "snippet,contentDetails",
        "playlistId": playlist_id,
        "maxResults": limit,
    })

    songs = []
    if items_data:
        for item in items_data.get("items", []):
            snippet = item.get("snippet", {})
            video_id = snippet.get("resourceId", {}).get("videoId")
            if not video_id:
                continue
            songs.append({
                "id": video_id,
                "title": snippet.get("title", ""),
                "artist": {"name": snippet.get("videoOwnerChannelTitle", "")},
                "album": playlist_info["name"],
                "image": (
                    snippet["thumbnails"].get("high", {}).get("url")
                    or snippet["thumbnails"].get("default", {}).get("url")
                    if snippet.get("thumbnails") else None
                ),
                "duration": None,   # Requires an extra videos.list call; omitted for quota
                "explicit": False,
                "date_added": snippet.get("publishedAt"),
                "youtube_url": f"https://www.youtube.com/watch?v={video_id}",
                "audio_url": None,
            })

    result = {"playlist": playlist_info, "songs": songs}
    cache.set(cache_key, result, timeout=1800)
    return result
