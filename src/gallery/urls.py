
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import url
from django.http import HttpResponse

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from src.profiles.api.views import GetProfilesAPI
from src.albums.api.views import GetAlbumsAPI


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # url(r'^albums/', include('src.albums.urls', namespace='albums')),
    # url(r'^tags/', include('src.tags.urls', namespace='tags')),
    url(r'^api/auth/', include("src.authentication.api.urls", namespace='auth')),
    url(r'^api/albums/', include("src.albums.api.urls", namespace='albums-api')),
    url(r'^api/images/', include("src.images.api.urls", namespace='images-api')),
    url(r'^api/tags/', include("src.tags.api.urls", namespace='tags-api')),
    url(r'^api/profiles/', include("src.profiles.api.urls", namespace='profiles-api')),

]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
