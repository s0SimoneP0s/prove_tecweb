from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

from datetime import  timedelta
from math import radians, sin, cos, sqrt, atan2


#####################################################################################
#               zona
#####################################################################################

class Zona(models.Model):
    TIPI_PERMESSI=["Stato","Regione","Provincia","Comune","Indirizzo"]
    confinanti = models.ManyToManyField('self', symmetrical=True, blank=True )
    soprazona = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='zona_confinanti') 
    nome = models.CharField(max_length=100,null=False) 
    latitudine = models.DecimalField(max_digits=9, decimal_places=6) 
    longitudine = models.DecimalField(max_digits=9, decimal_places=6) 
    tipo = models.CharField(max_length=20,null=False) 

    def __str__(self):
        return self.nome
    
    @classmethod
    def __new_zone(cls, nome=None, latitudine=None, longitudine=None, confinanti=None, soprazona=None, tipo=None):
        return cls.objects.create(nome=nome, latitudine=latitudine, longitudine=longitudine, confinanti=confinanti, soprazona=soprazona, tipo=tipo)

    def aggiungi_soprazona(self,nuova=None,nome=None, latitudine=None, longitudine=None, confinanti=None, soprazona=None, tipo=None):
        if not nuova:
            nuova = self.__new_zone(nome=nome, latitudine=latitudine, longitudine=longitudine, confinanti=confinanti, soprazona=soprazona, tipo=tipo)
        self.soprazona=nuova
        return nuova

    def aggiungi_confinanti(self,nuova=None,nome=None, latitudine=None, longitudine=None, confinanti=None, soprazona=None, tipo=None):
        if not nuova:
            nuova = self.__new_zone(nome=nome, latitudine=latitudine, longitudine=longitudine, confinanti=confinanti, soprazona=soprazona, tipo=tipo)
        self.confinanti.add(nuova)
        return nuova

    def calcola_distanza(self, altra_zona):
        # Raggio medio della Terra in chilometri
        diametro_terra= 12742.0
        raggio_terra_km = diametro_terra /2
        
        # Conversione delle coordinate in radianti
        lat1, lon1, lat2, lon2 = map(radians, [self.latitudine, self.longitudine, altra_zona.latitudine, altra_zona.longitudine])

        # Formula di Haversine
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distanza_km = raggio_terra_km * c
        return distanza_km

#####################################################################################
#               Utente Iscritti built in User
#####################################################################################

#####################################################################################
#               utente cliente
#####################################################################################

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    indirizzo = models.ForeignKey(Zona, on_delete=models.CASCADE, null=False)
    def __str__(self):
        return f"{self.user.username} - {self.indirizzo.nome} - {self.numero_telefono}"
    class Meta:
        verbose_name_plural = "clienti"


#####################################################################################
#               utente proprietario
#####################################################################################

class Proprietario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    indirizzo = models.ForeignKey(Zona, on_delete=models.CASCADE, null=False)
    numero_telefono = models.CharField(max_length=20, null=False)
    def __str__(self):
        return f"{self.user.username} - {self.indirizzo.nome} - {self.numero_telefono}"
    class Meta:
        verbose_name_plural = "proprietari"


#####################################################################################
#               immobile
#####################################################################################

class Immobile(models.Model):
    proprietario = models.ForeignKey(Proprietario, on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    indirizzo = models.ForeignKey(Zona, on_delete=models.SET_NULL, null=True, blank=True)
    data_creazione = models.DateTimeField(default=timezone.now)
    confermato_da_admin = models.BooleanField(default=False)
    prezzo = models.DecimalField(max_digits=10, decimal_places=2)
    foto = models.ImageField(upload_to='static/immobili/', blank=True, null=True)

    def disponibile(self):
        list_prenot = Prenotazione.objects.all()
        prenotati=[x.immobile.pk for x in list_prenot if not x.attiva() ]
        if self.confermato_da_admin and self.pk not in prenotati:
            return True
        return False

    def __str__(self):
        return f"{self.nome} di {self.zona} costo giornaliero € {self.prezzo}"

    class Meta:
        verbose_name_plural = "Immobili"

#####################################################################################
#               prenotazione
#####################################################################################


class Prenotazione(models.Model):
    utente = models.ForeignKey(User, on_delete=models.CASCADE,related_name="prenotazioni_utente")
    immobile = models.ForeignKey(Immobile,on_delete=models.CASCADE,related_name="prenotazioni")
    data_prenotazione = models.DateTimeField(default=timezone.now)
    durata = models.PositiveIntegerField(default=15)

    def attiva(self):
        termine=self.data_prenotazione + timedelta(days=self.durata)
        adesso=timezone.now()
        if self.data_prenotazione  < adesso and adesso < termine:
            return True
        return False


    def passata(self):
        termine=self.data_prenotazione + timedelta(days=self.durata)
        adesso=timezone.now()
        if adesso > termine:
            return True
        return False

    def futura(self):
        termine=self.data_prenotazione + timedelta(days=self.durata)
        adesso=timezone.now()
        if adesso < self.data_prenotazione:
            return True
        return False

    def __str__(self):
        return f"Prenotazione di {self.immobile.nome} di {self.immobile.zona} affittato dal {str(self.data_prenotazione)} per {self.durata} giorni"

    class Meta:
        verbose_name_plural = "Prenotazioni"


#####################################################################################
#               recensione
#####################################################################################


class Recensione(models.Model):
    utente = models.ForeignKey(User, on_delete=models.CASCADE)
    immobile = models.ForeignKey(Immobile, on_delete=models.CASCADE)
    testo = models.TextField()
    stelline = models.IntegerField(choices=[(i, str(i)) for i in range(0, 5)])

    def __str__(self):
        return f"Recensione di {self.immobile} di {self.utente}"
    class Meta:
        verbose_name_plural = "recensioni"