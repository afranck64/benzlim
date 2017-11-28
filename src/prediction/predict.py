

import cPickle as pickle
import os
import warnings

import pandas as pd
import numpy as np
import dateutil

from .. import utils

warnings.simplefilter('ignore', np.RankWarning)

TEST_STATION_ID = 11108
DEFAULT_END_TRAIN_TIMESTAMP = "2015-07-30 00:00:00"
TEST_BEGIN_RANGE_TIMESTAMP = "2015-07-30" #DEFAULT_END_TRAIN_TIMESTAMP
TEST_END_RANGE_TIMESTAMP = "2015-08-31"

CACHE_PREDICTORS = {}

class Predictor(object):
    def __init__(self, full_predictor=None, full_converter=None, year_predictor=None, month_predictor=None, week_predictor=None, day_predictor=None, hour_predictor=None, min_predictor=None):
        """
        full_predictor: <callable> return the complete prediction for a given timestamp
        year_predictor: <callable> return the corresponding yearly average price 
        month_predictor: <callable> return the month relative average (from the year)
        week_predictor: <callable> return the corresponding relative average (from the month)
        day_predictor: <callable> the relative day predictor
        hour_predictor: <callable> a relative hour averag predictor
        min_predictor: <callable> a relative minutes predictor

        if full_predictor: is submitted, it is used for the prediction
        """
        self.year_predictor = year_predictor
        self.month_predictor = month_predictor
        self.week_predictor = week_predictor
        self.day_predictor = day_predictor
        self.hour_predictor = hour_predictor
        self.min_predictor = min_predictor
        self.full_predictor = full_predictor
        self.full_converter = full_converter

    def predict(self, dt):
        """Return the predicted price at the timestamp <dt>
        dt: <str|pd.Timestamp|np.datetime64|datetime> the timestamp"""
        if self.full_predictor is not None:
            if self.full_converter is not None:
                return self.full_predictor(self.full_converter(dt))
            return self.full_predictor(dt)
        res_price = 0
        dt = pd.Timestamp(dt)
        if self.year_predictor is not None:
            res_price += self.year_predictor(get_time(dt, 'Y'))
        if self.month_predictor is not None:
            res_price += self.month_predictor(get_time(dt, 'M'))
        if self.week_predictor is not None:
            res_price += self.week_predictor(get_time(dt, 'W'))
        if self.day_predictor is not None:
            res_price += self.day_predictor(get_time(dt, 'D'))
        if self.hour_predictor is not None:
            res_price += self.hour_predictor(get_time(dt, 'H'))
        if self.min_predictor is not None:
            res_price += self.min_predictor(get_time(dt, 'T'))
        return res_price

    def __call__(self, dt):
        """callable interface to the predict method"""
        return self.predict(dt)


def get_station_dataframe(station_id, dir_prices, datetime_parser=None):
    """return a DataFrame containing timestamps and prices of the station <station_id>"""
    datetime_parser = datetime_parser or dateutil.parser.parse
    station_fic = utils.get_station_filename(station_id, dir_prices)
    ts = pd.read_csv(station_fic, index_col='timestamp', delimiter=";", header=None, names=["timestamp", "price"], parse_dates=True)
    return ts

def get_freq_avg(ts, freq="30T", fill_method='bfill', fill_method2=None):
    if fill_method2 is not None:
        return ts.resample(freq, fill_method=fill_method).fillna(fill_method2)    
    return ts.resample(freq, fill_method=fill_method)

def get_time(timestamp, field=None):
    """return the corresponding value of the attribut corresponding to <field>
    timestamp: <pd.Timestamp>
    field: <str> Y, M, W, D, H, T"""
    field = field or "T"
    if field=="T":
        return timestamp.minute
    elif field=="H":
        return timestamp.hour
    elif field=="D":
        return timestamp.weekday()
    elif field=="W":
        return timestamp.week
    elif field=="M":
        return timestamp.month
    elif field=="Y":
        return timestamp.year
    return -1

