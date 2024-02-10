'''
Dimostrazione identità degli oggetti in python
'''

class OggettoCustom:
    def __init__(self, a):
        self.a = a

    def __str__(self):
        return str(self.a)

print("Dimostrazione con variabili intere")
x = 5
y = x

print(  x is y  )
print( str(id(x)) + " " + str(id(y))  )

x = 5
y = x
x += 1
print(  x is y  )
print( str(id(x)) + " " + str(id(y)) )
print("Perchè?")
print(str(x) + " " + str(y)) #immutabilità!


print("Dimostrazione con oggetti generici")

x = OggettoCustom(10)
y = x

print(  x is y  )
print( str(id(x)) + " " + str(id(y))  )

x.a = 5
print(str(x) + " " + str(y))


y = OggettoCustom(10)

print(  x is y  )
print( str(id(x)) + " " + str(id(y))  )

