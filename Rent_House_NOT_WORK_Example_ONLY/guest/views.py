from django.shortcuts import render,redirect
from .init_db_app import erase_db,init_db_sql,group_create

import logging # prova logger
# Create your views here.


from .models import Immobile

def front_page(request):
    house = Immobile.objects.all()
    if bool(house):
        n = len(house)
        nslide = n // 3 + (n % 3 > 0)
        houses = [house, range(1, nslide), n]
        app = {'house': houses , 'room' : True}

    return render(request, 'home.html', app)




def lista_immobili(request):
    print(request)
    immobili = Immobile.objects.all()
    print(immobili)
    return render(request, 'lista_immobili.html', {'immobili': immobili})

def init_db(request):
    #erase_db()
    print("esecuzione script DB")
    init_db_sql()
    #group_create()
    return lista_immobili(request)
