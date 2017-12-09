from math import atan2, pi
import os

import pandas as pd

from ..exceptions_ import (BadFormatException, PriceNotFoundException)
from ..compat import printf, pickle
from ..config import Configuration
from ..dao import StationDAO
from ..utils import cosine_sim, cosine_sim2, diff_score

LATITUDE_MAX = 90.0
LONGITUDE_MAX = 180.0
#A number big enough to cover ascores_labels stations
HASH_MAX = 982451653
#German: nb_letters + nb_digits + punctuation
NB_CHARS = 30 + 10 + 5

def get_str_hash(str_obj):
    """Generates a python/platform indepent str-hash"""
    if not isinstance(str_obj, (str, unicode)):
        return -1
    obj_hash = len(str_obj)
    for symbol in str_obj:
        obj_hash *= ord(symbol) % NB_CHARS
        obj_hash %= HASH_MAX + 1
    return obj_hash

def n_cos(v1, v2):
    return 1 - abs(cosine_sim2(v1, v2))


class CSClassifier(object):
    def __init__(self, scoring_function=None, partition_index=0):
        self.trained_data = dict()
        self.scoring_function = scoring_function or diff_score
        self.last_pred = []
        self.partitions = dict()
        self.partition_index = partition_index

    def fit(self, x_values, labels):
        classifier = CSClassifier()
        classifier.scoring_function = self.scoring_function
        classifier.partition_index = self.partition_index
        classifier.partitions = dict()
        if classifier.partition_index is not None:
            for id_, x in enumerate(x_values): 
                x_escaped_index = self._escaped_index(x)
                classifier.trained_data[labels[id_]] = x_escaped_index
                partition_key = x[self.partition_index]
                partition = classifier.partitions.get(partition_key, {})
                partition[labels[id_]] = x_escaped_index
                classifier.partitions[partition_key] = partition
        else:
            for id_, x in enumerate(x_values): 
                classifier.trained_data[labels[id_]] = x
        return classifier

    def predict(self, x):
        """predict class for features x based on the training data"""
        trained_data = dict()
        if self.partition_index is not None:
            partition_key = x[self.partition_index]
            partition = self.partitions.get(partition_key, dict())
            if partition:
                trained_data = partition
            else:
                trained_data = self.trained_data
        else:
            trained_data = trained_data

        if self.partition_index is not None:
            x_escaped_index = self._escaped_index(x)
            scores_labels = [(self.scoring_function(x_l, x_escaped_index), label) for label, x_l in trained_data.items()]
        else:
            scores_labels = [(self.scoring_function(x_l, x), label) for label, x_l in trained_data.items()]
        scores_labels.sort()
        self.last_pred = [trained_data[scores_labels[i][1]]  for i in range(0, len(scores_labels))]
        return scores_labels[0][1]

    def _escaped_index(self, x):
        res =  x[:self.partition_index] + x[self.partition_index+1:]
        return res


class Classifier(object):
    _classifier = None
    def __init__(self):
        pass

    @classmethod
    def get_category(cls, station_row):
        """Return a category for the given station"""
        return station_row[0]

    @classmethod
    def station_id2id(cls, station_id, end_train_timestamp=None):
        """Return a usable station id"""
        station_row = StationDAO.get(station_id)
        return cls.station_row2id(station_row, end_train_timestamp)
    
    @classmethod
    def station_row2id(cls, station_row, end_train_timestamp=None):
        """Return a usable (with prices available) id"""
        station_id = station_row[0]
        station_begin_timestamp = station_row[-1]
        is_prices_available = station_row[-2]   
        if end_train_timestamp is None:
            if is_prices_available:
                return station_id
            else:
                if cls._classifier is None:
                    cls.load()
                return cls._classifier.predict(cls.get_station_features(station_row))
        else:
            if is_prices_available and pd.Timestamp(end_train_timestamp) > pd.Timestamp(station_begin_timestamp):
                return station_id
            else:
                ext_stations = StationDAO.get_all_before(end_train_timestamp)
                if not ext_stations:
                    raise PriceNotFoundException("No training data available")
                classifier = cls.train(*cls.get_prepared_data(ext_stations))
                category = classifier.predict(cls.get_station_features(station_row))
                printf(classifier.last_pred[:2])
                return category

    @classmethod
    def get_station_features(cls, station_row):
        """Return features for the given station"""
        features = station_row[2].lower(), station_row[7], station_row[8]
        return features
      
    @classmethod  
    def get_prepared_data(cls, ext_stations=None):
        """return features with corresponding classes"""
        ext_stations = ext_stations or StationDAO.get_all_with_prices()
        features = (cls.get_station_features(row) for row in ext_stations)
        classes = (cls.get_category(row) for row in ext_stations)
        return features, classes

    @classmethod
    def train(cls, features=None, classes=None):
        classifier = CSClassifier()
        if classes is None or features is None:
            features, classes = cls.get_prepared_data()
        X = tuple(features)
        Y = tuple(classes)
        classifier = classifier.fit(X, Y)
        return classifier

    @classmethod
    def dump(cls, classifier, filename=None):
        filename = filename or Configuration.get_instance().classifier_file
        with open(filename, 'w') as output_file:
            pickle.dump(classifier, output_file)

    @classmethod
    def load(cls, filename=None, create_on_error=True):
        filename = filename or Configuration.get_instance().classifier_file
        if create_on_error:
            try:
                with open(filename) as input_f:
                    classifier = pickle.load(input_f)
                cls._classifier = classifier
            except:
                #TODO logging
                classifier = cls.train()
                cls._classifier = classifier
                cls.dump(classifier)
        return classifier

if __name__ == "__main__":
    Configuration.config(**os.environ)

    try:
        clf = Classifier.load()
    except:
        clf = Classifier.train()
        Classifier.dump(clf)

    missing_stations = StationDAO.get_all_without_prices()
    for row in [5, 7, 33]:
        #sid = row[0]
        sid = row
        cat = Classifier.station_id2id(row)
        if cat!= sid:
            printf("STATION: (%s) => (%s) " % (sid, cat), clf.last_pred[:2])