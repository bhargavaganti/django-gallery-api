
from src.likes.models import Like

from src.images.models import Image

image_id = 1

all_likes_at_images = Like.objects.filter(image__pk=image_id)
all_likes_at_images
# like = Like.objects.first()
# like.images.all()


image = Image.objects.get(pk=all_likes_at_images.first().image.get().id)
image
