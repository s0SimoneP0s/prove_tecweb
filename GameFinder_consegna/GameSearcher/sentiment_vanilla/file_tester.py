import unittest
import os
from windex import FileManager

class TestFileManager(unittest.TestCase):
    def test_static_path(self):
        file_manager = FileManager(package_name="sentiment_vanilla",condition="g") # verifica che il percorso statico sia corretto per la condizione "b"
        expected_static_path = "../csv/gold_truth.csv"
        self.assertEqual(file_manager.static_path, expected_static_path)

    def test_dinamic_path(self):
        file_manager = FileManager(package_name="sentiment_vanilla",condition="g") # verifica che il percorso dinamico sia corretto per la condizione "b"
        current_directory = os.getcwd()
        expected_dinamic_path = os.path.join(current_directory, "II_g")
        self.assertEqual(file_manager.dinamic_path, expected_dinamic_path)

    def test_invalid_condition(self):
        with self.assertRaises(ValueError): # verifica che la classe sollevi un'eccezione per una condizione non valida
            FileManager(package_name="sentiment_vanilla",condition="invalid_condition")

if __name__ == '__main__':
    unittest.main()
