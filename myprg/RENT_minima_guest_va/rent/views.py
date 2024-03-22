#####################################################################################
#               imports
#####################################################################################
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy,reverse

from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView

from django.utils import timezone


from django.shortcuts import render,redirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator
from django.http import HttpResponse

from gestione.models import (
    Immobile,
    )

from .forms import (
    SearchAppartamentiForm,
    CreaUtente,
    )

from django.shortcuts import render
from django.views import View

from .init_db_app import init_db_sql
#####################################################################################
#               dev init db
#####################################################################################

class InitDBView(View):
    def get(self, request):
        print("******esecuzione script DB******")
        init_db_sql()
        error_message = """<p>Script lanciato ed eseguito</p>"""
        return HttpResponse(error_message, status=200)


#####################################################################################
#               Front page guest, vetrina
#####################################################################################

class RentHomeView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":
            return self.post(request, *args, **kwargs)
        else:
            return self.get(request, *args, **kwargs)
    @method_decorator(login_required)
    def post(self, request):
        return render(request, template_name="gestione/gestione_h.html")
    def get(self, request):
        return render(request, template_name="home.html")

#####################################################################################
#               Immobili
#####################################################################################

class ImmobileListView(ListView):
    nome = "Le nostre offerte affitti contengono"
    model = Immobile
    template_name = "lista_immobili.html"


class MessaggioPrenotaOraView(View):

    @login_required
    def post(self, request, pk):
        l = get_object_or_404(Immobile, pk=pk)
        errore = "NO_ERRORS"
        if not l.disponibile():
            errore = "Non vi sono immobili disponibili"
        prenotazioni_utente = request.user.prenotazioni_utente.all()
        if prenotazioni_utente.filter(immobile__zona__iexact=l.zona, immobile__nome__iexact=l.nome).exists():
            errore = "Hai già affittato quell'appartamento!"
        prenotazione = None
        if errore == "NO_ERRORS":
            for c in l.prenotazioni.filter(data_prenotazione=None):
                c.data_prenotazione = timezone.now()
                c.utente = request.user
                prenotazione = c
                break
            if prenotazione:
                try:
                    prenotazione.save()
                    print(f"Prenotazione salvata con successo {prenotazione} in messaggio_prenota_ora_da_lista: {prenotazione.utente_in_affitto()}")
                except Exception as e:
                    errore = f"Errore nella registrazione del contratto affitto: {e}"
                    print(errore)
        return render(request, "gestione/messaggio_prenota_ora_da_lista.html", {"errore": errore, "immobile": l, "prenotazione": prenotazione})


#####################################################################################
#               Ricerche immobili
#####################################################################################

class RicercaImmobileView(ImmobileListView):
    nome = "La tua ricerca ha dato come risultato"
    def get_queryset(self):
        sstring = self.request.resolver_match.kwargs["sstring"] 
        where = self.request.resolver_match.kwargs["where"]
        if "Titolo" in where:
            return self.model.objects.filter(nome__icontains=sstring)
        else:
            return self.model.objects.filter(zona__icontains=sstring)

class SearchAndRedirectView(View):
    template_name = 'ricerca.html'  # Assicura che questo sia il nome del tuo template
    def get(self, request):
        form = SearchAppartamentiForm()
        return render(request, template_name=self.template_name, context={"form": form})

    def post(self, request):
        form = SearchAppartamentiForm(request.POST)
        if form.is_valid():
            sstring = form.cleaned_data.get("search_string")
            where = form.cleaned_data.get("search_where")
            return redirect("ricerca_risultati", sstring=sstring, where=where)
        return render(request, template_name=self.template_name, context={"form": form})

class AjaxSearchGetHintView(View):
    """Anticipa i risulatati della ricerca"""
    def get(self, request):
        response = request.GET.get("q")
        search_where = request.GET.get("w")
        if search_where == "Titolo":
            immobile_query = Immobile.objects.filter(nome__icontains=response)
        else:
            immobile_query = Immobile.objects.filter(zona__icontains=response)
        
        if immobile_query.exists():
            if search_where == "Titolo":
                response = immobile_query.first().nome
            else:
                response = immobile_query.first().zona
        return HttpResponse(response)

#####################################################################################
#               utente
#####################################################################################

class UserCreateView(SuccessMessageMixin,CreateView):
    form_class = CreaUtente
    template_name = "registration/user_create.html"
    success_url = reverse_lazy("login")
    success_message = "Utente creato con successo! Effettua il login per accedere."

