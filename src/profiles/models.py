from django.conf import settings
from django.db import models

# from .albums.models import Album
# from .comments.models import Comment
# from .images.models import Image
# from .likes.models import Like
from django.urls import reverse

# асоцијација са уграђеним Корисник моделом
User = settings.AUTH_USER_MODEL

class Profile(models.Model):
    user            = models.OneToOneField(User)
    albums          = models.ManyToManyField("albums.Album", blank=True)
    # commented       = models.ManyToManyField("comments.Comment", blank=True, unique=False)
    # liked           = models.ManyToManyField("likes.Like", blank=True)
    profile_picture = models.ImageField( blank=True, null=True, upload_to='profile_pics')
    timestamp       = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

    def __unicode__(self):
        return self.user.email

    def get_absolute_url(self): #get_absolute_url
        return reverse('profiles:detail', kwargs={'profile_id': self.pk})
