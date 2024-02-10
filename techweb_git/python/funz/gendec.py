
def funz_decoratrice(f):
    def inner(a):
        print("Pre process della funzione")
        f(a)
        print("Post process della funzione")
    return inner

@funz_decoratrice
def funzione(a):
    print("Eseguo la funzione con parametro " + str(a))

def div_decor(f):
    def inner(a,b):
        if b==0:
            return "Non posso dividere per zero!"
        return f(a,b)
    return inner

@div_decor
def divisione(a,b):
    return a/b

#funzione("args")
print(divisione(5,0))
print(divisione(5,2))