
from src.comments.models import Comment

image_id = 1

all_comments_at_images = Comment.objects.filter(image__pk=image_id)
all_comments_at_images
# comment = Comment.objects.first()
# comment.images.all()

