"""
from src.albums.models import Album
albums = Album.objects.filter(owner__pk=1)
albums
"""

from src.profiles.models import Profile

profile = Profile.objects.get(pk=1)

print(profile.albums.all())

