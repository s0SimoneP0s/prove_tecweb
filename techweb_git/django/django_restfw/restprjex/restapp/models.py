from django.db import models

# Create your models here.


#Original JSON structure...
#'userId': 1, 'id': 1, 'title': 'delectus aut autem', 'completed': False

class ToDo(models.Model):
    #id è la chiave. La facciamo generare al DBMS
    userIP = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
