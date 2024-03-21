from django.urls import path,re_path

from . import views

urlpatterns = [
    #path('', views.front_page, name='front'),
    re_path(r"^$|^/$|^home/$|''",views.front_page,name="front"), # next 404
    re_path(r"^lista_immobili/$",views.lista_immobili,name="lista_immobili"),
#    re_path(r"^lista_immobili$",views.front_page,name="front"),
    re_path(r"^init_db/$",views.init_db,name="init_db"),
]
