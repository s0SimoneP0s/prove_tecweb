import time
import asyncio
import threading

async def mossa(mio_tempo,suo_tempo):
    print(threading.current_thread().name)
    mia_mossa(mio_tempo)
    await mossa_avversaria(suo_tempo)

def mia_mossa(tempo):
    time.sleep(tempo) #dormi e non fare nient'altro.

async def mossa_avversaria(tempo):
    print(threading.current_thread().name)
    await asyncio.sleep(tempo) #dormi, ma se hai meglio da fare controlla la lista di altre coroutine da eseguire.

async def main(): #async è necessario per poter essere aspettato!
    OPPONENTS = 5
    OPP_TIME_TO_THINK = 1
    MY_MOVE_TIME = 1
    MAX_MOVES = 2

    # totale = 2 mosse * 5 avversari * 1 (mio tempo di mossa) + spicci... = circa >10
    print(threading.current_thread().name)
    l=[]
    #riempiamo un array di funzioni di tipo async
    for _ in range(OPPONENTS*MAX_MOVES):
        l.append(mossa(MY_MOVE_TIME,OPP_TIME_TO_THINK))

    await asyncio.gather(*l) #gather schedula ed esegue "awaitable objects" uno dopo l'altro.


if __name__ == "__main__":
    print(threading.current_thread().name)
    s = time.perf_counter()
    asyncio.run(main()) #aspettiamo che finiscano tutti.
    e = time.perf_counter()
    print("ELAPSED " + str(e-s))
   