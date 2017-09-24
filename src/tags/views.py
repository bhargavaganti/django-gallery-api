from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView

from src.tags.models import Tag

class TagListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return Tag.objects.all()


class TagDetailView(LoginRequiredMixin, DetailView):

     def get_queryset(self):
        return Tag.objects.filter()

     # def get_context_data(self, *args, **kwargs):
     #     context = super(AlbumDetailView, self).get_context_data(*args, **kwargs)
     #     images = self.get_object().images
     #     context['images'] = images.all()
     #     retur