from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.http import HttpResponse

# pipenv install django-braces
from braces.views import GroupRequiredMixin

# Create your views here.

def gestione_home(request):
    return render(request,template_name="gestione/home.html")


class LibroListView(ListView):
    titolo = "La nostra biblioteca possiede"
    model = Libro
    template_name = "gestione/lista_libri.html"


def search(request):

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            sstring = form.cleaned_data.get("search_string")
            where = form.cleaned_data.get("search_where")
            return redirect("gestione:ricerca_risultati", sstring, where)
    else:
        form = SearchForm()

    return render(request,template_name="gestione/ricerca.html",context={"form":form})
    #return render(request,template_name="gestione/ricerca_ajax.html",context={"form":form})

class LibroRicercaView(LibroListView):
    titolo = "La tua ricerca ha dato come risultato"

    def get_queryset(self):
        sstring = self.request.resolver_match.kwargs["sstring"] 
        where = self.request.resolver_match.kwargs["where"]

        if "Titolo" in where:
            qq = self.model.objects.filter(titolo__icontains=sstring)
        else:
            qq = self.model.objects.filter(autore__icontains=sstring)

        return qq

@login_required
def prestito(request, pk):
    l = get_object_or_404(Libro,pk=pk)

    errore = "NO_ERRORS"
    if l.disponibile() == False:
        errore = "Non vi sono copie disponibili"

    copie_in_prestito = request.user.copie_in_prestito.all()

    if copie_in_prestito.filter(libro__autore__iexact=l.autore,libro__titolo__iexact=l.titolo).count() != 0:
        errore = "Hai già una copia di quel libro!"

    copia = None
    if errore == "NO_ERRORS":
        for c in l.copie.filter(data_prestito=None):
            c.data_prestito = timezone.now()
            c.utente = request.user
            copia = c
            break

    if copia != None:       
        try:
            copia.save()
            print("Copia salvata con successo " + str(copia) + " in prestito: " + copia.chi_in_prestito())
        except Exception as e:
            errore = "Errore nella registrazione del prestito"
            print(errore + " " + str(e))

    return render(request,"gestione/prestito.html",{"errore":errore,"libro":l,"copia":copia})

@login_required
def my_situation(request):
    user = get_object_or_404(User, pk=request.user.pk)
    copie = user.copie_in_prestito.all()
    ctx = { "listacopie" : copie }
    return render(request,"gestione/situation.html",ctx)

class RestituisciView(LoginRequiredMixin, DetailView):
    model = Copia
    template_name = "gestione/restituzione.html"
    errore = "NO_ERRORS"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        c = ctx["object"]

        if c.data_prestito != None:

            if c.utente.pk != self.request.user.pk:
                self.errore = "Non puoi restituire un libro non tuo!"

        else:
            self.errore = "Libro attualmente non in prestito"

        if self.errore == "NO_ERRORS":
            try:
                c.data_prestito = None
                c.utente = None
                c.save()
            except Exception as e:
                print("Errore! " + str(e))
                self.errore = "Errore nell'operazione di restituzione"

        return ctx

def get_hint(request):

    response = request.GET["q"]

    if(request.GET["w"]=="Titolo"):
        q = Libro.objects.filter(titolo__icontains=response)
        if len(q) > 0: 
            response = q[0].titolo
    else: 
        q = Libro.objects.filter(autore__icontains=response)
        if len(q) > 0: 
            response = q[0].autore

    return HttpResponse(response)

#Views per soli Bibliotecari 

class BiblioSituationView(GroupRequiredMixin, ListView):
    group_required = ["Bibliotecari"]
    model = Libro
    template_name = "gestione/situationb.html"

class BiblioDetailView(GroupRequiredMixin, DetailView):
    group_required = ["Bibliotecari"]
    model = Libro
    template_name = "gestione/detailb.html"

class CreateLibroView(GroupRequiredMixin, CreateView):
    group_required = ["Bibliotecari"]
    title = "Aggiungi un libro alla biblioteca"
    form_class = CreateLibroForm
    template_name = "gestione/create_entry.html"
    success_url = reverse_lazy("gestione:home")

class CreateCopiaView(CreateLibroView):
    title = "Aggiungi una Copia ad un libro"
    form_class = CreateCopiaForm

