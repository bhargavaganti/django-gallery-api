from django.conf.urls import url
from .views import GetProfilesAPI, GetProfileAPI, CreateProfileAPI, UpdateProfileAPI, DeleteProfileAPI

urlpatterns = [
    url(r'(?P<pk>\d+)/delete/?$', DeleteProfileAPI.as_view(), name='delete'),
    url(r'(?P<pk>\d+)/edit/?$', UpdateProfileAPI.as_view(), name='update'),
    url(r'(?P<pk>\d+)/?$', GetProfileAPI.as_view(), name='detail'),  # TODO: обриши имена
    url(r'create/?$', CreateProfileAPI.as_view(), name='create'),
    url(r'$', GetProfilesAPI.as_view(), name='list')

]

