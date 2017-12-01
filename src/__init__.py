import os
import sys
import argparse
from multiprocessing import Pool

from .train import Trainer
from .compat import printf
from .utils import create_file_dirs
from .dao import CSVDAO
from .config import Configuration
from .prediction import predict_prices_timestamps_x2_stations

def process_predictions(filename, dir_prices, out_filename=None, nb_workers=None):
    if out_filename is None:
        out_filename = os.path.join(Configuration.get_instance().output_dir, 'predictions.csv')
    timestamps_x2_stations = CSVDAO.get_predict_params(filename)
    res_infos = predict_prices_timestamps_x2_stations(timestamps_x2_stations, dir_prices, nb_workers)
    create_file_dirs(out_filename)
    with open(out_filename, 'w') as output_f:
        output_f.writelines("%s;%s;%s;%s\n"%(row) for row in res_infos)


def process_routing(filename, dir_prices, out_filename=None, gas_prices_file=None, nb_workers=None, auto_end_timestamp=True):
    if out_filename is None:
        out_filename = os.path.join(Configuration.get_instance().output_dir, 'predictions_route.csv')
    capacity, timestamps_stations = CSVDAO.get_route_params(filename)

    if gas_prices_file is None:
        timestamps_x2_stations = []
        end_timestamp = None
        for timestamp, station_id in timestamps_stations:
            timestamps_x2_stations.append((end_timestamp, timestamp, station_id))
            if auto_end_timestamp:
                end_timestamp = timestamp
        routing_infos = predict_prices_timestamps_x2_stations(timestamps_x2_stations, dir_prices, nb_workers)
    else:
        routing_infos = CSVDAO.get_predicted_prices(gas_prices_file)
    #routing_infos: [<end_timestamp>, <timestamp>, <station_id>, <pred_price>]

    #TODO check make sure the route and predictions match each oder
    if len(timestamps_stations) != len(routing_infos):
        printf("ERROR! incompatible prediction file")
    else:
        for idx, row in enumerate(routing_infos):
            row2 = timestamps_stations[idx]
            timestamp1, station1 = row[1], row[2]
            timestamp2, station2 = row2[0], row2[1]
            if timestamp1 != timestamp2 or station1 != station2:
                printf("ERROR! wrong match: timestamp/station")

    #TODO manage routing with infos in and output
    for end_timestamp, timestamp, station_id, pred_price in routing_infos:
        #TODO Build graph???
        printf(end_timestamp, timestamp, station_id, pred_price)
    ## Routing...

    #res_infos: [<timestamp>, <station>, <pred_price>, <gas_quantity>
    res_infos = []
    create_file_dirs(out_filename)
    with open(out_filename, 'w') as output_f:
        output_f.writelines("%s;%s;%s;%s\n"%(row) for row in res_infos)



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
    
    args = parser.parse_args()
    
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
    print args
    if args.command == "predict":
        process_predictions(config.file, config.prices_dir, config.output_file, config.nb_workers)
    elif args.command == "route":
        process_routing(config.file, config.prices_dir, config.output_file, args.gas_prices_file, config.nb_workers, args.auto_end_timestamp)
    elif args.command == "train":
        Trainer.train()
