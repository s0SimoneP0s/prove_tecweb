from email.policy import default
from django.db import models
import datetime
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE,related_name="choices")
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text
