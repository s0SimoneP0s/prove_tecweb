import unittest
import os
from windex import FileManager

class TestFileManager(unittest.TestCase):
    def test_static_path(self):
        file_manager = FileManager(package_name="sentiment_vanilla",condition="b") 
        expected_static_path = "../csv/benchmark.csv"
        self.assertEqual(file_manager.static_path, expected_static_path)

    def test_dinamic_path(self):
        file_manager = FileManager(package_name="sentiment_vanilla",condition="b") # verifica che il percorso dinamico sia corretto per la condizione "b"
        current_directory = os.getcwd()
        expected_dinamic_path = os.path.join(current_directory, "II_b")
        self.assertEqual(file_manager.dinamic_path, expected_dinamic_path)


    def test_static_path_g(self):
        file_manager = FileManager(package_name="sentiment_vanilla",condition="g") 
        expected_static_path = "../csv/benchmark.csv"
        self.assertEqual(file_manager.static_path, expected_static_path)

    def test_dinamic_path_g(self):
        file_manager = FileManager(package_name="sentiment_vanilla",condition="g") 
        current_directory = os.getcwd()
        expected_dinamic_path = os.path.join(current_directory, "II_b")
        self.assertEqual(file_manager.dinamic_path, expected_dinamic_path)


    def test_invalid_condition(self):
        with self.assertRaises(ValueError): 
            FileManager(package_name="sentiment_vanilla",condition="invalid_condition")

if __name__ == '__main__':
    unittest.main()
