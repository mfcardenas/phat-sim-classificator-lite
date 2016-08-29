"""
    Class File structure and divide data for samples and frecuence.
    UCM
"""
from numpy import fft
from numpy import array
from sklearn.decomposition import PCA
import os

class sfile:
    def __init__(self, filename, buffer_):
        """ Init sfile read  """
        self.pca = False
        self.data = []
        self.accelerations = []
        self.timestamps = []
        self.feature = []
        raw_data = []
        decrement = 0
        
        if buffer_ == None:
            decrement = 1
            self.filename = filename
            self.timestamps = []
            raw_data = []
            with open(filename) as file:
                print(filename)
                lines = [line for line in file]
                for line in lines[2:]:
                    parts = [float(measurement.strip()) for measurement in line.split(';')]
                    self.timestamps.append(parts[0])
                    raw_data.append(parts[1:])
        else:
            for line in buffer_:
                self.timestamps.append(line[0])
                raw_data.append(line[1:])
        
        for i in range(len(raw_data) - decrement):
            current = raw_data[i]
            acceleration = current
            self.data.append([acceleration[0], acceleration[1], acceleration[2]])
            self.accelerations.append(acceleration)

    def get_frequencies(self):
        """ Get array frecuence of data or sample  """
        num_seconds = float(self.timestamps[-2] - self.timestamps[0]) / float(1000)
        samples_per_second = len(self.data) / num_seconds
        num_samples = len(self.data)
        oscilations_per_sample = [float(oscilations) / num_samples for oscilations in range(0, num_samples)]
        return [ops * samples_per_second for ops in oscilations_per_sample]
    
    def get_buckets(self, first, last, num_buckets, hertz_cutoff=float(5)):
        """ Get Bucket of Data  """
        # Pensar en la posibilidad de no aplicar PCA, permitir utilizar fft sobre una feature diferente, por ejemplo raiz-cuadrada(x2 + y2 + z2)
        if self.pca == True:
            pca = PCA(n_components=1, copy=True, whiten=True)
            numpy_data = array(self.data)
            transformed_dataset = PCA.fit_transform(pca, numpy_data)
            slice=transformed_dataset[first:last]
        else:
            slice = self.data[first:last]
            slice = [column[0] for column in slice]
            
        transformed = fft.fft(slice)
        absolute = [abs(complex) for complex in transformed]

        frequencies = self.get_frequencies()

        buckets = [0 for i in range(num_buckets)]
        width = hertz_cutoff / num_buckets
        sum_of_buckets = 0.0000001
        for i in range(1, len(absolute)):
            index = int(frequencies[i] / width)
            if index >= num_buckets:
                break
            buckets[index] += absolute[i]
            sum_of_buckets += absolute[i]

        #if args.normalize == 't':
        #    buckets = map(lambda x: x/sum_of_buckets, buckets)

        return buckets

    def get_samples(self):
        """ Get Samples of data file  """
        result = []
        segmentsize=30
        # Reduce this to very little to get very large trainingsets
        stride=5
        noOfBuckets=40
        for  start in range(0, len(self.data) - segmentsize, stride):
            if start + segmentsize <= len(self.data):
                segments_buckets = self.get_buckets(start, start + segmentsize, noOfBuckets)
                result.append(segments_buckets)
        return result
    
    def keep_last_lines(self, num_lines):
        """ Keep last lines of Samples  """
        self.data = self.data[-num_lines:]
        
"""
    Creacion del DataSet de datos apartir de los ficheros
    UCM
"""
class dataset:
    def __init__(self, foldername, filters = {}):
        """ Init sfile read  """
        self.data = []
        self.target = []
        self.activities = []
        noOfSamples = 0
        for activity, number in filters.items():
            samples = get_samples_file(foldername, filter=activity)
            for sample in samples:
                noOfSamples +=1
                self.data.append(sample)
                self.target.append(number)
                self.activities.append(activity)
        print( "---> File: " + foldername + ", Samples: " + str(noOfSamples))

        
# 
def get_samples_file(foldername, filter=None):
    """ Get Samples of data file. Obtener muestras de datos directamente del fichero  """
    samples = []
    for file in os.listdir(foldername):
        if filter and file.find(filter) == -1:
            continue
        for sample in sfile(foldername + '/' + file, None).get_samples():
            samples.append(sample)
    return samples