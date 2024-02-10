from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def welcome_user(request):
    string = "welcome_"
    out = request.path[len(string)+1:]
    return HttpResponse("Ciao, " + out)


def welcome_path(request,nome,eta):
    return HttpResponse("Si chiama " + nome + "<br> ed ha " + str(eta) + " anni")

#richiede
#python manage.py migrate
#altrimenti tutto quello che riguarda "user" fallisce!
#vedere warning "unapplied migrations"
def home_page(request):

    response = "Benvenuto nella Homepage, \n" + str(request.user)
    
    """
    print("RESPONSE " + str(request))
    print("Caratteristiche di request " + str(dir(request)))

    for e in request.__dict__:
        print(e)

    print("USER " + str(request.user))
    print("PATH " + str(request.path))
    """

    if not request.user.is_authenticated:
        logger.warning(str(request.user) + " non è autenticato!")

    return HttpResponse(response)


def elenca_params(request):

    response = ""
    for k in request.GET:
        response += request.GET[k] + " "

    return HttpResponse(response)


def welcome_name(request):
    if "nome" in request.GET:
        return HttpResponse("Ciao, " + request.GET["nome"])
    else:
        return HttpResponse("Non mi hai dato abbastanza parametri!")

def pari_dispari(request):
    try:
        n = int(request.GET["num"])
        if n%2==0: return HttpResponse("Pari")
        else: return HttpResponse("Dispari")
    except:
        return HttpResponse("Non è un numero")


def hello_template(request):
    #occorre importare 
    #from datetime import datetime e
    #from django.shortcuts import render

    ctx = { "title" : "Hello Template",
    "lista" : [ datetime.now(), datetime.today().strftime('%A'), datetime.today().strftime('%B')]}

    template = "baseext.html"
    #template = "baseinclude.html"

    return render(request, template_name=template, context=ctx)


#Dimostrazione di lettura tramite DTL di parametri passati tramite get o 
#tramite url path.
#il contesto ha una sola variabile booleana che ci dice se elencare
#i parametri get o i parametri passati tramite url.
#i parametri passati sono string:nome e int:eta 
def hello_params_get(request):
    return hello_params(request,True)

def hello_params_url(request, nome: str, eta: int):
    return hello_params(request,False)

def hello_params(request, getv):
    return render(request, template_name="params.html",context={"get":getv})


def page_with_static(request):
    return render(request, template_name="pwstatic.html",context={"title":"Pagina con elementi statici"})