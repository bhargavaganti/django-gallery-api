from django.db import models

# Create your models here.
from django.urls import reverse


class Album(models.Model):
    name        = models.CharField(max_length=120, blank=False, null=False)
    description = models.TextField( max_length=500, null=True)
    images      = models.ManyToManyField("images.Image", related_name="album_images", blank=True)
    is_public   = models.BooleanField(default=False)
    timestamp   = models.DateField(auto_now_add=True)
    updated     = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def get_absolute_url(self): #get_absolute_url
        return reverse('albums:detail', kwargs={'pk': self.pk})

    @property
    def owner(self):
        return self.profile_set.get()

    def set_owner(self, owner):
        self.profile_set.all().delete()
        self.profile_set.add(owner)





