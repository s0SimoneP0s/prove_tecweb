from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import *

# Create your views here.

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:20]
    template = loader.get_template('polls/index.html')
    context = {'latest_question_list': latest_question_list}
    return HttpResponse(template.render(context,request))

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def recent(request, n_polls):
    question_list_ord = Question.objects.order_by('-pub_date')
    latest_question_list = []
    for q in question_list_ord:
        if q.was_published_recently():
            latest_question_list.append(q)

    context = {'latest_question_list':latest_question_list[:int(n_polls)]}
    return render(request, 'polls/index.html', context)

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
