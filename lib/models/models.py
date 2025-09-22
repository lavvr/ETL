# #базовый класс от sklearn с рандомом
from sklearn.base import BaseEstimator
# import numpy - eще подумаю над ним

# class ClassificationMaster(BaseEstimator):
#     def __init__(self):
#         super().__init__()
    
#     def fit(self, X, y):
#         pass

#     def predict(self, X):
#         pass
# from typing import Optional
# import logging

# import torch
# from transformers import AutoTokenizer, AutoModelForSequenceClassification


# class BERTClassifier():
#     def __init__(self, model_name: str, num_labels: int = 2):
#         pass

#     def predict():
#         pass

#     def save_model():
#         pass

from __future__ import annotations
from typing import Optional
import logging

import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