def get_price_predictor(station_id, dir_prices, ts=None, end_train_timestamp=None, poly_deg=3):
    """Generate a price predictor for gas station <station_id> of the timeserie <ts>,
    station_id: str, the id of the station
    ts: DataFrame|Serie, the price's timeserie of as gas station
    end_train_timestamp: str, the last usable timestamp for learning,
    poly_deg: int, the degree of polynomial approximation [1,2,3,4,5]
    return the callable prediction(timestamp)

    if station_id is submitted, the predictor is cached resp. recovered from the cache"""
    cache_key = None
    if station_id is not None:
        cache_key = (station_id, end_train_timestamp, poly_deg, 1)
    if cache_key in CACHE_PREDICTORS:
        #TODO data gathered from cache
        return CACHE_PREDICTORS[cache_key]
    ts = ts if ts is not None else get_station_dataframe(station_id, dir_prices)
    if end_train_timestamp is not None:
        ts = ts[:end_train_timestamp]
    NB_YEARS = 1*2
    NB_MONTHS = 12 * 2
    NB_WEEKS = 4 * 12
    NB_DAYS = 7 * 4
    NB_HOURS = 24 * 7
    NB_MINUTES = 60 * 24
    year_avg_predictor = None
    month_rel_predictor = None
    week_rel_predictor = None
    day_rel_predictor = None
    hour_rel_predictor = None
    min_rel_predictor = None
    ts_year = get_freq_avg(ts, 'AS').tail(NB_YEARS)
    ts_month = get_freq_avg(ts, 'M').tail(NB_MONTHS)
    ts_week = get_freq_avg(ts, 'W').tail(NB_WEEKS)
    ts_day = get_freq_avg(ts, 'D').tail(NB_DAYS)
    ts_hour = get_freq_avg(ts, 'H').tail(NB_HOURS)
    ts_min = get_freq_avg(ts, 'T').tail(NB_MINUTES)

    year_avg_predictor = np.poly1d(np.polyfit(np.array([get_time(dt, 'Y') for dt in ts_year.index]), ts_year.values.flat, poly_deg))

    #relative values are generated using average and predicted values to carriage the prediction errors
    ts_month_rel_x = np.array([get_time(pd.Timestamp(dt), 'M') for dt in ts_month.index.values.flat])
    ts_month_rel_y = ts_month.values.flat - year_avg_predictor([get_time(pd.Timestamp(dt), 'Y') for dt in ts_month.index.values.flat])
    month_rel_predictor = np.poly1d(np.polyfit(np.array(ts_month_rel_x).flat, ts_month_rel_y.flat, poly_deg))

    ts_week_dt = [pd.Timestamp(dt) for dt in ts_week.index.values.flat]
    ts_week_rel_x = np.array([get_time(pd.Timestamp(dt), 'W') for dt in ts_week_dt])
    ts_week_rel_y = ts_week.values.flat - (year_avg_predictor([get_time(dt, 'Y') for dt in ts_week_dt]) + month_rel_predictor([get_time(pd.Timestamp(dt), 'M') for dt in ts_week.index.values.flat]))
    week_rel_predictor = np.poly1d(np.polyfit(np.array(ts_week_rel_x).flat, ts_week_rel_y.flat, poly_deg))

    ts_day_dt = [pd.Timestamp(dt) for dt in ts_day.index.values.flat]
    ts_day_rel_x = np.array([get_time(pd.Timestamp(dt), 'D') for dt in ts_day_dt])
    ts_day_rel_y = ts_day.values.flat - (year_avg_predictor([get_time(dt, 'Y') for dt in ts_day_dt]) + month_rel_predictor([get_time(dt, 'M') for dt in ts_day_dt]) + week_rel_predictor([get_time(dt, 'W') for dt in ts_day_dt]))
    day_rel_predictor = np.poly1d(np.polyfit(np.array(ts_day_rel_x).flat, ts_day_rel_y.flat, poly_deg))

    ts_hour_dt = [pd.Timestamp(dt) for dt in ts_hour.index.values.flat]
    ts_hour_rel_x = np.array([get_time(pd.Timestamp(dt), 'H') for dt in ts_hour_dt])
    ts_hour_rel_y = ts_hour.values.flat - (year_avg_predictor([get_time(dt, 'Y') for dt in ts_hour_dt]) + month_rel_predictor([get_time(dt, 'M') for dt in ts_hour_dt]) + week_rel_predictor([get_time(dt, 'W') for dt in ts_hour_dt]) + day_rel_predictor([get_time(dt, 'D') for dt in ts_hour_dt]))
    hour_rel_predictor = np.poly1d(np.polyfit(np.array(ts_hour_rel_x).flat, ts_hour_rel_y.flat, poly_deg))

    ts_min_dt = [pd.Timestamp(dt) for dt in ts_min.index.values.flat]
    ts_min_rel_x = np.array([get_time(pd.Timestamp(dt), 'T') for dt in ts_min_dt])
    ts_min_rel_y = ts_min.values.flat - (year_avg_predictor([get_time(dt, 'Y') for dt in ts_min_dt]) + month_rel_predictor([get_time(dt, 'M') for dt in ts_min_dt]) + week_rel_predictor([get_time(dt, 'W') for dt in ts_min_dt]) + day_rel_predictor([get_time(dt, 'D') for dt in ts_min_dt])  + hour_rel_predictor([get_time(dt, 'H') for dt in ts_min_dt]))
    min_rel_predictor = np.poly1d(np.polyfit(np.array(ts_min_rel_x).flat, ts_min_rel_y.flat, poly_deg))
    
    def predictor(timestamp):
        timestamp = pd.Timestamp(timestamp)
        res = year_avg_predictor(get_time(timestamp, 'Y'))\
                + month_rel_predictor(get_time(timestamp, 'M'))\
                + week_rel_predictor(get_time(timestamp, 'W'))\
                + day_rel_predictor(get_time(timestamp, 'D'))\
                + hour_rel_predictor(get_time(timestamp, 'H'))\
                + min_rel_predictor(get_time(timestamp, 'T'))
        return int(round(res))
    #import cPickle as pickle
    #with open("out.dump", 'w') as out_f:
    #    pickle.dump(month_rel_predictor, out_f)
    if cache_key:
        CACHE_PREDICTORS[cache_key] = predictor
    return predictor


