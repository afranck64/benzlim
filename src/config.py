"""config.py - access benzlim's instance configuration"""

import logging
import os
import sys
import multiprocessing
import platform

from .compat import printf

class Configuration:
    """Contains the configuration to run a benzlim instance"""
    RESOURCE_DIR = "resources"
    OUTPUT_DIR = "out"
    CLASSIFIER_FILENAME = "classifier.pkl"
    DATABASE_FILENAME = "db.sqlite3"
    TIME_BINS = ['%02.d:00' % h for h in range(0, 24, 1)]
    def __init__(self, **kwargs):
        #hourly intervalls to take into consideration for the model training
        self.time_bins = self.TIME_BINS
        #nb of worker processes
        self.nb_workers = kwargs.get("nb_workers") or multiprocessing.cpu_count()
        if platform.system() in ("Windows",):
            if self.nb_workers > 1:
                logging.warning("Multiprocessing not yet supported on this platform. Switching to Mono-processing")
                self.nb_workers = 1
        # Working pool instance
        self.worker_pool = None
        #abspath to the <src> dir
        self.src_dir = os.path.abspath(os.path.join(os.path.split(__file__)[0], '.'))
        #abspath to the <benzlim> dir
        self.base_dir = os.path.split(self.src_dir)[0]
        output_dir = os.path.join(self.base_dir, self.OUTPUT_DIR)
        #path to the output dir
        self.output_dir = kwargs.get("output_dir", output_dir)
        #path to the <resources> dir
        self.resources_dir = os.path.join(self.base_dir, self.RESOURCE_DIR)
        #abspath to the sqlite-database
        self.database_file = os.path.join(self.resources_dir, self.DATABASE_FILENAME)
        #abspath to the dumped classifier
        self.classifier_file = os.path.join(self.resources_dir, self.CLASSIFIER_FILENAME)
        #path to the downloaded Informaticup2018 directory
        self.informaticup2018_dir = os.path.abspath(kwargs.get("informaticup2018_dir"))
        prices_dir = os.path.join(self.informaticup2018_dir, "Eingabedaten", "Benzinpreise")
        stations_file = os.path.join(self.informaticup2018_dir, "Eingabedaten", "Tankstellen.csv")
        #path to the file containing the stations files
        self.stations_file = kwargs.get("stations_file", stations_file)
        #path to the folder containing the stations' prices
        self.prices_dir = kwargs.get("prices_dir", prices_dir)
        #path to a generated gas prices file, usable for routing
        self.gas_prices_file = kwargs.get("gas_prices_file", None)
        #enable or disable caching price predictors
        self.enabled_cache = kwargs.get("enabled_cache", True)
        #output file
        self.output_file = kwargs.get("output_file")
        #input file
        self.file = kwargs.get("file")
        #logging level
        self.log_level = kwargs.get("log", None) or logging.WARNING

    @staticmethod
    def get_instance(**kwargs):
        if not hasattr(Configuration, "_config"):
            sys.exit("Missing configuration")
        return Configuration._config

    @staticmethod
    def config(**kwargs):
        config = Configuration(**kwargs)
        Configuration._config = config 
        logging.basicConfig(level=config.log_level)


    def get_pool(self):
        _config = self.get_instance()
        if self.worker_pool is None and self.nb_workers > 1:
            self.worker_pool = multiprocessing.Pool(self.nb_workers)
        return self.worker_pool

if __name__ == "__main__":
    printf(os.environ.get("INFORMATICUP2018_DIR", "(-_-)"))
    Configuration.config(**os.environ)
