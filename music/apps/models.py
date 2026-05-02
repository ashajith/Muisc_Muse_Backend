from django.db import models

class Artist(models.Model):
    name = models.CharField(max_length=255)
    image = models.URLField()

    def __str__(self):
        return self.name


class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="songs")
    audio_file = models.URLField()
    cover_image = models.URLField()
    duration = models.IntegerField()

    play_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Playlist(models.Model):
    name = models.CharField(max_length=255)
    image = models.URLField()
    songs = models.ManyToManyField(Song, related_name="playlists")

    def __str__(self):
        return self.name