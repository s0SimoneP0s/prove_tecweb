
from django.urls import path
from .views import *

app_name = "gestione"

urlpatterns = [
    path("", gestione_home, name="home"),
    path("listalibri/", LibroListView.as_view(),name="listalibri"),
    path("ricerca/", search, name="cercalibro"),
    path("ricerca/<str:sstring>/<str:where>/", LibroRicercaView.as_view(), name="ricerca_risultati"),
    path("prestito/<pk>/", prestito, name="prestito"),
    path("situation/", my_situation, name="situation"),
    path("restituzione/<pk>/", RestituisciView.as_view(), name="restituzione"),

    path("situationb/", BiblioSituationView.as_view(),name="situationb"),
    path("detailb/<pk>/", BiblioDetailView.as_view(), name="detailb"),
    path("crea_libro/",CreateLibroView.as_view(),name="crealibro"),
    path("crea_copia/",CreateCopiaView.as_view(),name="creacopia"),

    path("ricerca/gethint/", get_hint, name="get_hint")
]