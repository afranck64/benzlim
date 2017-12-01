

import cPickle as pickle
import os
import warnings

import pandas as pd
import numpy as np
import dateutil

from ..dao import CSVDAO, StationDAO
from .classification import Classifier


TIME_SPLITS = ['%02.d:00' % h for h in range(24)]

warnings.simplefilter('ignore', np.RankWarning)

CACHE_PREDICTORS = {}

def _to_hour(hour_stamp):
    hour, minute = hour_stamp.split(":")
    return float(hour) + float(minute)/60.0

def get_time_range(timestamp):
    timestamp = pd.Timestamp(timestamp)
    hour_ref = timestamp.hour + timestamp.minute/60.0
    begin = None
    end = None

    if hour_ref < _to_hour(TIME_SPLITS[0]):
        begin = TIME_SPLITS[0]
        end = TIME_SPLITS[-1]
    else:
        for idh, hour_stamp in enumerate(TIME_SPLITS[1:]):
            hour = _to_hour(hour_stamp)
            if hour_ref > _to_hour(hour_stamp):
                begin = TIME_SPLITS[idh]
                end = TIME_SPLITS[(idh+1)%len(TIME_SPLITS)]
            else:
                begin = TIME_SPLITS[idh]
                end = TIME_SPLITS[(idh+1)%len(TIME_SPLITS)]
                break
    assert begin!=end
    return begin, end




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

    def predict(self, timestamp):
        """Return the predicted price at the timestamp <dt>
        timestamp: <str|pd.Timestamp|np.datetime64|datetime> the timestamp"""
        if self.full_predictor is not None:
            if self.full_converter is not None:
                return self.full_predictor(self.full_converter(timestamp))
            return self.full_predictor(timestamp)
        res_price = 0
        dt = pd.Timestamp(timestamp)
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

    def __call__(self, timestamp):
        """callable interface to the predict method"""
        return self.predict(timestamp)


def get_station_dataframe(station_id, dir_prices, datetime_parser=None):
    """return a DataFrame containing timestamps and prices of the station <station_id>"""
    datetime_parser = datetime_parser or dateutil.parser.parse
    station_fic = CSVDAO.get_station_filename(station_id, dir_prices)
    ts = pd.read_csv(station_fic, index_col='timestamp', delimiter=";", header=None, names=["timestamp", "price"], parse_dates=True)
    return ts

def get_freq_avg(ts, freq="10T", fill_method='pad', fill_method2=None):
    if fill_method2 is not None:
        return ts.resample(freq, fill_method=fill_method).fillna(fill_method2)    
    return ts.resample(freq, fill_method=fill_method)

def get_time(timestamp, field=None):
    """return the corresponding value of the attribut corresponding to <field>
    timestamp: <pd.Timestamp>
    field: <str> Y, M, W, D, H, T"""
    field = field or "T"
    if field == "T":
        return timestamp.minute
    elif field == "H":
        return timestamp.hour
    elif field == "D":
        return timestamp.weekday()
    elif field == "W":
        return timestamp.week
    elif field == "M":
        return timestamp.month
    elif field == "Y":
        return timestamp.year
    return -1

def get_price_predictor(station_id, dir_prices, ts=None, time_begin=None, time_end=None, end_train_timestamp=None, poly_deg=3):
    """Generate a price predictor for gas station <station_id> of the timeserie <ts>,
    station_id: str, the id of the station
    ts: DataFrame|Serie, the price's timeserie of as gas station
    time_begin: str,
    time_end: str,
    end_train_timestamp: str, the last usable timestamp for learning,
    poly_deg: int, the degree of polynomial approximation [1,2,3,4,5]
    return the callable prediction(timestamp)

    if station_id is submitted, the predictor is cached resp. recovered from the cache"""
    if time_begin is None or time_end is None:
        time_begin = "00:00"
        time_end = "23:59"
    if station_id is not None:
        cache_key = (station_id, end_train_timestamp, time_begin, time_end, poly_deg, 1)
    if cache_key in CACHE_PREDICTORS:
        #TODO data gathered from cache
        return CACHE_PREDICTORS[cache_key]
    ts = ts if ts is not None else get_station_dataframe(station_id, dir_prices)
    if end_train_timestamp is not None:
        ts = ts[:end_train_timestamp]
    ts_range = ts.between_time(time_begin, time_end)

    coef = 4
    NB_YEARS = 2 * coef
    NB_MONTHS = 12 * coef
    NB_WEEKS = 4 * coef
    NB_DAYS = 7 * coef
    NB_HOURS = 24 * coef
    NB_MINUTES = 60 * coef

    if ts_range.size < NB_YEARS * NB_MONTHS * NB_WEEKS * NB_DAYS * NB_MINUTES:
        ts = get_freq_avg(ts).between_time(time_begin, time_end)
    else:
        ts = ts_range
    year_avg_predictor = None
    month_rel_predictor = None
    week_rel_predictor = None
    day_rel_predictor = None
    hour_rel_predictor = None
    min_rel_predictor = None
    ts_year = get_freq_avg(ts, 'A').tail(NB_YEARS).fillna('pad')
    ts_month = get_freq_avg(ts, 'M').tail(NB_MONTHS).fillna('pad')
    ts_week = get_freq_avg(ts, 'W').tail(NB_WEEKS).fillna('pad')
    ts_day = get_freq_avg(ts, 'D').tail(NB_DAYS).fillna('pad')
    ts_hour = get_freq_avg(ts, 'H').tail(NB_HOURS).fillna('pad')
    ts_min = get_freq_avg(ts, 'T').tail(NB_MINUTES).fillna('pad')
    for ts_x in (ts_year, ts_month, ts_week, ts_day, ts_hour, ts_min):
        pass
    
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
    #if cache_key:
    #    CACHE_PREDICTORS[cache_key] = predictor
    return predictor


