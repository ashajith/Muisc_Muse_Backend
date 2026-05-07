import requests
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@require_GET
def audio_lookup(request):
    """
    GET /api/audio/?title=Tum Hi Ho&artist=Arijit Singh
    Searches JioSaavn for a playable MP3 URL. No API key needed.
    Returns { audio_url: "https://..." } or { audio_url: null }
    """
    title = request.GET.get("title", "").strip()
    artist = request.GET.get("artist", "").strip()

    if not title:
        return JsonResponse({"audio_url": None, "error": "title is required"}, status=400)

    query = f"{title} {artist}".strip()

    try:
        resp = requests.get(
            "https://saavn.dev/api/search/songs",
            params={"query": query, "limit": 5},
            timeout=8,
            headers={"User-Agent": "Mozilla/5.0"},
        )

        if resp.status_code != 200:
            return JsonResponse({"audio_url": None})

        results = resp.json().get("data", {}).get("results", [])

        for song in results:
            # downloadUrl is a list of quality options: pick highest available
            for entry in reversed(song.get("downloadUrl", [])):
                url = entry.get("url", "")
                if url:
                    return JsonResponse({"audio_url": url})

        return JsonResponse({"audio_url": None})

    except Exception as e:
        print(f"Audio lookup error: {e}")
        return JsonResponse({"audio_url": None})