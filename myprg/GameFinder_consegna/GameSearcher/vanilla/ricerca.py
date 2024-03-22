#!/usr/bin/env python

from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from windex import SchemaManager
import custom_scoring
from nltk.corpus import wordnet

class Search(SchemaManager):
  """
      Classe per la ricerca
  """
  def __init__(self , package="vanilla" , condition="b" ,advanced=False ,  limit=100 ):
      super().__init__(  package , condition )
      self.advanced=advanced
      self.limit=limit
      self.scorer = custom_scoring.BM25Custom(B=0.35, K1=1.35, delta=0.6 , K3=1.3)


  def _reset_tag_counter(*args):
    """Metodo dinamico per il benchmark"""
    pass
  
  def _set_tag_counter1(*args):
    """Metodo dinamico per il benchmark"""
    pass
  
  def _set_tag_counter2(*args):
    """Metodo dinamico per il benchmark"""
    pass

  def _set_tag_DCG(*args):
    """Metodo dinamico per il benchmark"""
    pass

  def stampa_bench(*args):
    """Metodo dinamico per il benchmark"""
    pass

  def stampa_dati(self , I):
    for k, V in I.items():
      print("\n\n" +  k   + " <------------------ titolo"  )
      for v in V:
        print("\nreview ------------------ >  " +  v )

  def _title_sorting(self, results):
      """Ordina per rilevanza media i titoli dei giochi, per ogni review associata, 
      non per ordine di rilevanza delle review e basta
      """
      self._reset_tag_counter()  # azzera il contatore ogni query e lo inizializza
      r=[]
      for i in results:
          self._set_tag_counter1(i) # conta le query con il contatore
          r.append(i) # aggiunge alla lista di ritorno cose
      grouped_results = {} # dizionario
      l=len(r)
      l_score= [r.score for r in r[:]]
      i=0
      grouped_results = {}
      tuple_app_DCG=set() # unico
      for result in results:
          title = result['title']
          review = result['review']
          self.stampa_bench(title,review)
          score = l_score[i]
          i=i+1
          unique_reviews = grouped_results.get(title, set())
          unique_reviews.add((review, score))
          grouped_results[title] = unique_reviews
          tags=result['tag']
          tuple_app_DCG.add( (score, tuple(tags) )  )
      if self.condition=="g":
          self._set_tag_DCG(tuple_app_DCG) # va al benchmark e prende una tupla con score e tags
      grouped_results2 = {} # calcolare la media delle recensioni per ogni titolo
      l= len(grouped_results) # l --> contatore per le review uniche
      sum_avfg=0              #  valore per la somma di tutte le review
      for title, reviews in grouped_results.items():
          total_score = sum(score for _, score in reviews)
          avg_score = total_score / len(reviews) if len(reviews) > 0 else 0
          sum_avfg =  sum_avfg + avg_score 
          grouped_results2[title] = avg_score
      sorted_items = sorted(grouped_results2.items(), key=lambda x: x[1], reverse=True) # ordina i risultati in base alla media delle recensioni
      avg_map = sum_avfg / l if l > 0 else 0  # media tra tutti i documenti unici con una verifica per evitare la divisione per zero
      grouped_results3 = {} # nuovo dizionario con i risultati ordinati
      for title, avg_score in sorted_items:
        if len(grouped_results[title]) > 0 and avg_score >= avg_map: # solo i titoli con recensioni e con uno score maggiore o uguale alla media
            if super().condition == "b" or super().condition == "g" :
              grouped_results3[title] = [review for review, score in grouped_results[title] ] # per il benchmark li conta tutti
            else:
              grouped_results3[title] = [review for review, score in grouped_results[title] if score >= avg_map]
      for i in results:
          self._set_tag_counter2(i) # conta le query post media, le teniamo anche per il benchmark
      return grouped_results3
  
  def wu_palmer_similarity(self, word1, word2):
    synset1 = wordnet.synsets(word1)
    synset2 = wordnet.synsets(word2)
    if synset1 and synset2:
        synset1 = synset1[0]
        synset2 = synset2[0]
        return synset1.wup_similarity(synset2) or 0.0
    return float(0.0)

  def __get_synonyms(self, word, num_synonyms=2):
      """Non modificare i sinomimi num_synonyms, o comunque massimo 2"""
      synonyms = set()
      for syn in wordnet.synsets(word):
          for lemma in syn.lemmas():
              synonym = lemma.name()
              if synonym != word:
                  synonyms.add(synonym)
      return sorted(set(synonyms), key=lambda x: self.wu_palmer_similarity(word, x) or 0, reverse=True)[:num_synonyms]
  
  def synonymous_expansion(self,query_str):
    query_str = super()._preprocessing(query_str)
    synonyms = self.__get_synonyms(query_str)
    if len(synonyms) == 2:
      app=synonyms[0]
      ap1=synonyms[1]
      query_str = f'({query_str}) OR ({app}) OR ({ap1})'
    elif len(synonyms) == 1:
      ap1=synonyms[0]
      query_str = f'({query_str}) OR ({app}) )'
    else:
       query_str = query_str
    return QueryParser("pre", self.ix.schema).parse(query_str)

  def __search_backend(self, query_str ):
    """backend ricerca e ritorna risultati"""
    with self.ix.searcher(weighting=self.scorer) as searcher: # weighting=self.scorer
      # nostri algoritmi personalizzati
      if self.advanced : # pre= BM25 nostro, whoosh standard cerca su review
        query = QueryParser("review", self.ix.schema).parse(query_str ) # supporta wildcard e booleane e proximity
      else:
        query = self.synonymous_expansion(query_str) # senza syn exapnsion whoosh
      results = searcher.search(query, limit=self.limit)
      grouped_results=self._title_sorting(results)
    return grouped_results 

  def search(self, query_str , advanced=None  ):
    """Proxy ricerca di interfaccia per tutte le User interface"""
    if advanced != None:
      self.advanced = advanced
    self.ix = open_dir(  str( super().dinamic_path ) , readonly=True)
    return self.__search_backend(query_str)

  def input_searcher(self):
    """Chiede a rullo query fino a Ctrl+D da parte dell'utente o Ctrl+Z se su windows"""
    quit = "Ctrl+Z,Enter" if sys.platform.startswith("win") else "Ctrl+D"
    prompt = "Inserici una query:  ({} per uscire ): ".format(quit) 
    while True:
      try:
        query = input(prompt)
        fquery = str(query)
        if fquery:
          print("------------------------below query < " + fquery + " > retrieved information--------------------")
          I = self.search(fquery) 
          self.stampa_dati(I)
      except EOFError:
        print("Fine shell query")
        break

if __name__ == "__main__":
  """Per provare la classe"""
  s=Search(condition="d")
  s.input_searcher()