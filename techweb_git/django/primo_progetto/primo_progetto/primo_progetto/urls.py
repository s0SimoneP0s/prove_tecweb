"""primo_progetto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    path("home/",home_page,name="homepage"),
    #re_path(r"^$|^/$|^home/$",home_page,name="homepage"),
    path("elencoparametri/",elenca_params,name="params"),

    re_path(r"^welcome_[A-Za-z0-9]+$",welcome_user,name="welcomeuser"),
    path("paridispari/",pari_dispari,name="paridispari"),
    path("welcome/",welcome_name,name="welcome"),

    path("welcome_path/<str:nome>/<int:eta>/",welcome_path,name="welcomepath"),

    path("hellotemplate/",hello_template,name="hellotemplate"),
    path("helloparams/", hello_params_get,name="helloparamget"),
    path("helloparams/<str:nome>/<int:eta>/", hello_params_url,name="helloparamurl"),

    path("staticpage/",page_with_static,name="staticpage")
]
