from django.urls import path
from . import views

urlpatterns = [
    path("playlists/<str:playlist_id>/", views.playlist_detail_view, name="playlist-detail"),
]