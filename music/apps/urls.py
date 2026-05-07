from django.urls import path
from .views import (
    # Auth
    LoginView,
    # DB
    SongListView,
    trending_songs,
    # Spotify
    artists_view,
    playlists_view,
    spotify_trending,
    playlist_detail,
    # YouTube
    youtube_trending,
    youtube_search,
    youtube_artists,
    youtube_playlists,
    youtube_playlist_detail,
)
from .audio_view import audio_lookup

urlpatterns = [
    # ── Auth ──────────────────────────────────────────────────
    path("login/", LoginView.as_view()),

    # ── DB / general ──────────────────────────────────────────
    path("songs/", SongListView.as_view()),
    path("trending/", trending_songs),

    # ── Audio lookup (JioSaavn) ────────────────────────────────
    path("audio/", audio_lookup),

    # ── Spotify ───────────────────────────────────────────────
    path("spotify/trending/", spotify_trending),
    path("artists/", artists_view),
    path("playlists/", playlists_view),
    path("playlists/<str:pk>/", playlist_detail),

    # ── YouTube ───────────────────────────────────────────────
    path("youtube/trending/", youtube_trending),
    path("youtube/search/", youtube_search),
    path("youtube/artists/", youtube_artists),
    path("youtube/playlists/", youtube_playlists),
    path("youtube/playlists/<str:playlist_id>/", youtube_playlist_detail),
]