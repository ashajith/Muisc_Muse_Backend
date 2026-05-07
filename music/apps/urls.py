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

urlpatterns = [
    # ── Auth ────────────────────────────────────────────────────────────────
    path("login/", LoginView.as_view()),

    # ── DB / general ────────────────────────────────────────────────────────
    path("songs/", SongListView.as_view()),
    path("trending/", trending_songs),

    # ── Spotify ─────────────────────────────────────────────────────────────
    path("spotify/trending/", spotify_trending),
    path("artists/", artists_view),
    path("playlists/", playlists_view),
    path("playlists/<str:pk>/", playlist_detail),

    # ── YouTube ─────────────────────────────────────────────────────────────
    path("youtube/trending/", youtube_trending),            # GET ?region=IN&limit=10
    path("youtube/search/", youtube_search),                # GET ?q=<query>&limit=10
    path("youtube/artists/", youtube_artists),              # GET
    path("youtube/playlists/", youtube_playlists),          # GET
    path("youtube/playlists/<str:playlist_id>/", youtube_playlist_detail),  # GET
]
