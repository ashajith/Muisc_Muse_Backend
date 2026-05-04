from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from apps.services.spotify_service import get_playlist_detail

@csrf_exempt
@require_GET
def playlist_detail_view(request, playlist_id):
    data = get_playlist_detail(playlist_id)
    if not data:
        return JsonResponse({"error": "Playlist not found"}, status=404)
    return JsonResponse(data)
