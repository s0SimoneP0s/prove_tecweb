"""biblio2 URL Configuration

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

from django.urls import path
from .views import *

app_name = "gestione"

urlpatterns = [
    path("listalibri/", lista_libri, name="listalibri"),
    path("prestito/<str:titolo>/<str:autore>/",presta_libro,name="prestalibro"),
    path("restituzione/<str:titolo>/<str:autore>/",restituisci_lista,name="restlista"),
    path("restituzione/<int:pk>/",restituisci_final,name="restfinal")
]
