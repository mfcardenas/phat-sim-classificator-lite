"""
    Class Model for Classification
    UCM
"""
from numpy import array
import os, time, sys
import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import confusion_matrix
from sklearn.externals import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.grid_search import GridSearchCV

class smodel:
    
    def __init__(self, data, target):
        """ Init class model  """
        self.data = data
        self.target = target
        self.jobs = -1
        
    def train_model(self, est, grid):
        """ Train model  """
        gs = GridSearchCV(estimator=est, param_grid=grid, scoring='accuracy', cv=5, n_jobs=self.jobs)
        gs = gs.fit(self.data, self.target)
        return gs
    
    def get_model(self, param):
        """ Get Model """

        if param == "BEST-KNN":
            print("---> Model: Best K-Nearest Neighbor")
            clf = self.train_model(est=KNeighborsClassifier(),
                                   grid={'n_neighbors': [6], 'weights': ['distance']})
            
        return clf