
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^albums/', include('src.albums.urls', namespace='albums')),
    url(r'^tags/', include('src.tags.urls', namespace='tags')),
    # url(r'^api/', include(router.urls, namespace='api')),
    url(r'^api/albums/', include("src.albums.api.urls", namespace='albums-api')),
    url(r'^api/images/', include("src.images.api.urls", namespace='images-api')),
    url(r'^api/tags/', include("src.tags.api.urls", namespace='tags-api')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
