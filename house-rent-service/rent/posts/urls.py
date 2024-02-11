#from django.conf.urls import url
from django.urls import path,re_path
from . import views


app_name = 'posts'

urlpatterns = [
    path('new/', views.create_post, name='post_new'),
    path('get_location/', views.get_location_data, name='get_location'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('remove/<int:pk>/', views.PostDeleteView.as_view(), name='post_remove'),
    path('getcontact/<int:pk>/', views.get_user_contact, name='getcontact'),
]

