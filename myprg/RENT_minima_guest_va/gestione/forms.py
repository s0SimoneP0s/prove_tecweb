from django import forms
from django.contrib.auth.models import Group,User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit,Field,Layout
from crispy_forms.bootstrap import FormActions
from .models import Prenotazione,Immobile


from .models import (

    Zona,
    Cliente,
    )
#####################################################################################
#               Staff: Zona, conferma proprietario
#####################################################################################

class ZonaForm(forms.ModelForm):
    class Meta:
        model = Zona
        fields = ['nome', 'latitudine', 'longitudine', 'tipo', 'confinanti', 'soprazona']
    
    def __init__(self, *args, **kwargs):
        super(ZonaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Salva'))




#####################################################################################
#               Utente Iscritto: setting utente, conferma cliente
#####################################################################################

#####################################################################################
#               Utente Cliente: Crea Prenotazioni
#####################################################################################



#####################################################################################
#               Utente Proprietaio: crea Immobili
#####################################################################################





