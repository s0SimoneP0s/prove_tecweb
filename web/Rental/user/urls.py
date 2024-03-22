from django.urls import path,re_path
from django.contrib.auth import logout
from . import views

urlpatterns =[
	path('profile', views.profile, name= 'profile'),
	path('post',views.post, name = 'post'),
]
