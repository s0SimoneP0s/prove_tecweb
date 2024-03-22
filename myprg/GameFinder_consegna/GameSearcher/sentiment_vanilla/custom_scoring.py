from whoosh.scoring import WeightLengthScorer, WeightScorer, BM25FScorer, WeightingModel
from whoosh.compat import iteritems

class BM25Custom(WeightingModel):
    """Classe di scoring personalizzata, aumenta l'espressività del BM25 standard"""
    def __init__(self, B=0.75, K1=1.2, K3=0.5,**kwargs):
        self.B = B
        self.K1 = K1
        self.K3 = K3
        self._field_B = {}
        for k, v in iteritems(kwargs):
            if k.endswith("_B"):
                fieldname = k[:-2]
                self._field_B[fieldname] = v

    def supports_block_quality(self):
        return True

    def scorer(self, searcher, fieldname, text, qf=1):
        if not searcher.schema[fieldname].scorable:
            return WeightScorer.for_(searcher, fieldname, text)
        if fieldname in self._field_B:
            B = self._field_B[fieldname]
        else:
            B = self.B
        return BM25FScorer_custom(searcher, fieldname, text, B, self.K1, self.K3, qf=qf)

class BM25FScorer_custom(WeightLengthScorer):
    def __init__(self, searcher, fieldname, text, B, K1, K3 , qf=1):
        parent = searcher.get_parent()  # returns self if no parent
        self.idf = parent.idf(fieldname, text)
        self.avgfl = parent.avg_field_length(fieldname) or 1
        self.B = B
        self.K1 = K1
        self.K3 = K3
        self.qf = qf
        self.setup(searcher, fieldname, text)

    def __custom_bm25(self, idf, tf, fl, avgfl, B, K1, k3, qf):
        return idf * ((tf * (K1 + 1)) / (tf + K1 * ((1 - B) + B * fl / avgfl))) * (((k3 + 1)*qf)/(k3 + qf))


    def _score(self, weight, length):
        """Lambda Lazy evaluation approach"""
        return self.__custom_bm25(self.idf, weight, length, self.avgfl, self.B, self.K1 , self.K3, self.qf )




   