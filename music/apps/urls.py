from django.urls import path
from .views import (
    LoginView,
    SongListView,
    artists_view,
    playlists_view,
    spotify_trending,
    playlist_detail,
)

urlpatterns = [
    path("login/", LoginView.as_view()),
    path("spotify/trending/", spotify_trending),
    path("artists/", artists_view),
    path("songs/", SongListView.as_view()),
    path("playlists/", playlists_view),
    path("playlists/<str:pk>/", playlist_detail),   # ← str, Spotify IDs are strings like "37i9dQZF1DX..."
]