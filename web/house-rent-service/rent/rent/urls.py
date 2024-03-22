"""rent URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
#from django.conf.urls import url, include
from django.urls import path, include,re_path
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    re_path('^admin/', admin.site.urls),
    re_path('^$', views.index, name='home'),
    re_path('^receivepay', views.process_user_sms, name='user_sms'),
    re_path('^accounts/', include('accounts.urls', namespace='accounts')),
    re_path('^accounts/', include('django.contrib.auth.urls')),
    re_path('^posts/', include('posts.urls', namespace='posts')),
    re_path('^ratings/', include('star_ratings.urls', namespace='ratings')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
