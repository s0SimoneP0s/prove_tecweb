from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.utils import timezone
from .models import Libro, Copia

# Create your views here.

def lista_libri(request):
    ctx = {
        "title" : "Lista di Libri",
        "listalibri" : Libro.objects.all()
    }
    return render(request, template_name="gestione/listalibri.html",context=ctx)


def presta_libro(request, titolo, autore):

    l = get_object_or_404(Libro, titolo=titolo, autore=autore)

    s = l.copie.filter(data_prestito=None)
    tmpl = "gestione/prestalibro.html"
 
    msg = ""
    if s.count() == 0:
        msg = "Non ci sono copie disponibili!"
        print(msg)
        return render(request,template_name=tmpl,
                      context={"title":"Prestito di un Libro", "message":msg})

    try:
        c = Copia.objects.get(pk=s[0].id)
        c.data_prestito = timezone.now()
        c.save()
        msg = "Prestito eseguito con successo! Hai ora la copia con ID " + str(c.id)
    except Exception as e:
        msg = "Errore nel prestito! " + str(e)

    ctx = {"title":"Prestito di un Libro", "message":msg}

    return render(request,template_name=tmpl,context=ctx)

def restituisci_lista(request, titolo, autore):

    l = get_object_or_404(Libro, titolo=titolo, autore=autore)
    s = l.copie.exclude(data_prestito=None)
    tmpl = "gestione/restituiscilibro.html"
    action = "lista"
    titolo = "Scegli copia da restituire: " + titolo + " " + autore
    ctx = {"title":titolo, "action":action, "listacopie":s}
    return render(request,template_name=tmpl,context=ctx)

def restituisci_final(request, pk):

    c = get_object_or_404(Copia, pk=pk)
    tmpl = "gestione/restituiscilibro.html"
    action = "ok"
    titolo = "Conferma Restituzione"

    if c.scaduto == True:
        action = "scaduto"

    c.data_prestito = None
    c.scaduto = False
    
    try:
        c.save()
    except Exception as e:
        action = "Errore nella restituzione " + str(e)

    ctx = {"title":titolo,"action":action}
    return render(request,template_name=tmpl,context=ctx)

    





        

    

