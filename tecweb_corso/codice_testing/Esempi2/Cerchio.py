#!/usr/bin/python

import math

class Cerchio:
	
	#requisito: raggio deve essere un numero positivo di tipo float
	def __init__(self, r):
		self.raggio(r)  #settaggio del parametro raggio attraverso il metodo get/set omonimo

	#metodo get/set del raggio 
	def raggio(self, r = None):
		"""metodo opzionale per cambiare il comportamento tra get e set"""
		if r != None:  #caso set
			if (isinstance(r, float) == False):
				raise TypeError("il raggio deve essere float")
			if (r < 0.0):
				raise ValueError("il raggio deve essere non negativo")
			self.__r = r
		return self.__r

	def perimetro(self):
		return 2 * math.pi * self.raggio()

	def area(self):
		return math.pi * (self.raggio() ** 2)