def get_price_predictor2(station_id, dir_prices, ts=None, time_begin=None, time_end=None, end_train_timestamp=None, poly_deg=2):
    """Generate a price predictor for gas station <station_id> of the timeserie <ts>,
    station_id: str, the id of the station
    ts: DataFrame|Series, the price's timeserie of as gas station
    end_train_timestamp: str, the last usable timestamp for learning,
    poly_deg: int, the degree of polynomial approximation
    return the predictor as a numpy.poly1d

    if station_id is submitted, the predictor is cached resp. recovered from the cache"""
    cache_key = None
    if time_begin is None or time_end is None:
        time_begin = "00:00"
        time_end = "23:59"
    if station_id is not None:
        cache_key = (station_id, end_train_timestamp, time_begin, time_end, poly_deg, 2)
    if cache_key in CACHE_PREDICTORS:
        print "From cache"
        return CACHE_PREDICTORS[cache_key]
    ts = ts if ts is not None else get_station_dataframe(station_id, dir_prices)
    ts = ts.between_time(time_begin, time_end)
    if end_train_timestamp is not None:
        ts = ts[:end_train_timestamp]
    predictor_f = np.poly1d(np.polyfit(ts.index.values.astype(int).flat, ts.values.flat, poly_deg))
    predictor = lambda timestamp: int(round(predictor_f(pd.Timestamp(timestamp).to_datetime64().astype(int))))
    if cache_key:
        CACHE_PREDICTORS[cache_key] = predictor
    return predictor_datetime64(predictor_f)

def predictor_ymwdhm(y_pred, m_pred, w_pred, d_pred, h_pred, t_pred):
    return lambda timestamp: y_pred(get_time(timestamp, 'Y'))\
                + m_pred(get_time(timestamp, 'M'))\
                + w_pred(get_time(timestamp, 'W'))\
                + d_pred(get_time(timestamp, 'D'))\
                + h_pred(get_time(timestamp, 'H'))\
                + t_pred(get_time(timestamp, 'T'))

def predictor_datetime64(predictor_f):
    return lambda timestamp: int(predictor_f(pd.Timestamp(timestamp).to_datetime64().astype(int)))


def predict_price(station_id, timestamp, end_train_timestamp, dir_prices):
    time_begin, time_end = get_time_range(timestamp)
    usable_station_id = Classifier.station_id2id(station_id, end_train_timestamp)
    if end_train_timestamp is not None:
        if False and pd.Timestamp(timestamp) >= pd.Timestamp(end_train_timestamp):
            predictor = get_price_predictor2(usable_station_id, dir_prices, time_begin=time_begin, time_end=time_end, end_train_timestamp=end_train_timestamp)
        else:
            predictor =  get_price_predictor(usable_station_id, dir_prices, time_begin=time_begin, time_end=time_end, end_train_timestamp=end_train_timestamp)
    else:
        predictor = get_price_predictor(usable_station_id, dir_prices, time_begin=time_begin, time_end=time_end, end_train_timestamp=end_train_timestamp)
    return predictor(timestamp)

def evaluate(ts, predictor, begin=None, end=None):
    orginal_values = ts[begin:end]
    predicted_values = np.array([predictor(dt) for dt in orginal_values.index.values.flat])
    diff = orginal_values.values - predicted_values
    diff = abs(diff)
    return np.average(diff), np.min(diff), np.max(diff)

def test_station(station_id, dir_prices):
    ts = get_station_dataframe(station_id, dir_prices)
    predictor = get_price_predictor(station_id, ts, end_train_timestamp=None)
    return evaluate(ts, predictor)

def timestamp2int8(timestamp):
    return pd.Timestamp(timestamp).to_datetime64().astype(int)

def save_predictor(station_id, dir_prices):
    ts = get_station_dataframe(station_id, dir_prices)
    predictor = get_price_predictor(station_id, ts)
    instance_predictor = Predictor(full_predictor=predictor, full_converter=timestamp2int8)
    PATH = "resources/predictors"
    filename = os.path.join(PATH, str(station_id) + ".p")
    with open(filename, "w") as out_f:
        pickle.dump(instance_predictor, out_f)
        
if __name__ == "__main__":
    pass
