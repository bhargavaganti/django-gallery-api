from django.conf import settings
from django.db import models
from django.urls import reverse

User = settings.AUTH_USER_MODEL

class Like(models.Model):
    owner     = models.ManyToManyField("profiles.Profile")
    image     = models.ManyToManyField("images.Image")
    timestamp = models.DateTimeField(auto_now_add=True)
    updated   = models.DateTimeField(auto_now=True)

    def __str__(self):
        # return self.owner.first()
        return "like"

    def __unicode__(self):
        return "like"

    def get_absolute_url(self): #get_absolute_url
        return reverse('likes:detail', kwargs={'like_id': self.pk})
