import logging
import os
import glob

from ..exceptions_ import (BadFormatException, BenzlimException)
from ..compat import printf
from ..config import Configuration

def execute_coverage():
    #An instance of the configuration
    config = Configuration.get_instance()
    #executing coverage for the sample test command
    os.system("coverage run %s test %s" % (config.base_dir, config.informaticup2018_dir))
    #renaming the created coverage file in order to merge the results after executing all the commands
    os.system("mv .coverage .coverage.test")
    #executing coverage for the sample predict command
    os.system("coverage run %s predict %s/tests/data_predict/stationen_ohne_marke.csv %s" % (config.base_dir, config.src_dir, config.informaticup2018_dir))
    #renaming the created coverage file in order to merge the results after executing all the commands
    os.system("mv .coverage .coverage.predict")
    #executing coverage for the sample route command
    os.system("coverage run %s route %s/tests/data_route/stationen_ohne_marke.csv %s" % (config.base_dir, config.src_dir, config.informaticup2018_dir))
    #renaming the created coverage file in order to merge the results after executing all the commands
    os.system("mv .coverage .coverage.route")
    #executing coverage for the sample train command
    os.system("coverage run %s train %s" % (config.base_dir, config.informaticup2018_dir))
    #renaming the created coverage file in order to merge the results after executing all the commands
    os.system("mv .coverage .coverage.train")
    #combining all the coverage files .coverage.test, .coverage.predict, .coverage.route and .coverage.train
    os.system("coverage combine")
    #creating html files for a nicer presentation of the results found under the folder 'htmlcov'
    os.system("coverage html")
    #printing the result onto the terminal window
    os.system("coverage report")
    printf("For a nicer presentation of the results please navigate to the folder 'htmlcov'.")
    return

def coverage():
    printf("Creating coverage benchmarks for benzlim...")
    execute_coverage()
    #test_route()
