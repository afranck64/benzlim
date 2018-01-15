import logging
import os
import warnings

import pandas as pd
import numpy as np
import dateutil

from ..compat import printf, pickle
from ..config import Configuration
from ..exceptions_ import (BadFormatException, BadValueException)
from ..dao import CSVDAO, StationDAO
from .classification import Classifier


warnings.simplefilter('ignore', np.RankWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)

CACHE_PREDICTORS = {}

def _to_hour(hour_stamp):
    hour, minute = hour_stamp.split(":")
    return float(hour) + float(minute)/60.0

def get_time_range(timestamp):
    time_bins = Configuration.get_instance().TIME_BINS
    timestamp = pd.Timestamp(timestamp)
    hour_ref = timestamp.hour + timestamp.minute/60.0
    begin = None
    end = None

    if hour_ref < _to_hour(time_bins[0]):
        begin = time_bins[0]
        end = time_bins[-1]
    else:
        for idh, hour_stamp in enumerate(time_bins[1:]):
            hour = _to_hour(hour_stamp)
            if hour_ref > _to_hour(hour_stamp):
                begin = time_bins[idh]
                end = time_bins[(idh+1)%len(time_bins)]
            else:
                begin = time_bins[idh]
                end = time_bins[(idh+1)%len(time_bins)]
                break
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

def get_freq_avg(ts, freq="10T", fill_method='pad', fill_method2=None):
    """resample the timeserie with the new frequence <freq> using the fill methods for NANs"""
    #"""
    res = ts.resample(freq)
    if fill_method == "pad":
        res = res.pad()
    elif fill_method == "ffill":
        res = res.ffill()
    elif fill_method == "bfill":
        res = res.bfill()

    if fill_method2 is not None:
        res = res.resample(freq)

    if fill_method2=="pad":
        res = res.pad()
    elif fill_method2 == "ffill":
        res = res.ffill()
    elif fill_method2 == "bfill":
        res = res.bfill()

    return res
    #In Deprecation
    """
    if fill_method2 is not None:
        return ts.resample(freq, fill_method=fill_method).fillna(fill_method2)    
    return ts.resample(freq, fill_method=fill_method)#"""

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

def get_price_predictor(station_id, dir_prices, ts=None, time_begin=None, time_end=None, end_train_timestamp=None, poly_deg=2):
    """Generate a price predictor for gas station <station_id> of the timeserie <ts>,
    station_id: str, the id of the station
    ts: DataFrame|Serie, the price's timeserie of as gas station
    time_begin: str,
    time_end: str,
    end_train_timestamp: str, the last usable timestamp for learning,
    poly_deg: int, the degree of polynomial approximation [1,2,3,4,5]
    return the callable prediction(timestamp)

    if station_id is submitted, the predictor is cached resp. recovered from the cache if available
    
    If the difference between the predicted value and the average is bigger than 20% of the average,
    the predictor will return the average instead of the predicted value"""
    if time_begin is None or time_end is None:
        time_begin = "00:00"
        time_end = "23:59"
    cache_key = None
    if station_id is not None:
        cache_key = (station_id, end_train_timestamp, time_begin, time_end, poly_deg, 1)
        if cache_key in CACHE_PREDICTORS:
                #TODO data gathered from cache
            return CACHE_PREDICTORS[cache_key]
    SIZE_MIN = 4
    ts = ts if ts is not None else CSVDAO.get_station_dataframe(station_id, dir_prices)
    ts_trimmed = ts[:end_train_timestamp].dropna()
    if end_train_timestamp is not None and ts_trimmed.size >= 1:
        ts = ts_trimmed
    ts_range = ts.between_time(time_begin, time_end)
    coef = 2
    NB_YEARS = 4
    NB_MONTHS = 12 * coef
    NB_WEEKS = 4 * coef
    NB_DAYS = 7 * coef
    NB_HOURS = 24 * coef
    NB_MINUTES = 60 * coef
    
    if ts_range.size >= SIZE_MIN:
        ts = ts_range
    
    if ts.size == 1:
        price = ts.values.flat[0]
        return lambda timestamp: (price, 0.0)

    year_avg_predictor = None
    month_rel_predictor = None
    week_rel_predictor = None
    day_rel_predictor = None
    hour_rel_predictor = None
    min_rel_predictor = None

    #print "TS: ", ts.groupby(pd.TimeGrouper("M"))
    ts = ts.resample("30T", level=0).dropna()
    ts_year = get_freq_avg(ts.drop_duplicates(), 'Y').tail(NB_YEARS).fillna(method='bfill')
    ts_month = get_freq_avg(ts, 'M').tail(NB_MONTHS).fillna(method='bfill').fillna(ts_year.values.flat[-1])
    ts_week = get_freq_avg(ts, 'W').tail(NB_WEEKS).fillna(method='bfill').fillna(ts_month.values.flat[-1])
    ts_day = get_freq_avg(ts, 'D').tail(NB_DAYS).fillna(method='bfill').fillna(ts_week.values.flat[-1])
    ts_hour = get_freq_avg(ts, 'H').tail(NB_HOURS).fillna(method='bfill').fillna(ts_day.values.flat[-1])
    ts_min = get_freq_avg(ts, 'T').tail(NB_MINUTES).fillna(method='bfill').fillna(ts_hour.values.flat[-1])

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
    
    avg = int(ts_min.tail(1).mean().values.flat[0])
    if ts.size > 1:
        stddev = ts.dropna().std().values.flat[0]
    else:
        stddev = 1
    def predictor_full(timestamp):
        margin_coef = 0.20
        timestamp = pd.Timestamp(timestamp)
        res = year_avg_predictor(get_time(timestamp, 'Y'))\
                + month_rel_predictor(get_time(timestamp, 'M'))\
                + week_rel_predictor(get_time(timestamp, 'W'))\
                + day_rel_predictor(get_time(timestamp, 'D'))\
                + hour_rel_predictor(get_time(timestamp, 'H'))\
                + min_rel_predictor(get_time(timestamp, 'T'))
        res = int(round(res))
        if avg is not None and abs(res - avg) >avg*margin_coef:
            return avg, stddev/avg
        else:
            return res, stddev/avg
    if cache_key and Configuration.get_instance().enabled_cache:
        CACHE_PREDICTORS[cache_key] = predictor_full
    return predictor_full


