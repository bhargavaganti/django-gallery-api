from django.db import models

# Create your models here.
from django.urls import reverse


class Category(models.Model):
    name        = models.CharField(max_length=120, blank=False, null=False)
    description = models.TextField(max_length=500, null=True)
    albums      = models.ManyToManyField("albums.Album", blank=True, null=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('categories:detail', kwargs={'pk': self.pk})
