#!/usr/bin/python

import unittest

class TestProva(unittest.TestCase):

	def testEqual(self):
		self.assertEqual(1, 3-2)


	def testNotEqual(self):
		self.assertNotEqual(2, 3-2)

	def testAssertTrue(self):
		self.assertTrue(4 > 5-10)

	def testAlmostEqual(self):
		self.assertAlmostEqual(1.12, 3.38-2.22, places=1)  #1.12,1.16
		self.assertAlmostEqual(1.12, 3.38-2.22, delta=0.1)  #1.12,1.16

	def testRegex(self):
		self.assertRegex("text", "ex")

	def testAssertRaises1(self):
		self.assertRaises(TypeError, range, "stringa") #range("str") solleva eccezione TypeError

	def testAssertRaises2(self):
		self.assertRaises(TypeError, range, 10) 

	def testAssertRaises3(self):
		self.assertRaises(ValueError, range, "stringa")


if __name__ == '__main__':    
	unittest.main()       #che risultati abbiamo?
