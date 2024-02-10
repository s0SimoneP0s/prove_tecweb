from django.contrib import admin
from .models import Libro, Copia

# Register your models here.

admin.site.register(Libro)
admin.site.register(Copia)