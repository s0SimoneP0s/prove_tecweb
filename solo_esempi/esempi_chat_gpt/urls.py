# urls.py
from django.urls import path
from .views import ItemCreateView, ItemListView, ItemDetailView

urlpatterns = [
    path('item/create/', ItemCreateView.as_view(), name='item-create'),
    path('item/list/', ItemListView.as_view(), name='item-list'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),  # URL per la DetailView
    # Aggiungi altre URL se necessario
]
