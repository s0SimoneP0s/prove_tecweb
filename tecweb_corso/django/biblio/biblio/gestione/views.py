from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Libro
from django.utils import timezone


def lista_libri(request):
    templ = "gestione/listalibri.html"

    ctx = { "title":"Lista di Libri",
            "listalibri": Libro.objects.all()}

    return render(request,template_name=templ,context=ctx)

MATTONE_THRESHOLD = 300

def mattoni(request):
    templ = "gestione/listalibri.html"

    #lista_filtrata = Libro.objects.filter(pagine__gte=MATTONE_THRESHOLD)
    lista_filtrata = Libro.objects.exclude(pagine__lt=MATTONE_THRESHOLD)

    #raw query:
    #Attenzione! Non restituisce un QuerySet, ma un RawQuerySet: quindi non può essere 
    #passata al template selezionato (metodo count non esiste per un RawQuerySet)
    raw_qry_set = Libro.objects.raw("SELECT * FROM gestione_libro WHERE pagine >= %s", [MATTONE_THRESHOLD])
    for l in raw_qry_set:
        print(l)

    ctx = { "title":"Lista di Mattoni",
            "listalibri": lista_filtrata}

    return render(request,template_name=templ,context=ctx)


def crea_libro(request):
    message = ""

    if "autore" in request.GET and "titolo" in request.GET:
        aut = request.GET["autore"]
        tit = request.GET["titolo"]
        pag = 100

        try: 
            pag = int(request.GET["pagine"])
        except:
            message = " Pagine non valide. Inserite pagine di default."

        l = Libro()
        l.autore = aut
        l.titolo = tit
        l.pagine = pag
        l.data_prestito = timezone.now()

        try:
            l.save()
            message = "Creazione libro riuscita!" + message
        except Exception as e:
            message = "Errore nella creazione del libro " + str(e) 

    return render(request,template_name="gestione/crealibro.html",
            context={"title":"Crea Autore", "message":message})

#soluzioni esercizi 1
def autore_get(request):
    title = "Ricerca per Autore"
    
    if "autore" not in request.GET:
        title = "Parametro non corretto"
        qs = None
    else:
        author =  request.GET["autore"]
        qs = Libro.objects.filter(autore=author)

    templ = "gestione/listalibri.html"
    ctx = { "title":title,"listalibri": qs}

    return render(request,template_name=templ,context=ctx)

def autore_path(request,autore):
    templ = "gestione/listalibri.html"
    ctx = { "title":"Ricerca per Autore","listalibri": Libro.objects.filter(autore=autore)}

    return render(request,template_name=templ,context=ctx)    



#soluzioni esercizi 2
def delmodlibro(request,libro_da_modificare=None):

    msg = ""
    title = "Elimina Libro"

    templ = "gestione/delmodlibro.html"
    ctx = {}

    if libro_da_modificare == None:
        if "libro" in request.GET:
            s = request.GET["libro"]
            s = s[:s.index(':')]
            try:
                l = Libro.objects.get(pk=int(s))
                l.delete()
                msg = "Rimozione completata!"
            except Exception as e:
                msg = "Errore nella cancellazione dell'entry " + str(e)
        ctx = {"title":title,"listalibri": Libro.objects.all(),"message":msg}
    else:
        title = "Modifica Libro"
        if "autore" in request.GET and "titolo" in request.GET:
            aut = request.GET["autore"]
            tit = request.GET["titolo"]
            pag = 100
            try:
                pag = int(request.GET["pagine"])
            except:
                msg = " Pagine fallback a valore di default"

            libro_da_modificare.autore = aut
            libro_da_modificare.titolo = tit
            libro_da_modificare.pagine = pag

            try:
                libro_da_modificare.save()
                msg = "Aggiornamento completato!" + msg
            except Exception as e:
                msg = "Errore nella modifica dell'entry " + str(e) 

        ctx = {"title":title,"libro": libro_da_modificare,"message":msg}

    return render(request,template_name=templ,context=ctx)    


def cancella_libro(request):
    return delmodlibro(request)

def modifica_libro(request,titolo,autore):
    libro = get_object_or_404(Libro, autore=autore, titolo=titolo)
    return delmodlibro(request,libro)

