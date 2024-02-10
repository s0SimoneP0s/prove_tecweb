from django.db import models

# Create your models here.

class Studente(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)

    def __str__(self):
        return "ID: " + str(self.pk) + ": " + self.name + " " + self.surname

    class Meta:
        verbose_name_plural = "Studenti"

class Insegnamento(models.Model):
    titolo = models.CharField(max_length=50)
    studenti = models.ManyToManyField(Studente,default=None)
  
    def __str__(self):
        return "ID: " + str(self.pk) + ": " + self.titolo

    class Meta:
        verbose_name_plural = "Insegnamenti"

