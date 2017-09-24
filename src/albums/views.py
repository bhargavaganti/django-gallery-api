from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from src.albums.models import Album

class AlbumListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return Album.objects.all()


class AlbumDetailView(LoginRequiredMixin, DetailView):

     def get_queryset(self):
        return Album.objects.filter(owner=self.request.user.profile)

     def get_context_data(self, *args, **kwargs):
         context = super(AlbumDetailView, self).get_context_data(*args, **kwargs)
         images = self.get_object().images
         context['images'] = images.all()
         return context