def get_price_predictor2(station_id, dir_prices, ts=None, time_begin=None, time_end=None, end_train_timestamp=None, poly_deg=2):
    """Generate a price predictor for gas station <station_id> of the timeserie <ts>,
    station_id: str, the id of the station
    ts: DataFrame|Series, the price's timeserie of as gas station
    end_train_timestamp: str, the last usable timestamp for learning,
    poly_deg: int, the degree of polynomial approximation
    return the predictor as a numpy.poly1d

    if station_id is submitted, the predictor is cached resp. recovered from the cache

    If the difference between the predicted value and the average is bigger than 20% of the average,
    the predictor will return the average instead of the predicted value"""
    cache_key = None
    if time_begin is None or time_end is None:
        time_begin = "00:00"
        time_end = "23:59"
    if station_id is not None:
        cache_key = (station_id, end_train_timestamp, time_begin, time_end, poly_deg, 2)
    if cache_key in CACHE_PREDICTORS:
        logging.info("Retrieved from cache: %s" % str(cache_key))
        return CACHE_PREDICTORS[cache_key]
    ts = ts if ts is not None else CSVDAO.get_station_dataframe(station_id, dir_prices)
    try:
        pass
        ts = get_freq_avg(ts, "30T")
    except ValueError:
        pass
    SIZE_MIN = 4
    MAX_SAMPLES = 256
    if end_train_timestamp is not None:
        ts_trimmed = ts[:end_train_timestamp].bfill()
        if ts_trimmed.size >= 0:
            ts = ts_trimmed
    ts_between = ts.between_time(time_begin, time_end)
    if ts_between.size >= SIZE_MIN:
        ts = ts_between
    
    ts = ts.tail(MAX_SAMPLES)
    ts = ts.dropna()
    if ts.size == 1:
        price = ts.values.flat[0]
        return lambda x: (price, 1)
    avg = int(ts.dropna().mean())
    stddev = ts.dropna().std().values.flat[0]
    predictor_f = np.poly1d(np.polyfit(ts.index.values.astype(int).flat, ts.values.flat, poly_deg))
    

    def predictor_full(timestamp):
        margin_coef = 0.2
        res = int(predictor_f(pd.Timestamp(timestamp).to_datetime64().astype(int)))
        if abs(res-avg) > avg*margin_coef:
            return avg, stddev/avg
        else:
            return res, stddev/avg
    if cache_key and Configuration.get_instance().enabled_cache:
        CACHE_PREDICTORS[cache_key] = predictor_full
    return predictor_full


def predict_price(station_id, timestamp, end_train_timestamp, dir_prices, bench_ts=None):
    try:
        time_begin, time_end = get_time_range(timestamp)
        if bench_ts is None:
            usable_station_id = Classifier.station_id2id(station_id, end_train_timestamp)
            if str(station_id) != str(usable_station_id):
                logging.info("station_id: %s ===>> %s" %(station_id, usable_station_id))
            ts = CSVDAO.get_station_dataframe(usable_station_id, dir_prices)
        else:
            ts = bench_ts
            usable_station_id = None
        predictor = get_price_predictor(usable_station_id, dir_prices, ts, time_begin=time_begin, time_end=time_end, end_train_timestamp=end_train_timestamp)
        predictor2 = get_price_predictor2(usable_station_id, dir_prices, ts, time_begin=time_begin, time_end=time_end, end_train_timestamp=end_train_timestamp)
        pred1, coef1 = predictor(timestamp)
        pred2, coef2 = predictor2(timestamp)
        coef1 = 1-coef1
        coef2 = 1-coef2
        #print int((pred1*coef1 + pred2*coef2)/(coef1+coef2)), (pred1+pred2)/2
        return int((pred1*coef1 + pred2*coef2)/(coef1+coef2))
        #return (pred1+pred2)/2
    #except TypeError as err:
    #    raise BadValueException(err)
    except ValueError as err:
        logging.debug(err)
        raise BadValueException("Not enough values")
    except pd.errors.OutOfBoundsDatetime as err:
        raise BadValueException(err)

def timestamp2int8(timestamp):
    return pd.Timestamp(timestamp).to_datetime64().astype(int)

def save_predictor(station_id, dir_prices):
    ts = CSVDAO.get_station_dataframe(station_id, dir_prices)
    predictor = get_price_predictor(station_id, ts)
    instance_predictor = Predictor(full_predictor=predictor, full_converter=timestamp2int8)
    PATH = "resources/predictors"
    filename = os.path.join(PATH, str(station_id) + ".pred")
    with open(filename, "w") as out_f:
        pickle.dump(instance_predictor, out_f)
        
if __name__ == "__main__":
    pass
