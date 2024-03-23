# myapp/forms.py
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Item

# create
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))

# list
class ItemFilterForm(forms.Form):
    """Classe che aggiunge il filtro alla vista lista
    Va tolta se non si vuole il filtro"""
    name = forms.CharField(label='Name', required=False)

    def __init__(self, *args, **kwargs):
        super(ItemFilterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.add_input(Submit('submit', 'Filter'))


# detail
class ItemDetailForm(forms.ModelForm):
    """Classe che aggiunge l'update alla vista lista
    Va tolta se non si vuole il filtro"""
    class Meta:
        model = Item
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'readonly': 'readonly'})
        }

    def __init__(self, *args, **kwargs):
        super(ItemDetailForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Update', css_class='btn btn-primary'))