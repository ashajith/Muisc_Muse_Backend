"""
Compatibility wrapper.

This module intentionally re-exports Spotify helpers from the canonical
service module so older imports under `apps.songs` stay in sync.
"""

from apps.services.spotify_service import (  # noqa: F401
    get_artists,
    get_cached_token,
    get_playlist_detail,
    get_playlists,
    get_spotify_tracks,
    spotify_request,
)
