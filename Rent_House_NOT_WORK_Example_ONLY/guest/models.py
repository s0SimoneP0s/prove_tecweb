from django.db import models

# Create your models here.


from django.utils import timezone
from django.contrib.auth.models import User


class Proprietario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    indirizzo = models.CharField(max_length=255, blank=True, null=True)
    numero_telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name_plural = "proprietari"

class Immobile(models.Model):
    proprietario = models.ForeignKey(Proprietario, on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    prezzo = models.DecimalField(max_digits=10, decimal_places=2)
    zona = models.CharField(max_length=100)
    data_creazione = models.DateTimeField(default=timezone.now)
    confermato_da_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.nome
    class Meta:
        verbose_name_plural = "immobili"


class Prenotazione(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    immobile = models.ForeignKey(Immobile, on_delete=models.CASCADE)
    data_prenotazione = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prenotazione di {self.immobile} da {self.cliente}"
    class Meta:
        verbose_name_plural = "prenotazioni"



class Recensione(models.Model):
    utente = models.ForeignKey(User, on_delete=models.CASCADE)
    immobile = models.ForeignKey(Immobile, on_delete=models.CASCADE)
    testo = models.TextField()
    stelline = models.IntegerField(choices=[(i, str(i)) for i in range(0, 5)])

    def __str__(self):
        return f"Recensione di {self.immobile} di {self.utente}"
    class Meta:
        verbose_name_plural = "recensioni"