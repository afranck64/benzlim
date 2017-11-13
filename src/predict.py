import pandas as pd
import numpy as np
import dateutil

import utils

TEST_STATION_ID = 10001
TEST_END_TIMESTAMP = "2017-01-01"
TEST_BEGIN_RANGE_TIMESTAMP = "2017-02-01" #TEST_END_TIMESTAMP
TEST_END_RANGE_TIMESTAMP = "2017-02-28"

CACHE_PREDICTORS = {}

def get_station_dataframe(station_id=TEST_STATION_ID, datetime_parser=None):
    """return a DataFrame containing timestamps and prices of the station <station_id>"""
    datetime_parser = datetime_parser or dateutil.parser.parse
    station_fic = utils.get_station_filename(station_id)
    ts = pd.read_csv(station_fic, index_col='timestamp', delimiter=";", date_parser=datetime_parser, header=None, names=["timestamp", "price"], parse_dates='timestamp')
    return ts

def get_months_avg(ts):
    return ts.resample('M', fill_method='bfill')


def get_weeks_avg(ts):
    return ts.resample('W', fill_method='bfill')


def get_days_avg(ts):
    return ts.resample('D', fill_method='bfill')


def get_weekdays_avg(ts):
    timestamp_begin = ts.index.values[0]
    timestamp_end = ts.index.values[-1]
    day_range = pd.date_range(timestamp_begin, timestamp_end, freq='D')

def get_hours_avg(ts):
    return ts.resample('H', fill_method='bfill')

def get_minutes_avg(ts, nb_mins=30):
    return ts.resample('%sT' % nb_mins, fill_method='bfill')


def get_price_predictor(station_id=None, ts=None, end_timestamp=TEST_END_TIMESTAMP, poly_deg=3):
    """Generate a price predictor for gas station <station_id> of the timeserie <ts>,
    station_id: str, the id of the station
    ts: DataFrame|Series, the price's timeserie of as gas station
    end_timestamp: str, the last usable timestamp for learning,
    poly_deg: int, the degree of polynomial approximation
    return the predictor as a numpy.poly1d

    if station_id is submitted, the predictor is cached resp. recovered from the cache"""
    cache_key = None
    if station_id is not None:
        cache_key = (station_id, end_timestamp, poly_deg)
    if cache_key in CACHE_PREDICTORS:
        return CACHE_PREDICTORS[cache_key]
    ts = ts if ts is not None else get_station_dataframe(station_id)
    if end_timestamp is not None:
        ts = ts[:pd.Timestamp(end_timestamp)]
    predictor = np.poly1d(np.polyfit(ts.index.values.astype(int).flat, ts.values.flat, poly_deg))
    if cache_key:
        CACHE_PREDICTORS[cache_key] = predictor
    return predictor

def predict_price(predictor, timestamp):
    return predictor(pd.Timestamp(timestamp).to_datetime64().astype(int))

def get_diff(ts1, ts2):
    return ts1 - ts2

def get_test_range(ts):
    return ts[TEST_BEGIN_RANGE_TIMESTAMP:TEST_END_RANGE_TIMESTAMP]

def evaluate(ts, predictor, begin=TEST_BEGIN_RANGE_TIMESTAMP, end=TEST_END_RANGE_TIMESTAMP):
    orginal_values = ts[begin:end]
    predicted_values = predictor(orginal_values.index.values.astype(int))
    diff = orginal_values.values - predicted_values
    diff = abs(diff)
    print diff.min(), diff.max()
    return np.average(diff**2)**0.5

def test_station(station_id):
    ts = get_station_dataframe(station_id)
    predictor = get_price_predictor(station_id, ts)
    return evaluate(ts, predictor)

#p = get_price_predictor(TEST_STATION_ID, ts=df)
#print evaluate(df, p)

for i in [1,3,77]:
    print i, test_station(i)

"""
print df.index.values[0]
print p(df.index.values.astype(int).flat[0])
today = pd.Timestamp.utcnow().to_datetime64().astype(int)
friday = pd.Timestamp('2017-11-17 14:15:00').to_datetime64().astype(int)
day = pd.Timestamp('2014-06-08 22:00:00').to_datetime64().astype(int)
print p(today), p(friday), p(day)
print get_test_range(df).index
"""