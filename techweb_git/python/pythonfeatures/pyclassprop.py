class Cerchio:

    def __init__(self,raggio = 1):
        self.raggio = raggio

    def __str__(self):
        return "Questo cerchio ha raggio " + str(self.raggio)

    @property
    def raggio(self):
        return self.__raggio

    @raggio.setter
    def raggio(self,value):
        if value <= 0: 
            self.__raggio = 1
            print("Errore!")
        else: self.__raggio = value 

    @raggio.getter
    def raggio(self):
        return self.__raggio


c = Cerchio(-3)
print(c)
c.raggio = -2
print(c)
c = Cerchio(3)
print(c)

