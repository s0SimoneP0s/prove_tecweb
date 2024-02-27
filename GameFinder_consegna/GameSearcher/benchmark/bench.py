# Benchmark
from typing import Final
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import math

class Mark:
    query_set: Final[list] = [            # avanzato? ⬇ vero/falso | R non usate
        ("good AND (soundtrack OR music)",           True ),    # Q:0 --> R=20 
        ("horror",                                   False ),    # Q:1 --> R=20 
        ("play AND (again OR replay)",               True ),    # Q:2 --> R=20 
        (""" "best free"~4 """ ,                     True ),    # Q:3 --> R=20 
        ("fun for child and family",                 False  ),    # Q:4 --> R=20 
        ("multiplayer OR co op",                     True ),    # Q:5 --> R=20 
        ("bug* ",                                    True ),    # Q:6 --> R=20
        ("hard OR challenge OR challenging",         True ),    # Q:7 --> R=20
        ("shoot people",                             False ),    # Q:8 --> R=20
        ("(more OR different) AND (ending OR end)",  True )     # Q:9 --> R=20
    ]
    
    """Dati ricavati manualmente valutando le review ritornate"""
    Algoritmo_BM25Pre_senza_ottimizzazione_media : Final[list]= [
        [0,	1,	1,	1,	1,	1,	0,	1,	1,	1], 
        [1,	1,	1,	0,	1,	1,	1,	1,	1,	0],
        [0,	0,	0,	1,	0,	0,	0,	1,	0,	1],
        [1,	1,	1,	1,	1,	0,	1,	0,	0,	1],
        [0,	1,	0,	0,	0,	0,	0,	0,	0,	0],
        [1,	1,	1,	0,	1,	1,	1,	1,	1,	1],
        [1,	0,	0,	0,	0,	1,	1,	1,	0,	0],
        [0,	0,	1,	1,	1,	0,	1,	1,	1,	0],
        [1,	1,	1,	1,	0,	1,	0,	1,	1,	1],
        [1,	0,	0,	0,	0,	0,	0,	1,	1,	0],
    ]  

    Algoritmo_BM25Pre_MOD_senza_media : Final[list]=[
        [1,	1,	1,	1,	1,	1,	1,	1,	1,	1],
        [1,	1,	1,	0,	0,	1,	1,	1,	1,	1],
        [0,	1,	0,	1,	1,	0,	0,	0,	0,	1],
        [1,	1,	1,	1,	1,	0,	0,	1,	0,	1],
        [1,	0,	0,	0,	0,	0,	0,	0,	0,	0],
        [1,	1,	1,	1,	1,	1,	1,	1,	1,	1],
        [1,	0,	0,	0,	0,	1,	0,	0,	0,	0],
        [0,	1,	1,	1,	0,	0,	0,	1,	1,	1],
        [1,	1,	0,	0,	0,	0,	0,	0,	0,	0],
        [1,	1,	1,	1,	1,	0,	0,	0,	0,	0],
    ]

    Algoritmo_whoosh_standard : Final[list] = [
        [1,	1,	1,	1,	1,	1,	0,	1,	1,	1],
        [1,	1,	0,	0,	1,	1,	1,	1,	1,	1],
        [0,	1,	0,	1,	1,	0,	1,	0,	1,	0],
        [1,	1,	1,	1,	0,	1,	0,	1,	0,	0],
        [1,	0,	0,	0,	0,	0,	0,	0,	0,	0],
        [1,	1,	1,	1,	1,	1,	0,	1,	1,	0],
        [1,	0,	0,	0,	0,	1,	0,	0,	0,	0],
        [1,	1,	1,	1,	0,	1,	0,	0,	1,	1],
        [1,	1,	0,	0,	0,	0,	0,	0,	0,	0], 
        [1,	0,	1,	1,	1,	0,	0,	0,	0,	0], 
    ]
    R : Final[list] = [40,40,40,40,30,20,40,30,30,40] #vettore dei documenti rilevanti per ogni query

    Algoritmi: Final[list] =[
            Algoritmo_whoosh_standard,
            Algoritmo_BM25Pre_senza_ottimizzazione_media,
            Algoritmo_BM25Pre_MOD_senza_media,
        ]

    def __init__(self, rt , cond="g" , pm=False ):
        """
        :post_media Quando True conta post media(set_counter2), altrimenti False (set_counter1), non implementato
        """
        self.count=self.reset_tag_counter()
        self.DCG=[]
        self.condition=cond
        self.target_obj=rt
        self.post_media=pm
        self.crea_bench()

    def reset_tag_counter(self):
        """azzera il contatore di query per ogni query run e lo inizializza"""
        self.count={ "R": 0 ,"0": 0,"1": 0,"2": 0,"3": 0, "4": 0, "5": 0, "6": 0 ,"7": 0,"8": 0,"9": 0 }

    
    def _set_tag_counter(self , i):
        """ conta i campi TAG se stiamo facendo il benchmark """
        self.count[str(i["tag"])] = self.count[str(i["tag"])] +1 

    def get_tag_counter(self):
        """ritorna i campi"""
        return self.count if self.count else self.reset_tag_counter()

    def get_DCG_counter(self):
        """ritorna i DCG per query"""
        return self.DCG 

    def stampa_dati(self , diz):
        for k, V in diz.items():
            print("\n\n" + str( k)   + " <------------------ titolo"  )
            for v in V:
                print("\nreview ------------------ >  " +  v )
    
    def stampa_bench(self,title, review):
            print("\n\n" +  title   + " <------------------ titolo"  ) 
            print("review ------------------ >  " +  review )

    def _set_tag_DCG(self, tuple_app_DCG): # va al benchmark e prende una tupla con score e tags
        """Prende le tuple e raccoglie in una lista tutte le DCG delle query"""
        dataset=list (tuple_app_DCG)
        sorted_dataset = sorted(dataset, key=lambda x: x[0], reverse=True)
        top_elements = sorted_dataset[:10]
        query_dcg=[]
        for i in top_elements:
            query_dcg.append(i[1][len(self.DCG)]) # vettore DCG
        self.DCG.append ( float(query_dcg[0]) + sum([ (  float(query_dcg[i]) / math.log(i + 1, 2)) for i in range(1, len(query_dcg))]) )

    def set_tag_benchmark(self ) :
        pass

    def dummy_print(self, *args, **kargs):
        pass

    def crea_bench(self):
        """Modifica dinamicamente i metodi e le proprietà dell'oggetto 
        di cui effettuare il benchmark"""
        self.target_obj.count=self.count
        self.target_obj.DCG=self.DCG
        self.target_obj._reset_tag_counter = self.reset_tag_counter
        # abbiamo 2 counter
        if not self.post_media: # stampa per capire i ranking
            if self.condition=="g": # conta i dcg se interroghiamo la gold truth
                self.target_obj._set_tag_DCG=self._set_tag_DCG
            else:
                # _set_tag_counter1 conta tutti anche quelli sotto media
                self.target_obj._set_tag_counter1 = self._set_tag_counter
            self.target_obj.stampa_bench=self.stampa_bench
            self.target_obj.stampa_dati=self.dummy_print
        else:
            # _set_tag_counter2 solo quelli sopra media
            self.target_obj._set_tag_counter2 = self._set_tag_counter
        self.target_obj.get_tag_counter = self.get_tag_counter
        self.target_obj.get_DCG_counter = self.get_DCG_counter

    def chiamata_hitmap(self, stampa=False):
        """Crea il grafico delle heatmap"""
        if not stampa: # vero --> stampa le review, falso altrimenti
            self.target_obj.stampa_bench=self.dummy_print
        benchmark=[]
        for i in self.query_set:
            _ = self.target_obj.search(i[0], advanced=i[1])
            if stampa:
                self.target_obj.get_tag_counter   = self.get_tag_counter
            benchmark.append(self.get_tag_counter())
        y_labels = [f'Q:{i}' for i in range(len(benchmark))] # crea una lista di etichette per gli assi
        x_labels = list(benchmark[0].keys())
        df = pd.DataFrame(benchmark, columns=x_labels)
        sns.heatmap(df, annot=True, fmt='g', cmap='coolwarm', xticklabels=x_labels, yticklabels=y_labels)
        plt.xlabel('Tag booleani riferimento')
        plt.ylabel('Dizionari')
        titolo="Heatmap Vanilla - limit " +  str(self.target_obj.limit) 
        plt.title(titolo)
        plt.show()

    def precision(self, A=10 ):
        """Calcola precision"""
        Ra=self.Algoritmo_whoosh_standard
        prec=[]
        i=0
        for _ in Ra:
            prec.append( sum( Ra[i] )  / A )
            i=i+1
        return prec
    
    def recall(self ):
        """Calcola recall"""
        Ra=self.Algoritmo_whoosh_standard
        R=self.R
        rec=[]
        i=0
        for _ in Ra:
            rec.append( sum( Ra[i] )  / R[i] )
            i=i+1
        return rec

    def avg_precision(self , riga): # riga di una query
        """Calcola avg_precision di una query"""
        prec=[]
        i=1 # indice posizionale da 1 a 10
        for j in riga:
            if j==1: # la j vale o 1 0 zero
                prec.append(  sum(riga[0:i])/i  ) # precision at seen
            i=i+1
        return sum(prec)/len(prec) if len(prec) != 0  else 0 # avg precision di ogni query

    def avg_map(self, vett_avg_pre):
        """Calcola la MAP con input vettore di avg_precision"""
        return sum(vett_avg_pre)/len(vett_avg_pre)  if len(vett_avg_pre) != 0  else 0
    
    def all_avg_prec(self, matrix):
        """Scorre matrice dati"""
        l=[]
        for j in matrix:
            l.append(self.avg_precision(j))
        return l, self.avg_map(l)


    def chiamata_barre(self):
        """Stampa grafico barre di precison"""
        recall = self.recall()
        precision = self.precision()
        num_classi = len(recall) 
        posizioni = range(num_classi)
        larghezza_barre = 0.35
        fig, ax = plt.subplots() 
        bar1 = ax.bar(posizioni, recall, larghezza_barre, label='Recall')
        bar2 = ax.bar([p + larghezza_barre for p in posizioni], precision, larghezza_barre, label='Precision')
        ax.set_xlabel('Query')
        ax.set_ylabel('Valori Precision e Recall')
        ax.set_title('Precision e Recall')
        ax.set_xticks([p + larghezza_barre / 2 for p in posizioni])
        ax.set_xticklabels(['Q0', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9']) 
        ax.legend() 
        plt.show() 


    def plotta_avg_and_map(self, matrice="whatislovebabydonthurtme"):
        """Stampa la map dei 3 algoritmi testati e li da in pasto alle funzioni di plot"""
        prec_vect = []
        map_vect = []
        if matrice != "whatislovebabydonthurtme":
            for i in matrice:
                app, _ = self.all_avg_prec(i)
                prec_vect.append(app)
        else:
            for i in self.Algoritmi:
                app, ap = self.all_avg_prec(i)
                map_vect.append(ap)
                prec_vect.append(app)
        self.plotta_avg(prec_vect)
        self.plotta_map(map_vect)
        
    def plotta_avg(self, prec_vect):
        """Grafico per i valori di average precision"""
        num_classi = len(prec_vect[0])
        posizioni = range(num_classi)  
        larghezza_barre = 0.22 
        gap = 0.00  
        fig, ax = plt.subplots()  
        bar1 = ax.bar([p - larghezza_barre - gap for p in posizioni], prec_vect[0], larghezza_barre, label='Whoosh')
        bar2 = ax.bar(posizioni, prec_vect[1], larghezza_barre, label='BM25 Whoosh modificato')
        bar3 = ax.bar([p + larghezza_barre + gap for p in posizioni], prec_vect[2], larghezza_barre, label='BM25 Whoosh modificato param modificati')
        ax.set_xlabel('Query')  
        ax.set_ylabel('Values of Average Precision')
        ax.set_title('Average Precision for the algorithms')
        ax.set_xticks([p for p in posizioni])
        ax.set_xticklabels(['Q0', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9'])
        ax.legend()  
        plt.show()  

    def plotta_map(self, vettore):
        """Grafico per i valori di MAP"""
        algorithms = ['Whoosh', 'BM25 Whoosh mod', 'BM25 Whoosh mod param mod']
        plt.bar(algorithms, [ vettore[0], vettore[1], vettore[2] ], color=['blue', 'green', 'red'])
        plt.xlabel('Algoritmi')
        plt.ylabel('Mean Average Precision (MAP)')
        plt.title('Valori della MAP per gli algoritmi')
        plt.show()


    def plot_DCG(self, vettore):
        """Grafico per i valori di DCG"""
        num_classi = len(vettore[0])
        posizioni = range(num_classi)
        larghezza_barre = 0.29
        fig, ax = plt.subplots()
        bar1 = ax.bar([p - larghezza_barre/2 for p in posizioni], vettore[0], larghezza_barre, label='Sentiment')
        bar2 = ax.bar([p + larghezza_barre/2 for p in posizioni], vettore[1], larghezza_barre, label='BM25')
        bar3 = ax.bar([p + 3 * larghezza_barre/2 for p in posizioni], vettore[2], larghezza_barre, label='Whoosh')
        ax.set_xlabel('Query')
        ax.set_ylabel('Valori della DCG')
        ax.set_title('DCG Values for Each Query')
        ax.set_xticks(posizioni)
        ax.set_xticklabels([f"Q{i}" for i in range(num_classi)])
        ax.legend()
        plt.show()

    def plot_armonica( self, vettore):
        """Grafico finale per comparare 3 algoritmi"""
        norm_avg_dcg=[]
        for i in vettore:
            norm_vect=[]
            numer=len (i)
            for j in i:
                norm_vect.append ( 1 / (j + 0.001)  )
            norm_avg_dcg.append ( numer / sum(norm_vect))
        algorithms = ['Sentiment', 'BM25', 'Whoosh']
        plt.bar(algorithms, [ norm_avg_dcg[0], norm_avg_dcg[1], norm_avg_dcg[2] ], color=['blue', 'green', 'red'])
        plt.xlabel('Algoritmi')
        plt.ylabel('Media Armonica')
        plt.title('Media armonica DCG')
        plt.show()