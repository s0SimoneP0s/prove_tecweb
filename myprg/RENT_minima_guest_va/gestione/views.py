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
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from django.utils import timezone
from django.http import HttpResponseRedirect,HttpResponseNotFound

# pipenv install django-braces
from braces.views import GroupRequiredMixin

from rent.views import (
    UserCreateView,
    )

from .models import (
    Zona,
    )
from .forms import (

    ZonaForm,
    )
#####################################################################################
#               Staff: Zona setting, conferma proprietario
#####################################################################################

@method_decorator(staff_member_required, name='dispatch')
class ZonaCreateView(CreateView,SuccessMessageMixin):
    model = Zona
    form_class = ZonaForm
    template_name = 'gestione/inserimento_zona.html'
    success_url = 'gestione/inserimento_zona.html'  # URL da reindirizzare dopo il salvataggio
    success_message = "Successo!"

#####################################################################################
#               Iscritti: conferma iscrizione, profilo, home gestione
#####################################################################################


class GestioneHomeView(GroupRequiredMixin,View):
    group_required = ["Iscritti"]

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":
            return self.post(request, *args, **kwargs)
        else:
            return self.get(request, *args, **kwargs)

    def get(self, request):
        return render(request, template_name="home.html")

    def post(self, request):
        return render(request, template_name="gestione/gestione_h.html")

#####################################################################################
#               Utente Cliente
#####################################################################################



#####################################################################################
#               Utente proprietario
#####################################################################################





