
from src.comments.models import Comment
from src.images.models import Image

image_id = 1

all_comments_at_images = Comment.objects.filter(image__pk=image_id)
image = Image.objects.get(pk=image_id)
image.comments.all()
all_comments_at_images
# comment = Comment.objects.first()
# comment.images.all()

