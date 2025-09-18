#базовый класс от sklearn с рандомом
from sklearn.base import BaseEstimator
# import numpy - eще подумаю над ним

class ClassificationMaster(BaseEstimator):
    def __init__(self):
        super().__init__()
    
    def fit(self, X, y):
        pass

    def predict(self, X):
        pass
    