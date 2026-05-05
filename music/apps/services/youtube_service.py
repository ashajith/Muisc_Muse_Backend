import yt_dlp
from django.core.cache import cache


def get_youtube_audio_url(title: str, artist: str) -> str | None:
    query = f"{title} {artist} audio"
    cache_key = f"yt_audio_{title}_{artist}".replace(" ", "_")[:200]

    cached = cache.get(cache_key)
    if cached:
        print(f"[YouTube] Cache hit for: {query}")
        return cached

    ydl_opts = {
        # itag=18 is mp4 audio+video — browser can play it fine
        # Use a broad format selector so it works without ffmpeg or JS runtime
        "format": "18/bestaudio/best",
        "quiet": False,
        "no_warnings": False,
        "noplaylist": True,
        "nocheckcertificate": True,
        "noprogress": True,
        # Pretend to be Android VR client — avoids JS requirement
        "extractor_args": {
            "youtube": {
                "player_client": ["android_vr", "android", "web"],
            }
        },
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"[YouTube] Searching: {query}")
            info = ydl.extract_info(f"ytsearch1:{query}", download=False)

            if not info:
                print("[YouTube] No info returned")
                return None

            entries = info.get("entries")
            if not entries:
                print("[YouTube] No entries in result")
                return None

            entry = entries[0]
            print(f"[YouTube] Found: {entry.get('title')}")

            formats = entry.get("formats") or []
            audio_url = None

            # Try audio-only first
            for f in reversed(formats):
                if f.get("acodec") != "none" and f.get("vcodec") == "none":
                    audio_url = f.get("url")
                    print(f"[YouTube] Audio-only format found: {f.get('format_id')}")
                    break

            # Fallback: itag 18 (mp4, browser-compatible)
            if not audio_url:
                for f in formats:
                    if f.get("format_id") == "18":
                        audio_url = f.get("url")
                        print("[YouTube] Using itag 18 (mp4 fallback)")
                        break

            # Last resort: top-level url
            if not audio_url:
                audio_url = entry.get("url")
                print("[YouTube] Using top-level url as last resort")

            if audio_url:
                print(f"[YouTube] URL obtained, caching...")
                cache.set(cache_key, audio_url, timeout=600)
            else:
                print("[YouTube] No URL found in any format")

            return audio_url

    except Exception as e:
        print(f"[YouTube] ERROR for '{query}': {type(e).__name__}: {e}")
        return None