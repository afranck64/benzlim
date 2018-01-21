"""Benzlim"""
import logging
import os
import sys
import argparse

from .train import Trainer
from .benchmark import process_benchmark
from .compat import printf
from .utils import create_file_dirs
from .dao import CSVDAO
from .config import Configuration
from .prediction import (predict_prices_timestamps_x2_stations, process_predictions, process_routing)
from .tests import test
from .coverage import coverage

_log_names = [logging.getLevelName(lvl) for lvl in (logging.DEBUG, logging.CRITICAL, logging.ERROR, logging.INFO, logging.WARNING, logging.NOTSET)]

def main():
    parser = argparse.ArgumentParser(prog="python benzlim")
    subparsers = parser.add_subparsers(dest="command", help="commands")
    fallback_dir = os.path.abspath(os.path.join(os.path.split(__file__)[0], "../../InformatiCup2018"))

    # A predict command
    predict_parser = subparsers.add_parser("predict", help="Prices prediction")
    predict_parser.add_argument("-o", "--output_file", action="store", help="output filename")
    predict_parser.add_argument("-n", "--nb-workers", action="store", type=int, help="number of workers, default: cpu_count")
    predict_parser.add_argument("--log", action="store", help="Loging level, default: WARNING, values: %s " % _log_names)
    predict_parser.add_argument("--informaticup2018-dir", action="store", help="Path referring to the InformatiCup/InformatiCup2018 folder", default=fallback_dir)
    predict_parser.add_argument("file", action="store", help="input filename")
    
    # A route command
    route_parser = subparsers.add_parser("route", help="Prices prediction and routing")
    route_parser.add_argument("-a", "--auto-end-timestamp", action="store", type=int, help="uses the timestamp at <t-1> as lastest available data timestamp at <t>. values: 0|1 default: 1 (enabled)", default=1)
    route_parser.add_argument("-o", "--output_file", action="store", help="output filename")
    route_parser.add_argument("-n", "--nb-workers", action="store", type=int, help="number of workers, default: cpu_count")
    route_parser.add_argument("-g", "--gas-prices-file", action="store", help="predicted gas prices file")
    route_parser.add_argument("--log", action="store", help="Loging level, default: WARNING, values: %s " % _log_names)
    route_parser.add_argument("--informaticup2018-dir", action="store", help="Path referring to the InformatiCup/InformatiCup2018 folder", default=fallback_dir)
    route_parser.add_argument("file", action="store", help="input filename")

    # A train command
    train_parser = subparsers.add_parser("train", help="Training using available data")
    train_parser.add_argument("--log", action="store", help="Loging level, default: WARNING, values: %s " % _log_names)
    train_parser.add_argument("--force", action="store_true", help="Force overwriting existing training data")
    train_parser.add_argument("--informaticup2018-dir", action="store", help="Path referring to the InformatiCup/InformatiCup2018 folder", default=fallback_dir)
    
    # A test command
    test_parser = subparsers.add_parser("test", help="Test the program on some station and edge cases")
    test_parser.add_argument("-n", "--nb-workers", action="store", type=int, help="number of workers, default: cpu_count")
    test_parser.add_argument("--log", action="store", help="Loging level, default: WARNING, values: %s " % _log_names)
    test_parser.add_argument("--informaticup2018-dir", action="store", help="Path referring to the InformatiCup/InformatiCup2018 folder", default=fallback_dir)


    # A benchmark command
    bench_parser = subparsers.add_parser("benchmark", help="Run light prediction benchmark")
    bench_parser.add_argument("-n", "--nb-workers", action="store", type=int, help="number of workers, default: cpu_count")
    bench_parser.add_argument("--nb-predictions", action="store", type=int, help="number predictions per station, default: 5", default=5)
    bench_parser.add_argument("--nb-stations", action="store", type=int, help="number of stations to benchmark, default: 100", default=100)
    bench_parser.add_argument("--informaticup2018-dir", action="store", help="Path referring to the InformatiCup/InformatiCup2018 folder", default=fallback_dir)
    bench_parser.add_argument("--log", action="store", help="Loging level, default: WARNING, values: %s " % _log_names)

    # A coverage command
    coverage_parser = subparsers.add_parser("coverage", help="Create coverage benchmarking data under the folder 'htmlcov'")
    coverage_parser.add_argument("--log", action="store", help="Loging level, default: WARNING, values: %s " % _log_names)
    coverage_parser.add_argument("--informaticup2018-dir", action="store", help="Path referring to the InformatiCup/InformatiCup2018 folder", default=fallback_dir)

    args = parser.parse_args()
    if args.log:
        if args.log.isdigit():
            args.log = int(args.log)
        else:
            args.log = args.log.upper()
        if args.log not in _log_names:
            parser.error("argument -l/--log: wrong value. expected: %s" % _log_names)
    if args.command in ("predict", "route"):
        if args.nb_workers is not None and args.nb_workers < 1:
            parser.error("argument -n/--nb-workers: expected at least 1")
        if not os.path.exists(args.file):
            parser.error("argument file: file <%s> not found" % args.file)
        if args.output_file and not os.path.exists(args.output_file):
            parser.error("argument output_file: file <%s> not found" % args.output_file)
    if args.command in ("route"):
        if args.gas_prices_file is not None:
            if not os.path.exists(args.gas_prices_file):
                parser.error("argument -g/--gas-prices_file: file <%s> not found" % args.gas_prices_file)
    if not os.path.exists(args.informaticup2018_dir):
        parser.error("argument --informaticup2018-dir: directory <%s> not found" % args.informaticup2018_dir)

    Configuration.config(**vars(args))
    config = Configuration.get_instance()

    #
    if (args.command not in ("train", "coverage")):
        Trainer.autotrain()
    if args.command == "predict":
        process_predictions(config.file, config.prices_dir, config.output_file, config.nb_workers)
    elif args.command == "route":
        process_routing(config.file, config.prices_dir, config.output_file, args.gas_prices_file, config.nb_workers, args.auto_end_timestamp)
    elif args.command == "train":
        Trainer.train(args.force)
    elif args.command == "test":
        test()
    elif args.command == "benchmark":
        process_benchmark(config.prices_dir, args.nb_stations, args.nb_predictions)
    elif args.command == "coverage":
        coverage()
