from django.db import models

# Create your models here.
from django.urls import reverse


class Image(models.Model):
    name        = models.CharField(max_length=120, blank=False, null=True)
    image       = models.ImageField(verbose_name="Image", blank=True, null=True, upload_to='img')
    description = models.TextField(max_length=500, null=True, blank=True)
    comments    = models.ManyToManyField("comments.Comment", related_name="all_comments", blank=True)
    likes       = models.ManyToManyField("likes.Like", related_name="all_likes", blank=True)
    tags        = models.ManyToManyField("tags.Tag", related_name="all_tags", blank=True)
    is_public   = models.BooleanField(default=False)
    timestamp   = models.DateField(auto_now_add=True)
    updated     = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def get_absolute_url(self): # get_absolute_url
        return reverse('images:detail', kwargs={'pk': self.pk})
