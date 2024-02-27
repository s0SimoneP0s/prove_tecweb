#!/usr/bin/env python

import csv, os
from whoosh.filedb.filestore import FileStorage
from windex import SchemaManager
from concurrent.futures import ThreadPoolExecutor
from nltk.sentiment import SentimentIntensityAnalyzer

class IndexBuilder(SchemaManager):
  """Classe per l'indicizzazione , eredita da windex BaseP la struttura dello schema e delle path"""
  def __init__(self ,condition="b" , max_threads = 2 ):
    # si chiama solo tramite shell
    current_path = os.getcwd()
    package = os.path.split(current_path)[-1]

    super().__init__( package ,condition )
    self.st = FileStorage(    str (  super().dinamic_path  )  )
    self.ix = self.st.create_index(super().schema)
    self.__build_index(max_threads)

  def __rank_sentiment(self, testo):
    sia = SentimentIntensityAnalyzer()
    scores = sia.polarity_scores(testo)
    joyrate= scores['pos']/(scores['pos']+scores['neg'] + 0.001)
    return joyrate

  def __build_index(self , max_threads):
    """scrive le righe dal CSV direttamente nell'indice"""
    with open( super().static_path , 'r', encoding='utf-8') as f: 
      self.w = self.ix.writer() # crea il writer dell'indice di woosh
      self.reader = csv.reader(f)
      next(self.reader) # skippa indice iniziale (titoli)
      # aggiunto perchè altrimenti il multithread non va
      self.condizione=super().condition
      self.pre_fun=super()._preprocessing
      if max_threads > 1 :
        def scrivi (riga ):
          if self.condition == "g": # se si prova il gold standard(formato diverso)
            ta=[]
            ta=riga[3:]
          else: # se non stiamo lavorando con il gold standard
            ta=riga[2]
          self.w.add_document(title=riga[0], review=riga[1] , tag=ta , rank=self.__rank_sentiment(riga[1]) , pre=self.pre_fun(str(riga[1])) )
        with ThreadPoolExecutor(max_threads) as executor:
          executor.map(scrivi, self.reader)
        self.w.commit()
      else:
        for riga in self.reader:
          if self.condition == "g": 
            ta=[]
            ta=riga[3:]
          else: 
            ta=riga[2]
          self.w.add_document(title=riga[0], review=riga[1] , tag=ta , rank=self.__rank_sentiment(riga[1]) , pre=self.pre_fun(str(riga[1])) )
        self.w.commit()

if __name__ == "__main__":
  """Per provare la classe""" 
  rt=IndexBuilder(condition="d") # search per buildare o no l'index