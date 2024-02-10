import random
import unittest

#Test di alcune funzioni del modulo random: shuffle, choice, sample

# random.shuffle(seq): mischia gli elementi di seq 
# 1)  controllo che l'esecuzione di shuffle non perda elementi della sequenze in ingresso
# 2)  controllo che sollevi una eccezione se riceve in ingresso una sequenza immutabile (es. tupla)

# random.choice(seq): ritorna un elemento random da seq
# 1)  controllo che restituisca un elemento effettivamente appartenente alla sequenza seq

# random.sample(seq,n): ritorna una lista di n elementi unici presi in ordine causuale da seq
# 1)  controllo che restituisca elementi effettivamente appartenenti alla sequenza seq
# 2) controllo che sollevi una eccezione di tipo ValueError se n > numero di elementi unici di seq

class TestSequenceFunctions(unittest.TestCase):

	def setUp(self):
	        self.seq = list(range(10))  #sequenza in ingresso

	def test_shuffle(self):
        	# controllo che non perda argomenti
        	random.shuffle(self.seq)  #mischio gli elementi di seq
        	self.seq.sort() #riordino
        	self.assertEqual(self.seq, list(range(10)))

        	# controllo che sollevi una eccezione se passo una sequenza immutabile
        	self.assertRaises(TypeError, random.shuffle, (1,2,3))

	def test_choice(self):
        	element = random.choice(self.seq)
        	self.assertTrue(element in self.seq)
	
	def test_sample(self):
		for element in random.sample(self.seq, 5):
        		self.assertTrue(element in self.seq)
		self.assertRaises(ValueError, random.sample, self.seq, 20)  	#20 strettamente maggiore 
								    		#del numero di elementi unici in seq

	def tearDown(self):
		del self.seq

if __name__ == '__main__':
    unittest.main()
