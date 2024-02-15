from polls.models import *
import json
import os
import random
from pathlib import Path
from datetime import timedelta
from django.utils import timezone
import html

def erase_db():
    print("Erasing Database tables...")
    Question.objects.all().delete()
    Choice.objects.all().delete()

def init_db():

    if Question.objects.count() > 0:
        return

    data = None

    #taken from: https://opentdb.com/api.php?amount=50&category=18&type=multiple
    #print(os.getcwd())
    filepath = os.path.join(Path(os.getcwd()), "static", "questions", "questions.txt")
    #print(filepath)
    #print(os.path.exists(filepath))

    with open(filepath) as f:
        data = f.read()

    if data == None:
        print("Error in populating database tables!")
        return 

    data = json.loads(data)["results"]

    for i,d in enumerate(data):
        question = d["question"]
        choices = []
        choices.append(d["correct_answer"])
        choices.extend(d["incorrect_answers"])
        random.shuffle(choices)
        date = timezone.now() - timedelta(days=i%10)
        q = Question(question_text=html.unescape(question), pub_date=date)
        q.save()
        #print("DOMANDA " + str(i) + " " + str(q))
        for k,j in enumerate(choices):
            c = Choice(choice_text = html.unescape(j), votes = k, question = q)
            if j == d["correct_answer"]: c.is_correct = True
            c.save()
            #print("Risposta " + str(c))
