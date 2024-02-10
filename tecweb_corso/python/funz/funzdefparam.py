
class Oggetto:
    def __init__(self):
        print("Mi creo")
        self.lista = "l i s t a".split()
    

def funzione(o=Oggetto()):
    o.lista.insert(0,"X")
    for e in o.lista:
        print(e,end="")


'''
def funzione_migliore(o : Oggetto = None):
    if o==None:
        o = Oggetto()
    funzione(o)


print("Prima invocazione def param")
funzione_migliore()
print("\n==================")

print("Seconda invocazione con parametro")
o = Oggetto()
o.lista.append("X")
funzione_migliore(o)
print("\n==================")

print("Terza invocazione senza parametro")
funzione_migliore()
print("\n==================")
'''
    

print("Prima invocazione def param")
funzione()
print("\n==================")

print("Seconda invocazione con parametro")
o = Oggetto()
o.lista.append("X")
funzione(o)
print("\n==================")

print("Terza invocazione senza parametro")
funzione()
print("\n==================")


