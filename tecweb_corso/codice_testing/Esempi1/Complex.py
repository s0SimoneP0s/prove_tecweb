#!/usr/bin/python

# definizione della classe Complex
class Complex:
	"An example with override of __init__"
	def __init__(self, realpart, imagpart):
		if not isinstance(realpart, (int, float)):
			raise TypeError("real part not a number")
		if not isinstance(imagpart, (int, float)):
			raise TypeError("image part not a number")
		# inizializza 2 variabili di istanza
		self.r = realpart
		self.i = imagpart

	def getreal(self):
		return self.r
	
	def getimg(self):
		return self.i
		


	

