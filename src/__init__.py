import os
import sys
import argparse
from multiprocessing import Pool

from .train import Trainer
from .compat import printf
from .utils import create_file_dirs
from .dao import CSVDAO
from .config import Configuration
from .prediction import (predict_prices_timestamps_x2_stations, process_predictions, process_routing)
from .tests import test



def main():
    parser = argparse.ArgumentParser(prog="python benzlim")
    subparsers = parser.add_subparsers(dest="command", help="commands")

    # A predict command
    predict_parser = subparsers.add_parser("predict", help="Prices prediction")
    predict_parser.add_argument("-o", "--output_file", action="store", help="output filename")
    predict_parser.add_argument("-n", "--nb-workers", action="store", type=int, help="number of workers, default: cpu_count")
    predict_parser.add_argument("file", action="store", help="input filename")
    predict_parser.add_argument("informaticup2018_dir", action="store", help="Path referering to the InformatiCup/InformatiCup2018 folder")
    
    # A route command
    route_parser = subparsers.add_parser("route", help="Prices prediction and routing")
    route_parser.add_argument("-a", "--auto-end-timestamp", action="store", type=int, help="uses the timestamp at <t-1> as lastest available data timestamp at <t>. values: 0|1 default: 1 (enabled)", default=1)
    route_parser.add_argument("-o", "--output_file", action="store", help="output filename")
    route_parser.add_argument("-n", "--nb-workers", action="store", type=int, help="number of workers, default: cpu_count")
    route_parser.add_argument("-g", "--gas-prices-file", action="store", help="predicted gas prices file")
    route_parser.add_argument("file", action="store", help="input filename")
    route_parser.add_argument("informaticup2018_dir", action="store", help="Path referering to the InformatiCup/InformatiCup2018 folder")

    # A train command
    train_parser = subparsers.add_parser("train", help="Training using available data")
    train_parser.add_argument("informaticup2018_dir", action="store", help="Path referering to the InformatiCup/InformatiCup2018 folder")
    
    # A test command
    test_parser = subparsers.add_parser("test", help="Test the program on some station and edge cases")
    test_parser.add_argument("-n", "--nb-workers", action="store", type=int, help="number of workers, default: cpu_count")
    test_parser.add_argument("informaticup2018_dir", action="store", help="Path referering to the InformatiCup/InformatiCup2018 folder")


    args = parser.parse_args()
    
    if args.command in ("predict", "route"):
        if args.nb_workers is not None and args.nb_workers < 1:
            parser.error("argument -n/--nb-workers: expected at least 1")
        if not os.path.exists(args.file):
            parser.error("argument file: file <%s> not found" % args.file)
        if args.output_file and not os.path.exists(args.output_file):
            parser.error("argument output_file: file <%s> not found" % args.output_file)
        if not os.path.exists(args.informaticup2018_dir):
            parser.error("argument informaticup2018_dir: directory <%s> not found" % args.informaticup2018_dir)
        if args.gas_prices_file is not None:
            if not os.path.exists(args.gas_prices_file):
                parser.error("argument -g/--gas-prices_file: file <%s> not found" % args.gas_prices_file)
    Configuration.config(**vars(args))
    config = Configuration.get_instance()
    if args.command == "predict":
        process_predictions(config.file, config.prices_dir, config.output_file, config.nb_workers)
    elif args.command == "route":
        process_routing(config.file, config.prices_dir, config.output_file, args.gas_prices_file, config.nb_workers, args.auto_end_timestamp)
    elif args.command == "train":
        Trainer.train()
    elif args.command == "test":
        test()
