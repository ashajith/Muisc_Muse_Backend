from django.core.management.base import BaseCommand
from apps.models import Artist, Song, Playlist


class Command(BaseCommand):
    help = "Seed database with music data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Clearing old data...")
        Playlist.objects.all().delete()
        Song.objects.all().delete()
        Artist.objects.all().delete()

        self.stdout.write("Creating artists...")

        arijit = Artist.objects.create(
            name="Arijit Singh",
            image="https://i.scdn.co/image/ab6761610000e5eb4293385d324db8558179afd9"
        )
        pritam = Artist.objects.create(
            name="Pritam",
            image="https://i.scdn.co/image/ab6761610000e5eb9e7290c01b14d0d81e1bf415"
        )
        ar_rahman = Artist.objects.create(
            name="A.R. Rahman",
            image="https://i.scdn.co/image/ab6761610000e5eba3f947f14f26ab1e3b0e4ae8"
        )
        shreya = Artist.objects.create(
            name="Shreya Ghoshal",
            image="https://i.scdn.co/image/ab6761610000e5eb82c3f91eb5e8c0b4aea8d1c1"
        )
        vishal = Artist.objects.create(
            name="Vishal-Shekhar",
            image="https://i.scdn.co/image/ab6761610000e5eb5c25988a6ac314394d3fbf5"
        )

        self.stdout.write("Creating songs...")

        songs_data = [
            # Arijit Singh
            {
                "title": "Tum Hi Ho",
                "artist": arijit,
                "audio_file": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
                "cover_image": "https://i.scdn.co/image/ab67616d0000b2732f6a706e9f3f1b6d2f5e0e5e",
                "duration": 261,
            },
            {
                "title": "Channa Mereya",
                "artist": arijit,
                "audio_file": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
                "cover_image": "https://i.scdn.co/image/ab67616d0000b273f4f8e3bfe8bb8c1e8c5b8d3e",
                "duration": 294,
            },
            {
                "title": "Ae Dil Hai Mushkil",
                "artist": arijit,
                "audio_file": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
                "cover_image": "https://i.scdn.co/image/ab67616d0000b273b8c6b4c5e3f1a7d2e5f9c0b1",
                "duration": 270,
            },
            {
                "title": "Kal Ho Naa Ho",
                "artist": arijit,
                "audio_file": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3",
                "cover_image": "https://i.scdn.co/image/ab67616d0000b2738a4f9b3c2e7d1f5a6b8c9d0e",
                "duration": 306,
            },
            # Pritam
            {
                "title": "Badtameez Dil",
                "artist": pritam,
                "audio_file": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3",
                "cover_image": "https://i.scdn.co/image/ab67616d0000b273b092dbb02f474b81fc300e24",
                "duration": 223,
            },
            {
                "title": "Ilahi",
                "artist": pritam,
                "audio_file": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-6.mp3",
                "cover_image": "https://i.scdn.co/image/ab67616d0000b273c3e5e2b9f4d8a1f7e9c5b3d2",
                "duration": 248,
            },
            {
                "title": "Gerua",
                "artist": pritam,
                "audio_file": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-7.mp3",
                "cover_image": "https://i.scdn.co/image/ab67616d0000b2735f8a6f2a27d5d75abc41501a",
                "duration": 285,
            },
            # A.R. Rahman
            {
                "title": "Jai Ho",
                "artist": ar_rahman,
                "audio_file": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3",
                "cover_image": "https://i.scdn.co/image/ab67616d0000b273d1e8e9f3c2a5b8f4e7c0d9b6",
                "duration": 318,
            },
            {
                "title": "Chaiyya Chaiyya",
                "artist": ar_rahman,
                "audio_file": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-9.mp3",
                "cover_image": "https://i.scdn.co/image/ab67616d0000b273e2f9c4b7a3d6f1e8c5b2a9d0",
                "duration": 342,
            },
            {
                "title": "Roja",
                "artist": ar_rahman,
                "audio_file": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-10.mp3",
                "cover_image": "https://i.scdn.co/image/ab67616d0000b2739b3c7f2e4d8a5c1b6e9f0d7a",
                "duration": 276,
            },
            # Shreya Ghoshal
            {
                "title": "Teri Meri",
                "artist": shreya,
                "audio_file": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-11.mp3",
                "cover_image": "https://i.scdn.co/image/ab67616d0000b273a4c8e2f1b7d5c3e9f6b0a8d4",
                "duration": 255,
            },
            {
                "title": "Sun Raha Hai",
                "artist": shreya,
                "audio_file": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-12.mp3",
                "cover_image": "https://i.scdn.co/image/ab67616d0000b2736b4d9c3e2f8a1b5c7e0d4f9a",
                "duration": 299,
            },
            # Vishal-Shekhar
            {
                "title": "Dil Dhadakne Do",
                "artist": vishal,
                "audio_file": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-13.mp3",
                "cover_image": "https://i.scdn.co/image/ab67616d0000b273f3e8c9b4a2d7e1f5c6b8a0d3",
                "duration": 244,
            },
            {
                "title": "Nashe Si Chadh Gayi",
                "artist": vishal,
                "audio_file": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-14.mp3",
                "cover_image": "https://i.scdn.co/image/ab67616d0000b273f5dc36d5000145375a41c3b8",
                "duration": 231,
            },
            {
                "title": "Besharam Rang",
                "artist": vishal,
                "audio_file": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-15.mp3",
                "cover_image": "https://i.scdn.co/image/ab67616d0000b27313d49ed65bac50bf72524091",
                "duration": 208,
            },
        ]

        songs = []
        for data in songs_data:
            song = Song.objects.create(**data)
            songs.append(song)
            self.stdout.write(f"  Created: {song.title}")

        self.stdout.write("Creating playlists...")

        # Playlist 1 — Bollywood Hits
        p1 = Playlist.objects.create(
            name="Bollywood Hits",
            image="https://i.scdn.co/image/ab67706f000000025551996f500ba876bda73fa5"
        )
        p1.songs.add(*songs[:8])

        # Playlist 2 — Romance
        p2 = Playlist.objects.create(
            name="Romance",
            image="https://i.scdn.co/image/ab67706f00000002fe6d8d1019d5b302213e3730"
        )
        p2.songs.add(songs[0], songs[1], songs[2], songs[6], songs[10], songs[11])

        # Playlist 3 — Party Anthems
        p3 = Playlist.objects.create(
            name="Party Anthems",
            image="https://i.scdn.co/image/ab67706f000000023dadf0baa76e5c1f7c7a2ab7"
        )
        p3.songs.add(songs[4], songs[5], songs[7], songs[12], songs[13], songs[14])

        # Playlist 4 — A.R. Rahman Classics
        p4 = Playlist.objects.create(
            name="A.R. Rahman Classics",
            image="https://i.scdn.co/image/ab67706f00000002e4eadd417a05b2b5b3c9e7f8"
        )
        p4.songs.add(songs[7], songs[8], songs[9])

        # Playlist 5 — Arijit Singh Best
        p5 = Playlist.objects.create(
            name="Arijit Singh Best",
            image="https://i.scdn.co/image/ab67706f000000024293385d324db8558179afd9"
        )
        p5.songs.add(songs[0], songs[1], songs[2], songs[3])

        self.stdout.write(self.style.SUCCESS(
            f"\nDone! Created {len(songs)} songs across 5 playlists."
        ))