# my_package/__init__.py
import sys
import os

# Aggiungi il percorso assoluto della directory corrente al percorso di ricerca dei moduli
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
