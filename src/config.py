"""config.py - access benzlim's instance configuration"""

import os
import multiprocessing

class Configuration:
    """Contains the configuration to run a benzlim instance"""
    RESOURCE_DIR = "resources"
    OUTPUT_DIR = "out"
    CLASSIFIER_FILENAME = "classifier.pkl"
    DATABASE_FILENAME = "db.sqlite3"
    TIME_BINS = ['%02.d:00' % h for h in range(24)]
    def __init__(self, **kwargs):
        self.time_bins = self.TIME_BINS
        self.nb_workers = kwargs.get("nb_workers", multiprocessing.cpu_count())

        self.src_dir = os.path.abspath(os.path.join(os.path.split(__file__)[0], '.'))
        self.base_dir = os.path.split(self.src_dir)[0]
        output_dir = os.path.join(self.base_dir, self.OUTPUT_DIR)
        self.output_dir = kwargs.get("output_dir", output_dir)
        self.resources_dir = os.path.join(self.base_dir, self.RESOURCE_DIR)
        self.database_file = os.path.join(self.resources_dir, self.DATABASE_FILENAME)
        self.classifier_file = os.path.join(self.resources_dir, self.CLASSIFIER_FILENAME)
        self.informaticup2018_dir = os.path.abspath(kwargs.get("informaticup2018_dir"))
        prices_dir = os.path.join(self.informaticup2018_dir, "Eingabedaten/Benzinpreise")
        stations_file = os.path.join(self.informaticup2018_dir, "Eingabedaten/Tankstellen.csv")
        self.stations_file = kwargs.get("stations_file", stations_file)
        self.prices_dir = kwargs.get("prices_dir", prices_dir)
        self.gas_prices_file = kwargs.get("gas_prices_file", None)
        self.enable_cache = kwargs.get("enable_cache", False)
        self.output_file = kwargs.get("output_file")
        self.file = kwargs.get("file")
        self.verbose = kwargs.get("verbose", 1)

    @staticmethod
    def get_instance(**kwargs):
        if not hasattr(Configuration, "_config"):
            raise SystemExit("Missing configuration")
        return Configuration._config

    @staticmethod
    def config(**kwargs):
        Configuration._config = Configuration(**kwargs)        

if __name__ == "__main__":
    print os.environ.get("INFORMATICUP2018_DIR", "(-_-)")
    Configuration.config(**os.environ)
