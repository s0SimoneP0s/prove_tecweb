from django.shortcuts import render

# Create your views here.

# myapp/views.py
from django.views.generic import CreateView,ListView,DetailView
from .models import Item


from django.urls import reverse_lazy
from .forms import ItemForm,ItemFilterForm,ItemDetailForm

class ItemCreateView(CreateView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('item-list')  # Redirects to item list upon successful creation


class ItemListView(ListView):
    model = Item
    template_name = 'esempi_chat_gpt/item_list.html'  # Template da utilizzare per la ListView
    context_object_name = 'item_list'  # Nome del context object nella template

    def get_context_data(self, **kwargs):
        """Da togliere se vogliamo solo la vista lista senza filtro, 
        altrimenti questa è una vista filtro"""
        context = super().get_context_data(**kwargs)
        context['filter_form'] = ItemFilterForm(self.request.GET)
        return context


class ItemDetailView(DetailView):
    model = Item
    template_name = 'esempi_chat_gpt/item_detail.html'  # Template da utilizzare per la DetailView
    context_object_name = 'item'  # Nome del context object nella template

    def get_context_data(self, **kwargs):
        """Da togliere se vogliamo solo la vista dettaglio senza inserimento, 
        altrimenti questa è una vista update"""
        context = super().get_context_data(**kwargs)
        context['detail_form'] = ItemDetailForm(instance=self.object)
        return context