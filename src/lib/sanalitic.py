"""
    Class DataSet structure for data sample
    UCM
"""
import pandas as pd
from scipy.stats import mode
import numpy as np
import os
import warnings

warnings.filterwarnings('ignore')

class dataset:
    """ Creacion del DataSet de datos apartir de los ficheros  """
    
    def __init__(self, foldername, ldata, filters={}):
        """ initializations class dataset  """
        self.data = pd.DataFrame()
        self.file_header_names = ['timestamp', 'accel-x', 'accel-y', 'accel-z']
        self.freq = '40970U'
        self.wsize = '1s'
        self.f_list = ['mean', 'std', 'var', self.rms]
        
        if ldata is not None:
            self.data = ldata
            self.data.index = pd.to_datetime(self.data.index, unit='ms')
        else:
            for activity, number in filters.items():
                samples = self.get_data_file(foldername, activity, number)
                self.data = pd.concat([samples, self.data])
            print( "---> File: ", foldername)
            
    def get_data_file(self, foldername, activity, number):
        """ Obtener muestras de datos directamente del fichero  """
        samples = pd.DataFrame()
        for file in os.listdir(foldername):
            if activity and file.find(activity) == -1:
                continue
            print(file, foldername, activity, number)
            data = pd.read_csv(foldername + "/" + file, sep=";", 
                               names=self.file_header_names, 
                               header=1,
                               index_col=0)
            data = data.assign(target = data['accel-x'] * 0 + number)
            data.index = pd.to_datetime(data.index, unit='ms')
            samples = pd.concat([samples,data])
        return samples
    
    def rms(self, ts): 
        """ Determinate RMS  """
        return np.sqrt(np.mean(ts**2))

    def corr(self, df): 
        """ Determinate correlations for data  """
        cor = df.corr()
        return pd.DataFrame({'xy':[cor['accel-x']['accel-y']], 
                             'xz':[cor['accel-x']['accel-z']], 
                             'yz':[cor['accel-y']['accel-z']]})

    def get_features(self, totrain):
        """ Determinate other features for data  """
        # f_list is a list of features names or methods to apply in resampling
        # features that invlove one dimension only.
        fname = '_' + (self.f_list[0] if isinstance(self.f_list[0], str) else self.f_list[0].__name__)   
        feats = self.data[['accel-x','accel-y','accel-z']].resample(self.wsize, how=self.f_list[0]).add_suffix(fname)

        for i, f in enumerate(self.f_list[1:]):
            fname = '_' + (f if isinstance(f, str) else f.__name__)
            feat = self.data[['accel-x','accel-y','accel-z']].resample(self.wsize, how=f).add_suffix(fname)
            feats = feats.join(feat)   

        # features that involve more than one dimension. 
        mean_mag = (self.data**2).sum(axis=1).resample(self.wsize, how=lambda ts: np.sqrt(ts).mean())
        mean_mag.name = 'mean_mag'
        feats = feats.join(mean_mag)
        
        pairs_cor = self.data.groupby(pd.TimeGrouper(self.wsize)).apply(self.corr).reset_index(1, drop=True)
        feats = feats.join(pairs_cor) 
        
        if totrain == True:
            # drop any nan values
            class_ = self.data['target'].resample(self.wsize, how=lambda ts: mode(ts)[0] if ts.shape[0] > 0 else np.nan)
            mask = np.any(np.isnan(feats), axis=1)
            feats, class_ = feats[~mask], class_[~mask]
            mask = np.isnan(class_)
            feats, class_ = feats[~mask], class_[~mask]
            return (feats, class_)
        else:        
            mask = np.any(np.isnan(feats), axis=1)
            feats = feats[~mask]
            return feats