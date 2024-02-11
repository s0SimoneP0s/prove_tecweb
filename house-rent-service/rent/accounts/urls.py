#from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path, include,re_path
from . import views
from . import forms

app_name = 'accounts'

urlpatterns = [
    re_path('login/$', auth_views.LoginView.as_view(
        template_name='accounts/login.html', authentication_form=forms.CustomAuthForm), name='login'),
    re_path('logout/$', auth_views.LogoutView.as_view(), name='logout'),
    re_path('signup/$', views.SignUp.as_view(), name='signup'),
    re_path('dashboard/$', views.user_dashboard, name='dashboard'),
]