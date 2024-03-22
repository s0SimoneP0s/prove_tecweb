from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import *

class SearchForm(forms.Form):

    CHOICE_LIST = [("Titolo","Cerca tra i titoli"), ("Autore","Cerca tra gli autori")]
    helper = FormHelper()
    helper.form_id = "search_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit","Cerca"))
    search_string = forms.CharField(label="Cerca qualcosa",max_length=100, min_length=3, required=True)
    search_where = forms.ChoiceField(label="Dove?", required=True, choices=CHOICE_LIST)


class CreateLibroForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "addlibro_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit","Aggiungi Libro"))

    class Meta:
        model = Libro
        fields = ["titolo","autore","pagine"]

class CreateCopiaForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "addcopia_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit","Aggiungi Copia"))

    class Meta:
        model = Copia
        fields = ["libro"]





