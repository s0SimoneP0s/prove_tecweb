'''
Dimostrazione di dinamicità di tipo in python,
inoltre, esempio di tipizzazione "suggerita".

Infine, float vs. double
'''

#tipizzazione dinamica
a = 3

print("Tipo di a: " + str(type(a)))

a = "Ciao"

print("Tipo di a: " + str(type(a)))

#tipizzazione suggerita
a : int 

a = "cinque"

print("Tipo e valore di a: " + str(type(a)) + " " + str(a))

##########################################################

'''
Secondo IEEE 754:
limits:
        min                         max
float	1.175494351 E -38	        3.402823466 E +38
double	2.2250738585072014 E-308	1.7976931348623158 E +308

'''

a = 1.7976931348623158e308

print(str(a-1) + str(type(a)))
