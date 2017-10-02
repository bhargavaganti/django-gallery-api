"""
from src.images.models import Image

obj = Image.objects.get(pk=4)

print(obj)

obj.album.images.all()
"""