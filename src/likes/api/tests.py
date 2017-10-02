
from src.likes.models import Like

image_id = 1

all_likes_at_images = Like.objects.filter(image__pk=image_id)
all_likes_at_images
# like = Like.objects.first()
# like.images.all()

