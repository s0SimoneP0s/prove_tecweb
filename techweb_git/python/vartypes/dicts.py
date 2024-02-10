
d = {"a":3,"b":3,"c":4,"d":3}

#cancelliamo tutti gli elementi i cui valori eccedono 3

#due soluzioni, ma una è sbagliata...

#spiegazione oltre il codice

try:
    for i in d:
        if d[i] > 3:
            del d[i]
except Exception as e:
    print("Qualcosa è andato storto... " + str(e))
    d["c"] = 4 #re-immettiamo la chiave "c" con 4: l'eliminazione va a buon fine,
               #ma l'iterazione successiva solleva l'eccezione.
else:
    print("Soluzione uno è ok")

print(d) #verifichiamo di aver "rimesso" a posto il dizionario di partenza.

try:
    #for i in list(d.keys()): #Occorre che sia una lista!
    for i in list(d): #equivalente
        if d[i] > 3:
            del d[i]
except Exception as e:
    print("Qualcosa è andato storto... " + str(e))
else:
    print("Soluzione due è ok")

print(d) #(ri)-verifichiamo che funzioni.

#spiegazione:

'''
#d.keys() restituiva una copia delle chiavi del dizionario in python 2, sottoforma di lista.
#In python 3, d.keys() restituisce una "view" delle chiavi del dizionario, sottoforma di iteratore.
#Una view è un riferimento a specchio rispetto al dizionario di partenza.

#esempio: (da visualizzare su pythontutor, https://pythontutor.com/)

d =  {1:2, 2:3} #instanzio un normalissimo dizionario
k = d.keys() #estraggo una view.

d[3] = 4 #modifico il dizionario.

print(k) #la modifica è visibile nella view del dizionario.

#qui mostriamo come d e k siano oggetti distinti:
print(id(d))
print(id(k))

#il fatto che la view si modifichi al modificarsi del dizionario implica che non possiamo 
#modificare il dizionario mentre si itera direttamente su k.

#occorre fare un passaggio in più.

l = list(d)
#oppure
lk = list(k)

#entrambi restituiscono una copia sottoforma di lista del set di chiavi, ergo è
#possibile ciclare e cambiare il d di partenza, senza problemi.

print(id(l))
print(id(lk))

'''  