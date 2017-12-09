import os
from multiprocessing import Pool

from . import predict
from ..b_exceptions import BenzlimException
from ..compat import printf
from ..config import Configuration
from ..dao import CSVDAO
from ..utils import create_file_dirs



def process_task(args):
    try:
        result = predict.predict_price(*args)
        return result
    except BenzlimException as err:
        return 1000

def predict_prices_timestamps_x2_stations(timestamps_x2_stations, dir_prices, nb_workers=None):
    """return [<end_timestamp>, <timestamp>, <station_id>, <pred_price>],
    timestamps_x2_stations: list[<end_timestamp>, <timestamp>, <station_id>]
    dir_prices: directory path
    """
    printf(timestamps_x2_stations)
    pred_params = [((station_id, timestamp, end_timestamp, dir_prices)) for end_timestamp, timestamp, station_id in timestamps_x2_stations]
    if nb_workers!=1:
        pool = Pool(nb_workers)
        pred_prices = pool.map(process_task, pred_params)
    else:
        pred_prices = [process_task(task) for task in pred_params]
    res_infos = []
    for idx, pred_price in enumerate(pred_prices):
        end_timestamp, timestamp, station_id = timestamps_x2_stations[idx]
        res_infos.append((end_timestamp, timestamp, station_id, pred_price))
    return res_infos


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
