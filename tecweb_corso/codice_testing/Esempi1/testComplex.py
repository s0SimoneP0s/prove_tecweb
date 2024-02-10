#!/usr/bin/python

import unittest
from Complex import Complex

class ExceptionTest(unittest.TestCase):
	"""e3sempio test cmpleto"""
	def testObj(self):  #consistenza architetturale
		self.assertTrue(isinstance(self.x, Complex), "x is not an instance of Complex")

	def testInvalidInput(self):  #robustezza a input non validi
		"""Lista input"""
		posinput = ["2.0",3]
		self.assertRaises(TypeError, Complex, *posinput)
		"""Dizionario input"""
		kwinput = {"realpart" : 2.0, "imagpart" : "3"}
		self.assertRaises(TypeError, Complex, **kwinput)

	def testMethods(self):  #coerenza funzionale: metodi invocabili e corretti 
		"""verifica call"""
		self.assertTrue(callable(self.x.getreal), "Metodo getreal() not callable")  #verifico che il metodo getreal() esista e sia callable
		self.assertTrue(callable(self.x.getimg), "Metodo getimg() not callable")  #verifico che il metodo getimg() esista e sia callable
		self.assertEqual(2.0,self.x.getreal(),'Method getreal() not working')
		self.assertEqual(3,self.x.getimg(), 'Method getimg() not working')
	
	def setUp(self):
	"""crea una istanza della classe usando la built in setUp poi cancella con tearDown"""
	        self.x = Complex(2.0,3)

	def tearDown(self):
		del self.x

	
if __name__ == '__main__':
	unittest.main()
