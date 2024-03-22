#from django.conf.urls import url
from django.urls import path, include,re_path
from .views import ListingsRudView, ListingsAPIView

urlpatterns = [
    re_path(r'^$', ListingsAPIView.as_view(), name='post-create'),
    re_path(r'^(?P<pk>\d+)/$', ListingsRudView.as_view(), name='post-rud'),
]