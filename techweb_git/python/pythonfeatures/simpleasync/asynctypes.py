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

input("Premi un tasto per lanciare la funzione async con gather")

a = asyncio.gather(funza())
print(type(a))

#input("Premi un tasto per lanciare la funzione async con run")
    
#a = asyncio.run(funza())
#print(type(a))