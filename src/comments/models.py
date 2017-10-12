from django.conf import settings
from django.db import models
from django.urls import reverse

User = settings.AUTH_USER_MODEL

class Comment(models.Model):
    owner     = models.ManyToManyField("profiles.Profile", unique=False)
    image     = models.ManyToManyField("images.Image", unique=False)
    content   = models.TextField(max_length=500, blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content #maybe Comment?!

    def __unicode__(self):
        return  self.content

    def get_absolute_url(self): #get_absolute_url
        return reverse('comment:detail', kwargs={'pk': self.pk})
