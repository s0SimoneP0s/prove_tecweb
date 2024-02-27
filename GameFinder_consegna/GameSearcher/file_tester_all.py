import unittest
import os

from vanilla.windex import FileManager as vanillaFM
from sentiment_vanilla.windex import FileManager as sentimentFM

class TestFileManager(unittest.TestCase):
    """
    Non esiste in python una variabile che tenga traccia di quale pacchetto 
    provenga un oggetto di una classe instanzioata quindi lo devo dire io
    """
    pkg1="vanilla"
    def test_static_path_v(self):
        file_manager = vanillaFM(package_name=self.pkg1,condition="b") # Verifica che il percorso statico sia corretto per la condizione "b"
        expected_static_path = "csv/benchmark.csv"
        self.assertEqual(file_manager.static_path, expected_static_path)

    def test_dinamic_path_v(self):
        file_manager = vanillaFM(package_name=self.pkg1,condition="b") # Verifica che il percorso dinamico sia corretto per la condizione "b"
        current_directory = os.getcwd()
        expected_dinamic_path = os.path.join(current_directory, self.pkg1, "II_b")
        self.assertEqual(file_manager.dinamic_path,  expected_dinamic_path)


    def test_invalid_condition_v(self):
        with self.assertRaises(ValueError): # Verifica che la classe sollevi un'eccezione per una condizione non valida
            vanillaFM(package_name=self.pkg1, condition="invalid_condition")


    pkg1="sentiment_vanilla"
    def test_static_path_s(self):
        file_manager = sentimentFM(package_name=self.pkg1,condition="b") # Verifica che il percorso statico sia corretto per la condizione "b"
        expected_static_path = "csv/benchmark.csv"
        self.assertEqual(file_manager.static_path, expected_static_path)

    def test_dinamic_path_s(self):
        file_manager = sentimentFM(package_name=self.pkg1,condition="b") # Verifica che il percorso dinamico sia corretto per la condizione "b"
        current_directory = os.getcwd()
        expected_dinamic_path = os.path.join(current_directory, self.pkg1, "II_b")
        self.assertEqual(file_manager.dinamic_path,  expected_dinamic_path)


    def test_invalid_condition_s(self):
        with self.assertRaises(ValueError): # Verifica che la classe sollevi un'eccezione per una condizione non valida
            sentimentFM(package_name=self.pkg1, condition="invalid_condition")

if __name__ == '__main__':
    unittest.main()
