from django.db import models

# Create your models here.
from django.urls import reverse


class Tag(models.Model):
    name   = models.CharField(max_length=120, blank=False, null=False)
    image  = models.ForeignKey("images.Image", blank=True, null=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag:detail', kwargs={'pk': self.pk})
