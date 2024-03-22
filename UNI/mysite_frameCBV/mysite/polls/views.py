from django.urls import reverse_lazy, reverse
from .models import *
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404, redirect, render
from .forms import *

# Create your views here.

class IndexViewList(ListView):
    model = Question
    template_name = 'polls/index.html'

    def get_queryset(self):
        return self.model.objects.order_by('-pub_date')[:20]

class DetailQuestion(DetailView):
    model = Question
    template_name = "polls/detail.html"

##########Form

def search(request):

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            sstring = form.cleaned_data.get("search_string")
            where = form.cleaned_data.get("search_where")
            return redirect("polls:searchresults", sstring, where)
    else:
        form = SearchForm()

    return render(request,template_name="polls/searchpage.html",context={"form":form})
    #return render(request,template_name="polls/crispyf/searchpage.html",context={"form":form})

class SearchResultsList(ListView):

    model = Question
    template_name = "polls/searchresults.html"

    def get_queryset(self):
        sstring = self.request.resolver_match.kwargs["sstring"] 
        where = self.request.resolver_match.kwargs["where"]

        if "Question" in where:
            qq = Question.objects.filter(question_text__icontains=sstring)
        else:
            qc = Choice.objects.filter(choice_text__icontains=sstring)
            qq = Question.objects.none()
            for c in qc:
                qq |= Question.objects.filter(pk=c.question_id)

        return qq

##########ModelChoiceField

def vote(request, pk):

    if request.method == "POST":
        form = VoteForm(data=request.POST, pk=pk)
        #form = VoteFormCrispy(data=request.POST, pk=pk)
        if form.is_valid():
            answer = form.cleaned_data.get("answer")
            return redirect("polls:votecasted", pk, answer.choice_text)
    else:
        q = get_object_or_404(Question,pk=pk)
        form = VoteForm(pk=pk)
        #form = VoteFormCrispy(pk=pk)
        return render(request,template_name="polls/crispyf/vote.html",context={"form":form,"question":q})
        #return render(request,template_name="polls/vote.html",context={"form":form,"question":q})

class VoteCastedDetail(DetailView):
    model = Question
    template_name = "polls/votecasted.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        answer = self.request.resolver_match.kwargs["answer"]
        ctx["answer"] = answer
        correct = ctx["object"].choices.all().get(is_correct=True) 
        if answer in correct.choice_text:
            ctx["message"] = "Right Answer!"
        else:
            ctx["message"] = "Wrong Answer! " + " The right answer was " + str(correct.choice_text)

        try:
            c = ctx["object"].choices.all().get(choice_text=answer) 
            c.votes += 1
            c.save()
        except Exception as e:
            print("Impossible to update vote value " + str(e))

        return ctx

##########Model Forms

class CreateQuestionView(CreateView):
    template_name = "polls/createentry.html"
    #template_name = "polls/crispyf/createentry.html"
    form_class = CreateQuestionForm
    success_url = reverse_lazy("polls:index")

class CreateChoiceView(CreateView):
    template_name = "polls/createentry.html"
    #template_name = "polls/crispyf/createentry.html"
    form_class = CreateChoiceForm

    def get_success_url(self):
        ctx = self.get_context_data()
        pk = ctx["object"].question.pk
        return reverse("polls:detail",kwargs={"pk":pk})