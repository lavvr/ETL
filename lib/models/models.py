# #базовый класс от sklearn с рандомом
# from sklearn.base import BaseEstimator
# # import numpy - eще подумаю над ним

# class ClassificationMaster(BaseEstimator):
#     def __init__(self):
#         super().__init__()
    
#     def fit(self, X, y):
#         pass

#     def predict(self, X):
#         pass
from typing import List, Optional
import logging

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


class BERTClassifier():
    def __init__(self, model_name: str, num_labels: int = 2):
        pass
    
    def fit():
        pass

    def predict():
        pass

    def save_model():
        pass
    