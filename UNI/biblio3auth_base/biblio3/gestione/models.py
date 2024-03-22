from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Libro(models.Model):
    titolo = models.CharField(max_length=200)
    autore = models.CharField(max_length=50)
    pagine = models.IntegerField(default=100)

    def disponibile(self):
        if self.copie.filter(data_prestito=None).count() > 0:
            return True
        return False
        
    def __str__(self):
        disp = self.copie.filter(data_prestito=None).count()
        out = self.titolo + " di " + self.autore + " ha " + str(self.copie.all().count()) + " copie" + " di cui " + str(disp) + " disponibili"
        return out

    class Meta:
        verbose_name_plural = "Libri"

class Copia(models.Model):
    data_prestito = models.DateField(default=None,null=True,blank=True)
    libro = models.ForeignKey(Libro,on_delete=models.CASCADE,related_name="copie")
    utente = models.ForeignKey(User, on_delete=models.PROTECT,blank=True,null=True,default=None,related_name="copie_in_prestito")

    def chi_in_prestito(self):
        if self.utente == None: return None
        return self.utente.username

    def __str__(self):
        return "Copia di " + self.libro.titolo + " di " + self.libro.autore + " in prestito dal " + str(self.data_prestito) 

    class Meta:
        verbose_name_plural = "Copie"
