"""coverage - Coverage informations generation about benzlim"""
import logging
import os
import glob
import shutil
import sys

from ..exceptions_ import (BadFormatException, BenzlimException)
from ..compat import printf
from ..config import Configuration

def clean_mp_coverages(empty_only=True): #pragma: no cover
    coverage_residus = glob.glob(".coverage.*")
    if empty_only:
        coverage_residus = (cov_file for cov_file in coverage_residus if os.stat(cov_file).st_size == 0)
    for cov_file in coverage_residus:
        os.remove(os.path.abspath(cov_file))

def clean_benzlim(): #pragma: no cover
    config = Configuration.get_instance()
    if os.path.exists(config.database_file):
        os.remove(config.database_file)
    if os.path.exists(config.classifier_file):
        os.remove(config.classifier_file)
    clean_mp_coverages()
    if os.path.exists(".coverage"):
        os.remove(".coverage")

def execute_coverage(): #pragma: no cover
    #An instance of the configuration
    config = Configuration.get_instance()
    coverage_config = os.path.join(config.base_dir, ".coveragerc")
    coverage_run_cmd = "coverage run --append --rcfile=%s %s " % (coverage_config, config.base_dir)
    coverage_combine_cmd = "coverage combine --rcfile=%s .coverage.*" % coverage_config
    coverage_html_cmd = "coverage html --rcfile=%s --directory=%s/htmlcov" % (coverage_config, config.output_dir)
    coverage_report_cmd = "coverage report --rcfile=%s" % coverage_config
    clean_benzlim()

    #executing coverage for the sample train command
    os.system("%s train --informaticup2018-dir %s --log error" % (coverage_run_cmd, config.informaticup2018_dir))
    #renaming the created coverage file in order to merge the results after executing all the commands
    #os.system("mv .coverage .coverage.train")
    #executing coverage for the sample test command
    os.system("%s test --informaticup2018-dir %s --log error" % (coverage_run_cmd, config.informaticup2018_dir))
    #renaming the created coverage file in order to merge the results after executing all the commands
    #os.system("mv .coverage .coverage.test")
    #executing coverage for the sample benchmark command
    os.system("%s benchmark --informaticup2018-dir %s --nb-stations 2 --nb-predictions 2" % (coverage_run_cmd, config.informaticup2018_dir))
    os.system("%s benchmark --informaticup2018-dir %s -n1 --nb-stations 2 --nb-predictions 2" % (coverage_run_cmd, config.informaticup2018_dir))
    #renaming the created coverage file in order to merge the results after executing all the commands
    #os.system("mv .coverage .coverage.benchmark")
    #executing coverage for the sample predict command
    os.system("%s predict %s/tests/data_predict/stationen_ohne_marke.csv --informaticup2018-dir %s" % (coverage_run_cmd, config.src_dir, config.informaticup2018_dir))
    os.system("%s predict %s/tests/data_predict/stationen_ohne_marke.csv -n1 --informaticup2018-dir %s" % (coverage_run_cmd, config.src_dir, config.informaticup2018_dir))
    #renaming the created coverage file in order to merge the results after executing all the commands
    #os.system("mv .coverage .coverage.predict")
    #executing coverage for the sample route command
    os.system("%s route %s/tests/data_route/stationen_ohne_marke.csv --informaticup2018-dir %s" % (coverage_run_cmd, config.src_dir, config.informaticup2018_dir))
    os.system("%s route %s/tests/data_route/stationen_ohne_marke.csv -n1 --informaticup2018-dir %s" % (coverage_run_cmd, config.src_dir, config.informaticup2018_dir))
    #renaming the created coverage file in order to merge the results after executing all the commands
    #os.system("mv .coverage .coverage.route")
    os.system("%s route -g  %s/tests/data_predict/stationen_mit_keine_benzin_preise_prices.csv %s/tests/data_route/stationen_mit_keine_benzin_preise.csv --informaticup2018-dir %s" % (coverage_run_cmd, config.src_dir, config.src_dir, config.informaticup2018_dir))
    #os.system("mv .coverage .coverage.route.predicted")
    #combining all the coverage files .coverage.test, coverage.benchmark .coverage.predict, .coverage.route and .coverage.train
    printf("combine...")
    clean_mp_coverages(empty_only=True)
    os.system(coverage_combine_cmd)
    clean_mp_coverages(empty_only=False)
    printf("cominde!!!!!!!!!!")
    #clean residual coverage files from multiprocessing
    clean_mp_coverages()
    #creating html files for a nicer presentation of the results found under the folder 'htmlcov'
    os.system(coverage_html_cmd)
    #printing the result onto the terminal window
    os.system(coverage_report_cmd)
    printf("For a nicer presentation of the results please navigate to '%s/htmlcov/index.html'." % config.output_dir)

def coverage(): #pragma: no cover
    printf("Creating coverage benchmarks for benzlim...")
    execute_coverage()
