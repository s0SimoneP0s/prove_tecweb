from ilpoker import il_poker
import re

class PokerCard:

    #static attributes
    seeds = ["CUORI", "PICCHE", "FIORI", "QUADRI"]
    regex = r"^[AJKQ2-9]$|^10$"

    def __init__(self, v: str, s: str):
        self.s = s
        self.v = str(v)

    @property
    def s(self):
        return self.__s

    @s.setter
    def s(self,s):
        if s not in PokerCard.seeds:
            raise ValueError(str(s)+ " Seme non valido")
        else:
            self.__s = s
    
    @s.getter
    def s(self):
        return self.__s

    @property
    def v(self):
        return self.__v

    @v.getter
    def v(self):
        return self.__v

    @v.setter
    def v(self,v):
        if not re.match(PokerCard.regex,v):
            raise ValueError(str(v) + " Valore non ammissibile")
        else: 
            self.__v = v

    def __lt__(self, o):

        values = [0,0]
        for i,x in enumerate((self.v, o.v)):
            values[i] = PokerCard.from_carta_to_int(x)

        if values[0] < values[1]: return True
        else: return False
 

    def __str__(self):
        return self.v + " di " + self.s

    @staticmethod
    def from_carta_to_int(x):
        if x == "A":  return 14
        elif x == "K": return 13
        elif x == "Q": return 12
        elif x == "J": return 11
        else: return int(x)

    @staticmethod
    def calcola_punto(carte): #carte devono essere sorted!
        
        #scala colore
        #poker
        #full
        #colore
        #scala
        #tris
        #doppia coppia
        #coppia
        #carta alta

        colore = False

        s = set()
        for c in carte:
            s.add(c.s)
        if len(s) == 1:
            colore = True

        scala = True

        for i in range(len(carte)-1):
            if (PokerCard.from_carta_to_int(carte[i].v)+1) != PokerCard.from_carta_to_int(carte[i+1].v):
                scala = False
                break

        if scala and colore:
            print("SCALA COLORE!")
            return

        d = {}
        for c in carte:
            if c.v not in d:
                d[c.v] = 1
            else: d[c.v] += 1
            if d[c.v] == 4:
                print("POKER di " + c.v)
                return
        
        if len(d) == 2: #solo 2 chiavi diverse, per 5 carte. E' full...
            print("FULL")
            return

        if colore:
            print("COLORE")
            return

        if scala:
            print("SCALA")
            return

        max_punto = max(d.values())

        if max_punto > 1:

            max_punto_s = "COPPIA"
            if max_punto == 3: max_punto_s = "TRIS"
            count = 0
            val = None

            for i in d:
                if max_punto == d[i]:
                    count += 1
                    val = i

            if count==2: 
                max_punto_s = "DOPPIA " + max_punto_s
                print(max_punto_s)
                return

            print(max_punto_s + " di " + val)
            return

        print("CARTA ALTA: " + carte[len(carte)-1].v)
                    
            
    
if __name__ == "__main__":

    estrazione = il_poker(False)

    # for tests:
    #estrazione = [ ("A","PICCHE"),("J","PICCHE"),("2","PICCHE"),("4","PICCHE"),("9","PICCHE")]
    #estrazione = [ ("10","PICCHE"),("J","PICCHE"),("Q","PICCHE"),("K","PICCHE"),("A","PICCHE")]
    #estrazione = [ ("10","PICCHE"),("10","FIORI"),("Q","QUADRI"),("Q","CUORI"),("Q","PICCHE")]
    #estrazione = [ ("3","PICCHE"),("4","FIORI"),("5","QUADRI"),("6","CUORI"),("7","PICCHE")]
    #estrazione = [ ("3","PICCHE"),("3","FIORI"),("3","QUADRI"),("3","CUORI"),("7","PICCHE")]

    l = []
    for e in estrazione:
        l.append(PokerCard(*e))

    l.sort()

    for i in l:
        print(i)

    PokerCard.calcola_punto(l)
    
    
    
