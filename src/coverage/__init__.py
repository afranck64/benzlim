import logging
import os
import glob

from ..exceptions_ import (BadFormatException, BenzlimException)
from ..compat import printf
from ..config import Configuration

def execute_coverage():
    config = Configuration.get_instance()
    os.system("coverage run %s test %s" % (config.base_dir, config.informaticup2018_dir))
    os.system("mv .coverage .coverage.test")
    os.system("coverage run %s predict %s/tests/data_predict/stationen_ohne_marke.csv %s" % (config.base_dir, config.src_dir, config.informaticup2018_dir))
    os.system("mv .coverage .coverage.predict")
    os.system("coverage run %s route %s/tests/data_route/stationen_ohne_marke.csv %s" % (config.base_dir, config.src_dir, config.informaticup2018_dir))
    os.system("mv .coverage .coverage.route")
    os.system("coverage run %s train %s" % (config.base_dir, config.informaticup2018_dir))
    os.system("mv .coverage .coverage.train")
    os.system("coverage combine")
    os.system("coverage html")
    os.system("coverage report")
    printf("For a nicer presentation of the results please navigate to the folder 'htmlcov'.")
    return

def coverage():
    printf("Creating coverage benchmarks for benzlim...")
    execute_coverage()
    #test_route()
