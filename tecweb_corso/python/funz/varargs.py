

def fvarargs_v1(*args):
    for a in args:
        print(a)

def fvarargs_v2(a,b,c,d,e,f):
    for i in [a,b,c,d,e,f]:
        print(i)

l = ("a",4,4.3,True,[1,2],False)

fvarargs_v1(*l)
print("========")
fvarargs_v2(*l)

#in entrambi i casi, sarebbe corretto anche:
#fvarargs_v1("a",4,4.3,True,[1,2],False)
#fvarargs_v2("a",4,4.3,True,[1,2],False)


def dict_varargs_v1(**kwargs):
    for e in kwargs:
        print(str(e)+":"+str(kwargs[e]))

def dict_varargs_v2(nome, cognome, eta, lista_mansioni):

    print(nome + " " + cognome + " di anni " + str(eta) + " si occupa di ")

    for s in lista_mansioni:
        print(s)

d = { "eta":77, 
    "lista_mansioni":["Giardino", "Reception", "Magazzino"],
    "nome":"Mario", 
    "cognome":"Rossi"}

dict_varargs_v1(**d)
dict_varargs_v2(**d)


