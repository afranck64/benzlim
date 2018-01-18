import numpy as np

from .prediction import predict
from .prediction import classification
from .prediction.classification import Classifier
from .dao import CSVDAO
from .dao import StationDAO
from .compat import printf
from config import Configuration


def evaluate(station_id, ts, ground_ts, end_train_timestamp, dir_prices, nb_predictions=16):
    #print "GROUND:", ground_ts.head(10)
    #print "last_ts", ts.last("M")
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
    diff = diff.astype(int)
    return np.min(diff), np.max(diff), np.average(diff)

def benchmark_station(station_id, dir_prices, base_station_id=None, nb_predictions=5):
    """test predictions on <station_id> using values of <base_station_id> as ground truth,
    if base_station_id is not given, station_id is used as ground truth
    
    return prediction errors:
        min, max, avg"""
    ts = CSVDAO.get_station_dataframe(station_id, dir_prices)
    index_end = np.random.randint(2, ts.size)
    end_train_timestamp = ts.index.values.flat[index_end]
    # We test prediction till one month for the station
    if base_station_id is None:
        ground_ts = ts
    else:
        ground_ts = CSVDAO.get_station_dataframe(base_station_id, dir_prices)
    ground_ts = ts[end_train_timestamp:].first("1M")
    ts = ts[:end_train_timestamp]
    return evaluate(station_id, ts, ground_ts, end_train_timestamp, dir_prices, nb_predictions)


def process_benchmark_station(args):
    return benchmark_station(*args)

def benchmark_with_prices(nb_stations, dir_prices):
    stations = StationDAO.get_all_with_prices()
    station_ids = [row[0] for row in stations]
    lst_min = []
    lst_max = []
    lst_avg = []
    
    tasks = []
    for idx in range(nb_stations):
        station_id = np.random.choice(station_ids)
        #min_, max_, avg = benchmark_station(station_id, dir_prices)
        tasks.append((station_id, dir_prices))

    pool = Configuration.get_instance().get_pool()
    if pool is not None:
        lst_res = pool.map(process_benchmark_station, tasks)
        for res in lst_res:
            min_, max_, avg = res
            lst_min.append(min_)
            lst_max.append(max_)
            lst_avg.append(avg)
            #printf(min_, max_, avg)

    else:
        for task in tasks:
            min_, max_, avg = process_benchmark_station(task)
            lst_min.append(min_)
            lst_max.append(max_)
            lst_avg.append(avg)
            #printf(min_, max_, avg)
    min_ = min(lst_min)
    max_ = max(lst_max)
    avg = sum(lst_avg)/len(lst_avg) 
    printf("stations_with_prices: min: %s, max: %s, avg: %s: " % (min_, max_, avg))


def benchmark_without_prices(nb_stations, dir_prices):
    stations = StationDAO.get_all_with_prices()
    station_ids = [row[0] for row in stations]
    lst_min = []
    lst_max = []
    lst_avg = []
    tasks = []
    for idx in range(nb_stations):
        station_id = base_station_id = None
        while (station_id == base_station_id):
            base_station_id = np.random.choice(station_ids)
            base_station_row = stations[idx]
            station_id = Classifier.station_row2id(base_station_row, ignore_station=True)
            #TEST:
            #station_id = 14481
            #base_station_id = 5898

        tasks.append((station_id, dir_prices, base_station_id))


        #print "id, base_id:", station_id, base_station_id

    pool = Configuration.get_instance().get_pool()
    if pool is not None:
        lst_res = pool.map(process_benchmark_station, tasks)
        for res in lst_res:
            min_, max_, avg = res
            lst_min.append(min_)
            lst_max.append(max_)
            lst_avg.append(avg)
    else:
        for task in tasks:
            min_, max_, avg = process_benchmark_station(task)
            lst_min.append(min_)
            lst_max.append(max_)
            lst_avg.append(avg)
    min_ = min(lst_min)
    max_ = max(lst_max)
    avg = sum(lst_avg)/len(lst_avg)
    printf("stations_without_prices: min: %s, max: %s, avg: %s: " % (min_, max_, avg))


def process_benchmark(dir_prices, nb_stations=100):
    benchmark_with_prices(nb_stations, dir_prices)
    benchmark_without_prices(nb_stations, dir_prices)