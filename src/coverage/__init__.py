import logging
import os
import glob

from ..exceptions_ import (BadFormatException, BenzlimException)
from ..compat import printf
from ..config import Configuration

def execute_coverage(): #pragma: no cover
    #An instance of the configuration
    config = Configuration.get_instance()
    #executing coverage for the sample train command
    os.system("coverage run -p %s train %s --log error" % (config.base_dir, config.informaticup2018_dir))
    #renaming the created coverage file in order to merge the results after executing all the commands
    #os.system("mv .coverage .coverage.train")
    #executing coverage for the sample test command
    os.system("coverage run -p %s test %s --log error" % (config.base_dir, config.informaticup2018_dir))
    #renaming the created coverage file in order to merge the results after executing all the commands
    #os.system("mv .coverage .coverage.test")
    #executing coverage for the sample benchmark command
    os.system("coverage run -p %s benchmark %s -n1" % (config.base_dir, config.informaticup2018_dir))
    #renaming the created coverage file in order to merge the results after executing all the commands
    #os.system("mv .coverage .coverage.benchmark")
    #executing coverage for the sample predict command
    os.system("coverage run -p %s predict %s/tests/data_predict/stationen_ohne_marke.csv %s" % (config.base_dir, config.src_dir, config.informaticup2018_dir))
    #renaming the created coverage file in order to merge the results after executing all the commands
    #os.system("mv .coverage .coverage.predict")
    #executing coverage for the sample route command
    os.system("coverage run -p %s route %s/tests/data_route/stationen_ohne_marke.csv %s -n1" % (config.base_dir, config.src_dir, config.informaticup2018_dir))
    #renaming the created coverage file in order to merge the results after executing all the commands
    #os.system("mv .coverage .coverage.route")
    os.system("coverage run -p %s route -g  %s/tests/data_predict/stationen_mit_keine_benzin_preise_prices.csv %s/tests/data_route/stationen_mit_keine_benzin_preise.csv %s" % (config.base_dir, config.src_dir, config.src_dir, config.informaticup2018_dir))
    #os.system("mv .coverage .coverage.route.predicted")
    #combining all the coverage files .coverage.test, coverage.benchmark .coverage.predict, .coverage.route and .coverage.train
    os.system("coverage combine --append .coverage.*")
    #creating html files for a nicer presentation of the results found under the folder 'htmlcov'
    os.system("coverage html --directory=%s/htmlcov" % (config.output_dir))
    #printing the result onto the terminal window
    os.system("coverage report")
    printf("For a nicer presentation of the results please navigate to the folder '%s/htmlcov'." % config.output_dir)
    return

def coverage(): #pragma: no cover
    printf("Creating coverage benchmarks for benzlim...")
    execute_coverage()
