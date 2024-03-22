from __future__ import unicode_literals

from django.urls import re_path, path

from .views import Rate
from . import app_settings


urlpatterns = [
    path('<int:content_type_id>/<str:object_id>/', Rate.as_view(), name='rate'),
]

app_name = 'star_ratings'
