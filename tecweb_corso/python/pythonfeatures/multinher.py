class A:
    def __init__(self,a):
        print("A inizializzato")
        self.a = a

    def metodo(self):
        print(f"Sono A e Stampo {self.a}")

    def metodo_specifico_a(self):
        print("Sono un metodo specifico di A")


class B:
    def __init__(self,b):
        print("B inizializzato")
        self.b = b

    def metodo(self):
        print(f"Sono B e Stampo {self.b}")

#Esempio di classi Ambigue
class ClasseBA(B,A):
    #default constructor

    def metodo(self):
        super().metodo()

class ClasseAB(A,B):
    
    def metodo(self):
        super().metodo()

#Esempio di classi non ambigue:
class ClasseABMigliore(A,B):
    def __init__(self, a=0, b=0):
        A.__init__(self,a)
        B.__init__(self,b)

    def metodo(self):
        A.metodo(self)
        B.metodo(self)

    def metodo_specifico(self):
        print(f"Metodo specifico della classe {type(self)} : ", end="")
        super().metodo_specifico_a()


#oggetto = ClasseBA(3,4) #Errore!
oggetto1 = ClasseBA(3) #inizializza solo B
oggetto1.metodo() #Andrà a chiamare metodo di B
oggetto2 = ClasseAB(4) #inizializza solo A
oggetto2.metodo() #andrà a chiamare metodo di A.

#print(f"Posso comunque raggiungere {oggetto1.a}?") #no...
oggetto1.metodo_specifico_a() #posso farlo? Si. Perchè non usa attributi non inizializzati

oggetto3 = ClasseABMigliore(3,4)
oggetto3.metodo()
oggetto3.metodo_specifico()
oggetto3.metodo_specifico_a()


    