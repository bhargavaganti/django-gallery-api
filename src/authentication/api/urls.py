from django.conf.urls import url
from rest_framework import urlpatterns
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

urlpatterns = [
    url(r'token/refresh/?$', refresh_jwt_token, name='token-refresh'),
    url(r'token/validate/?$', verify_jwt_token, name='token-validate'),
    url(r'token/?$', obtain_jwt_token, name='token'),

]
