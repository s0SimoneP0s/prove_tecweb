
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from .models import *

# Create your views here.

class ListaStudentiView(ListView):
    model = Studente
    template_name = "iscrizioni/lista_studenti.html"

#function view equivalente alla CBV ListaStudentiView:
def lista_studenti_function(request):
    lista = Studente.objects.all()
    templ = "iscrizioni/lista_studenti.html"
    ctx = {"object_list":lista}
    return render(request,template_name=templ,context=ctx)

#esercizio 1
class ListaInsegnamentiView(ListView):
    model = Insegnamento
    template_name = "iscrizioni/lista_insegnamenti.html"


class ListaInsegnamentiAttivi(ListView):
    model = Insegnamento
    template_name = "iscrizioni/insegnamenti_attivi.html"

    def get_queryset(self):
        return self.model.objects.exclude(studenti__isnull=True)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #print(context.keys())
        context['titolo'] = "Insegnamenti Attivi"
        return context

class ListaStudentiIscritti(ListView):
    model = Studente
    template_name = "iscrizioni/studenti_iscritti.html"

    def get_model_name(self):
        return self.model._meta.verbose_name_plural

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titolo"] = "Lista Studenti con Iscrizione"
        return ctx

    def get_totale_iscrizioni(self):
        count = 0
        for i in Insegnamento.objects.all():
            count += i.studenti.all().count()
        return count

class CreateStudenteView(CreateView):
    model = Studente
    template_name = "iscrizioni/crea_studente.html"
    fields = "__all__"
    success_url = reverse_lazy("iscrizioni:listastudenti")

class CreateInsegnamentoView(CreateView):
    model = Insegnamento
    template_name = "iscrizioni/crea_insegnamento.html"
    fields = "__all__"
    success_url = reverse_lazy("iscrizioni:listainsegnamenti")

class DetailInsegnamentoView(DetailView):
    model = Insegnamento
    template_name = "iscrizioni/insegnamento.html"

class UpdateInsegnamentoView(UpdateView):
    model = Insegnamento
    template_name = "iscrizioni/edit_insegnamento.html"
    fields = "__all__"
    
    def get_success_url(self):
        pk = self.get_context_data()["object"].pk
        return reverse("iscrizioni:insegnamento",kwargs={'pk': pk})


class DeleteEntitaView(DeleteView):
    
    template_name = "iscrizioni/cancella_entry.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        entita = "Studente"
        if self.model == Insegnamento:
            entita = "Insegnamento"
        ctx["entita"] = entita
        return ctx

    def get_success_url(self):
        if self.model == Studente:
            return reverse("iscrizioni:listastudenti")
        else:
            return reverse("iscrizioni:listainsegnamenti")

class DeleteStudenteView(DeleteEntitaView):
    model = Studente

class DeleteInsegnamentoView(DeleteEntitaView):
    model = Insegnamento

#Bonus: ListView in grado di prendere in ingresso un cognome
#passato come url path i.e. studenti/<str:surname>/
#ed elencare gli studenti con il cognome passato come input.
class ListStudenteBySurname(ListaStudentiView):

    #da ListaStudentiView andiamo ad ereditare gli attributi
    #model e template_name

    #riscriviamo la query. Di default, prenderebbe tutti
    #gli studenti della tabella Studente.
    def get_queryset(self):
        arg = self.kwargs["surname"] #leggiamo l'argomento passato
        qs = self.model.objects.filter(surname__iexact=arg) #case insensitive...
        return qs


#Esercizio complesso
def cerca_studenti(request):
    if request.method == "GET":
        return render(request,template_name="iscrizioni/cerca_studenti.html")
    else:
        if len(request.POST["name"]) < 1:
            nome = "null"
        else: nome = request.POST["name"] 

        if len(request.POST["surname"]) < 1:
            cognome  = "null"
        else: cognome = request.POST["surname"] 
    
        return redirect("iscrizioni:studentecercato",name=nome, surname=cognome)

class ListStudenteByNameAndSurname(ListView):

    model = Studente
    template_name = "iscrizioni/listastudenteinsegnamento.html"

    def get_queryset(self):

        try:
            arg = self.kwargs["name"]
            qs_name = self.model.objects.filter(name__iexact=arg)
        except:
            qs_name = self.model.objects.none()

        try:
            arg = self.kwargs["surname"]
            qs_surname = self.model.objects.filter(surname__iexact=arg)
        except:
            qs_surname = self.model.objects.none()

        return (qs_name | qs_surname)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titolo'] = "Studenti e loro insegnamenti"
        ls = set()
        for s in self.get_queryset():
            for i in Insegnamento.objects.all():
                if s in i.studenti.all():
                    ls.add(i)

        context['set_ins'] = ls
        
        return context



