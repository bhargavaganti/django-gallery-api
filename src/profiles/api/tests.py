"""
from src.albums.models import Album
albums = Album.objects.filter(owner__pk=1)
albums
"""