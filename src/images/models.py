from django.db import models

# Create your models here.
from django.urls import reverse


class Image(models.Model):
    name        = models.CharField(max_length=120, blank=False, null=True)
    image       = models.ImageField(verbose_name="Image", blank=True, null=True, upload_to='img')
    description = models.TextField(max_length=500, null=True, blank=True)
    comments    = models.ManyToManyField("comments.Comment", related_name="all_comments", null=True, blank=True)
    likes       = models.ManyToManyField("likes.Like", related_name="all_likes", null=True, blank=True)
    categories  = models.ManyToManyField("categories.Category", related_name="all_categories")
    is_public   = models.BooleanField(default=False)
    timestamp   = models.DateField(auto_now_add=True)
    updated     = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def get_absolute_url(self): #get_absolute_url
        return reverse('images:detail', kwargs={'pk': self.pk})
