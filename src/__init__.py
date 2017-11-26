import os
import sys
import argparse
from multiprocessing import Pool

from .compat import printf
from . import utils
from . import predict

def process_task(args):
    result = predict.predict_price(*args)
    return result

def predict_prices_timestamps_x2_stations(timestamps_x2_stations, dir_prices, nb_workers=None):
    """return [<end_timestamp>, <timestamp>, <station_id>, <pred_price>],
    timestamps_x2_stations: list[<end_timestamp>, <timestamp>, <station_id>]
    dir_prices: directory path
    """
    #TODO fix parallel predictions
    pool = Pool(nb_workers)

    pred_params = [((station_id, timestamp, end_timestamp, dir_prices)) for end_timestamp, timestamp, station_id in timestamps_x2_stations]
    pred_prices = pool.map(process_task, pred_params)
    res_infos = []
    for idx, pred_price in enumerate(pred_prices):
        end_timestamp, timestamp, station_id = timestamps_x2_stations[idx]
        res_infos.append((end_timestamp, timestamp, station_id, pred_price))
    return res_infos


def process_predictions(filename, dir_prices, out_filename=None, nb_workers=None):
    out_filename = out_filename or 'out/predictions.csv'
    timestamps_x2_stations = utils.get_prediction_params(filename)

    res_infos = predict_prices_timestamps_x2_stations(timestamps_x2_stations, dir_prices, nb_workers)
    with open(out_filename, 'w') as output_f:
        output_f.writelines("%s;%s;%s;%s\n"%(row) for row in res_infos)


def process_routing(filename, dir_prices, out_filename=None, gas_prices_file=None, nb_workers=None, auto_end_timestamp=True):
    out_filename = out_filename or "out/predictions_route.csv"
    capacity, timestamps_stations = utils.get_route_params(filename)

    if gas_prices_file is None:
        timestamps_x2_stations = []
        end_timestamp = None
        for timestamp, station_id in timestamps_stations:
            timestamps_x2_stations.append((end_timestamp, timestamp, station_id))
            if auto_end_timestamp:
                end_timestamp = timestamp
        routing_infos = predict_prices_timestamps_x2_stations(timestamps_x2_stations, dir_prices, nb_workers)
    else:
        routing_infos = utils.get_predicted_prices(gas_prices_file)
    #routing_infos: [<end_timestamp>, <timestamp>, <station_id>, <pred_price>]

    #TODO check make sure the route and predictions match each oder
    if len(timestamps_stations) != len(routing_infos):
        print ("ERROR! incompatible prediction file")
    else:
        for idx, row in enumerate(routing_infos):
            row2 = timestamps_stations[idx]
            timestamp1, station1 = row[1], row[2]
            timestamp2, station2 = row2[0], row2[1]
            if timestamp1 != timestamp2 or station1 != station2:
                print ("ERROR! wrong match: timestamp/station")

    #TODO manage routing with infos in and output
    for end_timestamp, timestamp, station_id, pred_price in routing_infos:
        #TODO Build graph???
        print (end_timestamp, timestamp, station_id, pred_price)
    ## Routing...

    #res_infos: [<timestamp>, <station>, <pred_price>, <gas_quantity>
    res_infos = []
    with open(out_filename, 'w') as output_f:
        output_f.writelines("%s;%s;%s;%s\n"%(row) for row in res_infos)



def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-p", "--prediction", action="store_true", help="make prediction for considering end-training time")
    group.add_argument("-r", "--routing", action="store_true", help="make a prediction and optimizes refuel strategy")
    parser.add_argument("-a", "--auto-end-timestamp", action="store", type=int, help="uses the timestamp at <t-1> as lastest available data timestamp at <t>. values: 0|1 default: 1 (enabled)", default=1)
    parser.add_argument("-o", "--output", action="store", help="output filename")
    parser.add_argument("-n", "--nb-workers", action="store", type=int, help="number of workers, default: cpu_count")
    parser.add_argument("-g", "--gas-prices-file", action="store", help="predicted gas prices file")
    parser.add_argument("file", action="store", help="input filename")
    parser.add_argument("dir_informaticup2018", action="store", help="Path referering to the InformatiCup/InformatiCup2018 folder")
    args = parser.parse_args()
    
    if args.nb_workers is not None and args.nb_workers < 1:
        parser.error("argument -n/--nb-workers: expected at least 1")
    if not os.path.exists(args.file):
        parser.error("argument file: file <%s> not found" % args.file)
    if not os.path.exists(args.dir_informaticup2018):
        parser.error("argument dir_informaticup2018: directory <%s> not found" % args.dir_informaticup2018)
    if args.gas_prices_file is not None:
        if not os.path.exists(args.gas_prices_file):
            parser.error("argument -g/--gas-prices_file: file <%s> not found" % args.gas_prices_file)
    dir_prices = os.path.join(args.dir_informaticup2018, "Eingabedaten/Benzinpreise")
    if args.prediction:
        process_predictions(args.file, dir_prices, args.output, args.nb_workers)
    elif args.routing:
        process_routing(args.file, dir_prices, args.output, args.gas_prices_file, args.nb_workers, args.auto_end_timestamp)