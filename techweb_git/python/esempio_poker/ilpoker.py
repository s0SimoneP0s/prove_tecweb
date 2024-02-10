import random

def carta(c):
    if c==1: return "A"
    elif c==11: return "J"
    elif c==12: return "Q"
    elif c==13: return "K"
    return c

def componi_carte():
    suits = ["CUORI","PICCHE","FIORI","QUADRI"]
    values = [a for a in range(1,13+1)]
    cards = [ (carta(v),s) for s in suits for v in values ]

    return cards

def generator_estrazione(cards):
    cards_cpy = cards.copy()
    while(len(cards_cpy)>0):
        index = random.randint(0,len(cards_cpy)-1)
        yield cards_cpy[index]
        del cards_cpy[index]


def il_poker(stampa=True):
    mazzo = componi_carte()

    #for i,c in enumerate(mazzo):
    #    print(f"{i}: {c}")
        
    g = generator_estrazione(mazzo)
    l = []

    for _ in range(5):
        l.append(next(g))

    if stampa:
        print("Carte Estratte: ")
        print(l)

    return l

#if __name__ == "__main__":
#    il_poker()