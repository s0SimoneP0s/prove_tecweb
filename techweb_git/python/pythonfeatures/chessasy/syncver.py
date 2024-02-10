import time

def mia_mossa(tempo):
    time.sleep(tempo)

def mossa_avversaria(tempo):
    time.sleep(tempo)

if __name__ == "__main__":
    OPPONENTS = 5
    OPP_TIME_TO_THINK = 1 #tempo necessario per far pensare l'avversario 
    MY_MOVE_TIME = 1 #tempo necessario per far pensare me stesso
    MAX_MOVES = 2 #in quante mosse vogliamo vincere

    # totale = 2*5*(1+1) = circa 20 secs.

    s = time.perf_counter()

    for _ in range(MAX_MOVES):          #per ogni mossa
        for _ in range(OPPONENTS):      #per ogni avversario
            mia_mossa(MY_MOVE_TIME)
            mossa_avversaria(OPP_TIME_TO_THINK)


    e = time.perf_counter()

    print("ELAPSED " + str(e-s))





