from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView

from src.categories.models import Category

class CategoryListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return Category.objects.all()


class CategoryDetailView(LoginRequiredMixin, DetailView):

     def get_queryset(self):
        return Category.objects.filter()

     # def get_context_data(self, *args, **kwargs):
     #     context = super(AlbumDetailView, self).get_context_data(*args, **kwargs)
     #     images = self.get_object().images
     #     context['images'] = images.all()
     #     retur