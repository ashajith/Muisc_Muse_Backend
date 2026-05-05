import requests

from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny

from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta

from rest_framework_simplejwt.tokens import RefreshToken

from .models import Artist, Song, Playlist
from .serializers import ArtistSerializer, SongSerializer, PlaylistSerializer

from .services.spotify_service import (
    get_spotify_tracks,
    get_artists,
    get_playlists,
    get_playlist_detail,
)
from .services.youtube_service import get_youtube_audio_url


# ---------------- AUTH ----------------
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({"error": "Invalid credentials"}, status=401)

        refresh = RefreshToken.for_user(user)
        return Response({"access": str(refresh.access_token)})


# ---------------- TRENDING ----------------
@api_view(['GET'])
def trending_songs(request):
    period = request.GET.get("period", "week")
    since = timezone.now() - (timedelta(days=30) if period == "month" else timedelta(days=7))
    songs = Song.objects.filter(created_at__gte=since).order_by("-play_count")[:5]
    serializer = SongSerializer(songs, many=True)
    return Response(serializer.data)


# ---------------- SPOTIFY TRENDING ----------------
@api_view(['GET'])
def spotify_trending(request):
    songs = get_spotify_tracks(query="top hits", limit=5)
    return Response(songs)


# ---------------- ARTISTS ----------------
@api_view(['GET'])
def artists_view(request):
    return Response(get_artists())


# ---------------- SONGS ----------------
class SongListView(APIView):
    def get(self, request):
        songs = Song.objects.select_related("artist").all()
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)


# ---------------- PLAYLISTS LIST ----------------
@api_view(['GET'])
def playlists_view(request):
    data = get_playlists()
    return Response(data)


# ---------------- PLAYLIST DETAIL (Spotify) ----------------
@api_view(['GET'])
def playlist_detail(request, pk):
    data = get_playlist_detail(pk)

    if not data:
        return Response({"error": "Playlist not found"}, status=404)

    return Response(data)


# ---------------- YOUTUBE AUDIO URL ----------------
@api_view(['GET'])
def youtube_audio_url(request):
    """
    GET /api/audio/?title=Blinding+Lights&artist=The+Weeknd
    Returns { "audio_url": "https://..." } or { "audio_url": null }
    """
    title = request.GET.get("title", "").strip()
    artist = request.GET.get("artist", "").strip()

    if not title:
        return Response({"error": "title is required"}, status=400)

    url = get_youtube_audio_url(title, artist)
    return Response({"audio_url": url})