from . import predict

from multiprocessing import Pool


def process_task(args):
    result = predict.predict_price(*args)
    return result

def predict_prices_timestamps_x2_stations(timestamps_x2_stations, dir_prices, nb_workers=None):
    """return [<end_timestamp>, <timestamp>, <station_id>, <pred_price>],
    timestamps_x2_stations: list[<end_timestamp>, <timestamp>, <station_id>]
    dir_prices: directory path
    """
    pool = Pool(nb_workers)
    pred_params = [((station_id, timestamp, end_timestamp, dir_prices)) for end_timestamp, timestamp, station_id in timestamps_x2_stations]
    pred_prices = pool.map(process_task, pred_params)
    res_infos = []
    for idx, pred_price in enumerate(pred_prices):
        end_timestamp, timestamp, station_id = timestamps_x2_stations[idx]
        res_infos.append((end_timestamp, timestamp, station_id, pred_price))
    return res_infos
