from django.conf import settings
from django.db import models
from django.urls import reverse

User = settings.AUTH_USER_MODEL

class Like(models.Model):
    owner     = models.OneToOneField("profiles.Profile")
    image     = models.OneToOneField("images.Image")
    timestamp = models.DateTimeField(auto_now_add=True)
    updated   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.owner.user.email + " - " + self.image.name

    def __unicode__(self):
        return self.owner.user.email + " - " + self.image.name

    def get_absolute_url(self): #get_absolute_url
        return reverse('likes:detail', kwargs={'pk': self.pk})
