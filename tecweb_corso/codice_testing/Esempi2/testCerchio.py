#!/usr/bin/python
# coding: utf-8

import unittest
import math
from Cerchio import *

class testCerchio(unittest.TestCase):

	def setUp(self):
		self.c = Cerchio(10.0)

	#consistenza architetturale
	def testObj(self):
		self.assertTrue(
			isinstance(self.c, Cerchio), 
			"c non è un Cerchio"
		)

	#coerenza funzionale: metodi invocabili
	def testMeth(self):
		self.assertTrue(
			callable(self.c.raggio),
			"c non ha il metodo raggio"
		)
		self.assertTrue(
			callable(self.c.perimetro),
			"c non ha il metodo perimetro"
		)
		self.assertTrue(
			callable(self.c.area),
			"c non ha il metodo area"
		)

	def testraggio(self):
		#robustezza: input non validi
		self.assertRaises(
			TypeError,
			self.c.raggio,
			""
		)
		self.assertRaises(
			ValueError,
			self.c.raggio,
			-1.0
		)
		#coerenza funzionale: risultati attesi dei metodi get/set
		self.c.raggio(2.0)  #setto il raggio prima della prova per avere la certezza del dato corretto
		self.assertEqual(
			self.c.raggio(),
			 2.0,
			 "il raggio di c non è recuperato correttamente"
		)
	#coerenza funzionale: risultati attesi dei metodi
	def testperimetro(self):
		"""va rifatto il calcolo"""
		self.c.raggio(5.0)
		self.assertEqual(
			self.c.perimetro(),
			10.0 * math.pi,
			"Il perimetro di c non è calcolato correttamente"
		)
	#coerenza funzionale: risultati attesi dei metodi
	def testarea(self):
		self.c.raggio(4.0)
		self.assertEqual(
			self.c.area(),
			math.pi * 4.0 * 4.0,
			"L'area di c non è calcolata correttamente"
		)

	def tearDown(self):
		del self.c

if __name__ == '__main__':
	unittest.main()






