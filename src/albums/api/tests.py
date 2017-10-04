from src.albums.models import Album

album_id, image_id = 1, 1

album = Album.objects.get(pk=album_id)
album.images.all()