def get_price_predictor2(station_id, dir_prices, ts=None, end_train_timestamp=None, poly_deg=2):
    """Generate a price predictor for gas station <station_id> of the timeserie <ts>,
    station_id: str, the id of the station
    ts: DataFrame|Series, the price's timeserie of as gas station
    end_train_timestamp: str, the last usable timestamp for learning,
    poly_deg: int, the degree of polynomial approximation
    return the predictor as a numpy.poly1d

    if station_id is submitted, the predictor is cached resp. recovered from the cache"""
    cache_key = None
    if station_id is not None:
        cache_key = (station_id, end_train_timestamp, poly_deg, 2)
    if cache_key in CACHE_PREDICTORS:
        print "From cache"
        return CACHE_PREDICTORS[cache_key]
    ts = ts if ts is not None else get_station_dataframe(station_id, dir_prices)
    if end_train_timestamp is not None:
        ts = ts[:pd.Timestamp(end_train_timestamp)]
    predictor_f = np.poly1d(np.polyfit(ts.index.values.astype(int).flat, ts.values.flat, poly_deg))
    predictor = lambda timestamp: int(round(predictor_f(pd.Timestamp(timestamp).to_datetime64().astype(int))))
    if cache_key:
        CACHE_PREDICTORS[cache_key] = predictor
    return predictor_datetime64(predictor_f)

def predictor_datetime64(predictor_f):
    return lambda timestamp: int(predictor_f(pd.Timestamp(timestamp).to_datetime64().astype(int)))


def predict_price(station_id, timestamp, end_train_timestamp, dir_prices):
    if end_train_timestamp is not None:
        if pd.Timestamp(timestamp) >= pd.Timestamp(end_train_timestamp):
            predictor = get_price_predictor2(station_id, dir_prices, end_train_timestamp=end_train_timestamp)
        else:
            predictor =  get_price_predictor(station_id, dir_prices, end_train_timestamp=end_train_timestamp)
    else:
        predictor = get_price_predictor(station_id, dir_prices, end_train_timestamp=end_train_timestamp)
    return predictor(timestamp)

def evaluate(ts, predictor, begin=TEST_BEGIN_RANGE_TIMESTAMP, end=TEST_END_RANGE_TIMESTAMP):
    orginal_values = ts[begin:end]
    predicted_values = np.array([predictor(dt) for dt in orginal_values.index.values.flat])
    diff = orginal_values.values - predicted_values
    diff = abs(diff)
    return np.average(diff), np.min(diff), np.max(diff)

def test_station(station_id, dir_prices):
    ts = get_station_dataframe(station_id, dir_prices)
    predictor = get_price_predictor(station_id, ts, end_train_timestamp=DEFAULT_END_TRAIN_TIMESTAMP)
    return evaluate(ts, predictor)

def timestamp2int8(timestamp):
    return pd.Timestamp(timestamp).to_datetime64().astype(int)

def save_predictor(station_id, dir_prices):
    ts = get_station_dataframe(station_id, dir_prices)
    predictor = get_price_predictor(station_id, ts)
    instance_predictor = Predictor(full_predictor=predictor, full_converter=timestamp2int8)
    print instance_predictor('2015-01-01')
    PATH = "resources/predictors"
    filename = os.path.join(PATH, str(station_id) + ".p")
    with open(filename, "w") as out_f:
        pickle.dump(instance_predictor, out_f)
        
if __name__ == "__main__":
    for i in [1,3,77]:
        print (i, test_station(i, utils.PATH_EINGABEDATEN))
