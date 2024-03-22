import nltk
from whoosh.fields import TEXT , Schema , NUMERIC , analysis
from nltk.corpus import stopwords 
from nltk.stem import WordNetLemmatizer, PorterStemmer
import os, time

def time_function(function):
    """Decoratore per la stampa del tempo di esecuzione di una funzione."""
    def new_function(*args, **kwargs):
        start = time.time()
        value = function(*args, **kwargs)
        end = time.time()
        print("Execution time: " + str(end - start))
        return value
    return new_function

class FileManager:
    """Classe che si occupa di restituire le path dei file corrette per tutto il progetto"""

    def __init__(self, package_name , condition):
        self.__condition=condition
        current_path = os.getcwd()
        current_dir = os.path.split(current_path)[-1]

        # capisce se chimato da dentro il package
        if current_dir == "GameSearcher":  # attenzione se la cartella superiore NON si chiama GameSearcher, chiamata da fuori
           prev= ''
           current_path=os.path.join(current_path, package_name)
        else: # chiamata da dentro
           prev= '..'
           current_path=os.path.join(current_path)


        if condition == "b" : # dataset benchmark
          static = os.path.join(prev , "csv" , "benchmark.csv") # "../csv/benchmark.csv", da GameSearcher solo "csv/benchmark.csv"
          dinamic = os.path.join(current_path, "II_b") # da GameSearcher "pacchetto/II_path"
        elif condition == "d" : # dataset produzione
          static = os.path.join(prev , "csv" , "prod.csv")
          dinamic = os.path.join(current_path, "II_d")
        elif condition == "g" : # dataset gold truth
          static = os.path.join(prev , "csv" , "gold_truth.csv")
          dinamic = os.path.join(current_path, "II_g")
        else:
          raise ValueError("Opzione non valida. Scegliere tra: condition = {}".format(["b","d","g"]))
        self.__static=static
        self.__dinamic=dinamic
        self.__make_path()

    def __make_path(self):
       if not os.path.exists(self.__dinamic):
            os.makedirs(self.__dinamic)

    """Vari getter"""
    @property
    def static_path(self):
        return self.__static

    @property
    def dinamic_path(self):
        return self.__dinamic

    @property
    def condition(self):
        return self.__condition


class SchemaManager(FileManager):
  """Classe per ora univoca che ha le funzionalità di base per l'interfaccia a whoosh e 
      tutte le altre librerie usate dal progetto"""
  schema = Schema (  
      title=TEXT (stored=True), # titolo 
      review=TEXT (stored=True,analyzer=analysis.StemmingAnalyzer() ), # review
      tag=TEXT(stored=True), # campo tag per il benchmark
      rank=NUMERIC(sortable=True , stored=True ), # contiene un valore di ordinamento per i risultati ritornati
      pre=TEXT(stored=True) # contiene i valori preprocessati per facilitare la ricerca
    )

  def __init__(self  , package,  condition ):
      """
          project_path è il nome del test che si sta effettunado, vanilla ha poche modifiche quindi è lo standard
          benchmark fa selezionare quali dati verranno usati per risolvere le query e creare l'index
          gold impone di creare indice per la gold truth di riferimento
      """
      super().__init__( package, condition )


  def _preprocessing(self,stringa):
      """Funzione che ritorna le stringhe preprocessate"""
      stringa_token = nltk.word_tokenize(stringa)
      stringa_token = [ word.lower() for word in stringa_token if word.isalpha()]
      stringa_token = [word for word in stringa_token if word not in stopwords.words("english")] 
      stemmer = PorterStemmer()
      stringa_token = [stemmer.stem(word) for word in stringa_token]
      lemmatizer = WordNetLemmatizer()
      stringa_token = [lemmatizer.lemmatize(word) for word in stringa_token]
      stringa_token = " ".join(stringa_token)
      return stringa_token
