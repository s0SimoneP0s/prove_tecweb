
from django.contrib import admin
from django.urls import path, re_path, include
from django.contrib.auth import views as v
from .views import (
    ImmobileListView,
    UserCreateView,
    RentHomeView,
    InitDBView,
    SearchAndRedirectView,
    RicercaImmobileView,
    AjaxSearchGetHintView,
    MessaggioPrenotaOraView
  )

urlpatterns = [
    # path                                      # class view                                  # html url name ES action="{% url 'cercaimmobile' %}"
    path("messaggio_prenota_ora_da_lista/<pk>/",      MessaggioPrenotaOraView.as_view(),   name="messaggio_prenota_ora_da_lista"),
    re_path(r"^$|^\/$|^home\/$",                RentHomeView.as_view(),                       name="home"),
    path("register/",                           UserCreateView.as_view(),                     name="register"),
    path("login/",                              v.LoginView.as_view(),                        name="login"),
    path("logout/",                             v.LogoutView.as_view(),                       name="logout"),
    path("listaimmobili/",                      ImmobileListView.as_view(),                   name="listaimmobili"),
    path("ricerca/",                            SearchAndRedirectView.as_view(),              name="cercaimmobile"),
    path("ricerca/get_hint/",                   AjaxSearchGetHintView.as_view(),              name="get_hint"),
    path("ricerca/<str:sstring>/<str:where>/",  RicercaImmobileView.as_view(),                name="ricerca_risultati"),
    path('admin/',                              admin.site.urls),
    path("gestione/",                           include("gestione.urls")), # app
    re_path(r"^init_db/$",                      InitDBView.as_view(),                         name="init_db"), # dev mode
]



