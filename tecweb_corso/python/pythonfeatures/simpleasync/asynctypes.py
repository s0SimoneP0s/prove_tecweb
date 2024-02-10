import asyncio


def funz():
    print("Funzione sincrona")


async def funza():
    print("Funzione asincrona")
    await asyncio.sleep(1)


a = funz()
print(type(a))

a = funza() #ad un certo punto questa istruzione solleva un warning...
print(type(a))

# commentato per che sbagliato da errore perche 
#input("Premi un tasto per lanciare la funzione async con gather")

a = asyncio.gather(funza())
print(type(a))

# decommentato perche una funzione corutine la lancio e non la aspetto
# prima o poi la deco aspettare

input("Premi un tasto per lanciare la funzione async con run")
 

   
#a = asyncio.run(funza())
#print(type(a))