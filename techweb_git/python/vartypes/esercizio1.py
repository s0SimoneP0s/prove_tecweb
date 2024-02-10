#prima versione: very basic

print("Inserisci raggio: ")
r = input() #restituisce sempre una stringa
r = int(r)
area = r*r*3.14
print(f"Area è {area}")

#seconda versione: compatta
r = int(input("Inserisci raggio: "))
print(f"Area è {r**2*3.14}")

#terza versione: check input ed import
import math
r = input("Inserisci raggio: ")

try:
    r = int(r)
except:
    print("Non hai inserito un numero intero!")
    exit(-1)

area = r**2*math.pi
print(f"Area è {area}")