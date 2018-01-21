"""benchmark.py - Benchmarking tool"""
from math import ceil
import os.path
import numpy as np

from .prediction import predict
from .prediction import classification
from .prediction.classification import Classifier
from .dao import CSVDAO
from .dao import StationDAO
from .compat import printf
from .config import Configuration


def evaluate_prediction(station_id, ts, ground_ts, end_train_timestamp, dir_prices, nb_predictions):
    timestamps = ground_ts.index.values.flat
    prices = ground_ts.values.flat
    real_prices = np.zeros(nb_predictions)
    pred_prices = np.zeros(nb_predictions)
    for idt in range(nb_predictions):
        idx = np.random.randint(0, len(timestamps))
        timestamp = timestamps[idx]
        p_price = predict.predict_price(station_id, timestamp, end_train_timestamp, dir_prices, ts)
        real_prices[idt] = prices[idx]
        pred_prices[idt] = p_price
    diff = real_prices - pred_prices
    diff = abs(diff)
    diff += 0.5
    rel_diff = diff/real_prices
    diff = diff.astype(int)
    return np.max(diff), np.average(diff), np.average(rel_diff)

def _benchmark_prediction(station_id, dir_prices, base_station_id=None, nb_predictions=5):
    """test predictions on <station_id> using values of <base_station_id> as ground truth,
    if base_station_id is not given, station_id is used as ground truth
    
    return prediction errors:
        max, max, avg"""
    ts = CSVDAO.get_station_dataframe(station_id, dir_prices)
    index_end = np.random.randint(2, ts.size)
    end_train_timestamp = ts.index.values.flat[index_end]
    # We test prediction till one month befor the station
    if base_station_id is None:
        ground_ts = ts
    else:
        ground_ts = CSVDAO.get_station_dataframe(base_station_id, dir_prices)
    ground_ts = ts[end_train_timestamp:].first("1M")
    ts = ts[:end_train_timestamp]
    return evaluate_prediction(station_id, ts, ground_ts, end_train_timestamp, dir_prices, nb_predictions)


def process_benchmark_prediction(args):
    return _benchmark_prediction(*args)

def benchmark_with_prices(nb_stations, nb_predictions, dir_prices):
    stations = StationDAO.get_all_with_prices()
    station_ids = [row[0] for row in stations]
    lst_abs_max = []
    lst_abs_avg = []
    lst_rel_avg = []
    
    tasks = []
    for idx in range(nb_stations):
        station_id = np.random.choice(station_ids)
        tasks.append((station_id, dir_prices, None, nb_predictions))

    pool = Configuration.get_instance().get_pool()
    lst_res = []
    if pool is not None:
        lst_res = pool.map(process_benchmark_prediction, tasks)
    else:
        lst_res = [process_benchmark_prediction(task) for task in tasks]

    rows = []
    for idx, res in enumerate(lst_res):
        abs_max = int(ceil(res[0]))
        abs_avg = int(ceil(res[1]))
        rel_avg = round(res[2], 4)
        lst_abs_max.append(abs_max)
        lst_abs_avg.append(abs_avg)
        lst_rel_avg.append(rel_avg)
        rows.append((tasks[idx][0], abs_max, abs_avg, rel_avg))

    g_abs_max = max(lst_abs_max)
    g_abs_avg = sum(lst_abs_avg)/len(lst_abs_avg)
    g_rel_avg = sum(lst_rel_avg)/len(lst_rel_avg) 
    printf("stations_with_prices: max abs: %s, avg abs: %s, avg rel: %.3f: " % (g_abs_max, g_abs_avg, g_rel_avg))


    out_filename = os.path.join(Configuration.get_instance().output_dir, "benchmark_with_prices.csv")
    CSVDAO.export_to_csv(out_filename, rows, ["station_id", "abs error max", "avg abs err", "avg rel. err"])


def benchmark_without_prices(nb_stations, nb_predictions, dir_prices):
    stations = StationDAO.get_all_with_prices()
    station_ids = [row[0] for row in stations]
    lst_abs_max = []
    lst_abs_avg = []
    lst_rel_avg = []
    tasks = []
    for idx in range(nb_stations):
        station_id = base_station_id = None
        while (station_id == base_station_id):
            base_station_id = np.random.choice(station_ids)
            base_station_row = stations[idx]
            station_id = Classifier.station_row2id(base_station_row, ignore_station=True)
        tasks.append((station_id, dir_prices, base_station_id, nb_predictions))

    pool = Configuration.get_instance().get_pool()
    if pool is not None:
        lst_res = pool.map(process_benchmark_prediction, tasks)
    else:
        lst_res = [process_benchmark_prediction(task) for task in tasks]
    rows = []
    for idx, res in enumerate(lst_res):
        abs_max = int(ceil(res[0]))
        abs_avg = int(ceil(res[1]))
        rel_avg = round(res[2], 4)
        lst_abs_max.append(abs_max)
        lst_abs_avg.append(abs_avg)
        lst_rel_avg.append(rel_avg)
        rows.append((tasks[idx][-1], tasks[idx][0], abs_max, abs_avg, rel_avg))

    g_abs_max = max(lst_abs_max)
    g_abs_avg = sum(lst_abs_avg)/len(lst_abs_avg)
    g_rel_avg = sum(lst_rel_avg)/len(lst_rel_avg) 
    printf("stations_without_prices: max abs: %s, avg abs: %s, avg rel: %.3f: " % (g_abs_max, g_abs_avg, g_rel_avg))


    out_filename = os.path.join(Configuration.get_instance().output_dir, "benchmark_without_prices.csv")
    CSVDAO.export_to_csv(out_filename, rows, ["base_station_id", "used_station_id",  "abs error max", "avg abs err", "avg rel. err"])


def benchmark_predictions(nb_stations, nb_predictions, dir_prices):
    benchmark_with_prices(nb_stations, nb_predictions, dir_prices)
    benchmark_without_prices(nb_stations, nb_predictions, dir_prices)

def _benchmark_routing(route_file, route_prices_file):
    capacity, _ = CSVDAO.get_route_params(route_file)
    route_rows = CSVDAO.get_route_prices_params(route_prices_file)

def benchmark_routing(nb_stations, nb_predictions, dir_prices):
    pass
    
def process_benchmark(dir_prices, nb_stations=1, nb_predictions=5):
    benchmark_predictions(nb_stations, nb_predictions, dir_prices)