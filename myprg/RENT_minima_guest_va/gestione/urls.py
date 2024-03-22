
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path,re_path

from .views import (
    GestioneHomeView,
    ZonaCreateView,
)

app_name = "gestione"

urlpatterns = [
    # Staff 
    path('nuova-zona/',                         ZonaCreateView.as_view(),           name='nuova_zona'),
    

    # Utente Iscritto
    re_path(r"^$|^\/$|^home\/$",                GestioneHomeView.as_view(),         name="home"),
 
    # Utente Cliente
    
    # Utente Proprietario
   
]