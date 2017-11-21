import pandas as pd
import numpy as np
from scipy import interpolate
import dateutil

from . import utils

TEST_STATION_ID = 11108
TEST_END_TIMESTAMP = "2015-07-01"
TEST_BEGIN_RANGE_TIMESTAMP = "2015-08-01" #TEST_END_TIMESTAMP
TEST_END_RANGE_TIMESTAMP = "2015-08-03"

CACHE_PREDICTORS = {}

def get_station_dataframe(station_id=TEST_STATION_ID, datetime_parser=None):
    """return a DataFrame containing timestamps and prices of the station <station_id>"""
    datetime_parser = datetime_parser or dateutil.parser.parse
    station_fic = utils.get_station_filename(station_id)
    ts = pd.read_csv(station_fic, index_col='timestamp', delimiter=";", date_parser=datetime_parser, header=None, names=["timestamp", "price"], parse_dates='timestamp')
    return ts

def get_years_avg(ts):
    return ts.resample('AS', fill_method='bfill')

def get_months_avg(ts):
    return ts.resample('M', fill_method='bfill')


def get_weeks_avg(ts):
    return ts.resample('W', fill_method='bfill')


def get_days_avg(ts):
    return ts.resample('D', fill_method='bfill')


def get_weekdays_avg(ts):
    #TODO
    timestamp_begin = ts.index.values[0]
    timestamp_end = ts.index.values[-1]
    day_range = pd.date_range(timestamp_begin, timestamp_end, freq='D')

def get_hours_avg(ts):
    return ts.resample('H', fill_method='bfill')

def get_minutes_avg(ts, nb_mins=1, fill_method='bfill'):
    return ts.resample('%sT' % nb_mins, fill_method=fill_method)

def combine_predict(arg, f):
    pass

def get_time(timestamp, precision=None):
    """return the time in seconds since day 0-0-0
    precision: Y, M, W, D, H, T"""
    #TODO take care of day (month day)
    year = timestamp.year
    month = timestamp.month
    week = timestamp.week
    day = timestamp.weekday()
    hour = timestamp.hour
    m = timestamp.minute
    precision = precision or "T"
    if precision=="T":
        return m
        return year + month/12.0 + week/(4.0*12) + day/(4.0*12*7) + hour/(4.0*12*7*24) + m/(4.0*12*7*24*60)
        #return m*60 + hour*60*60 + day*60*60*24 + week*60*60*24*7 + month*60*60*24*7*4 + year*60*60*24*7*4*12
    elif precision=="H":
        return hour
        return year + month/12.0 + week/(4.0*12) + day/(4.0*12*7) + hour/(4.0*12*7*24)
        #return hour*60*60 + day*60*60*24 + week*60*60*24*7 + month*60*60*24*7*4 + year*60*60*24*7*4*12
    elif precision=="D":
        return day
        return year + month/12.0 + week/(4.0*12) + day/(4.0*12*7)
        #return day*60*60*24 + week*60*60*24*7 + month*60*60*24*7*4 + year*60*60*24*7*4*12
    elif precision=="W":
        return week
        return year + month/12.0 + week/(4.0*12)
        #return week*60*60*24*7 + month*60*60*24*7*4 + year*60*60*24*7*4*12
    elif precision=="M":
        return month
        return month/12.0 + year
        #return month*60*60*24*7*4 + year*60*60*24*7*4*12
    elif precision=="Y":
        return year
        #return year*60*60*24*7*4*12
    return -1

def get_sub_price_predictor(ts, freq, tail, poly_deg=1):
    ts_values = ts.values.flat[-tail:]
    #weight = (0.1/np.arange(ts_values.size+1, 1, -1))**2
    weight = None
    predictor = np.poly1d(np.polyfit(np.array([get_time(dt, freq) for dt in ts.index][-tail:]), ts_values, poly_deg, w=weight))
    return predictor

def get_price_predictor(station_id=None, ts=None, end_timestamp=TEST_END_TIMESTAMP, poly_deg=1):
    ts_avg_month
    ts_avg_week
    ts_avg_day
    ts_avg_hour
    pass

def get_price_predictor(station_id=None, ts=None, end_timestamp=TEST_END_TIMESTAMP, poly_deg=1):
    cache_key = None
    if station_id is not None:
        cache_key = (station_id, end_timestamp, poly_deg)
    if cache_key in CACHE_PREDICTORS:
        print "From cache"
        return CACHE_PREDICTORS[cache_key]
    ts = ts if ts is not None else get_station_dataframe(station_id)
    if end_timestamp is not None:
        ts = ts[:end_timestamp]
    NB_YEARS = 1*2
    NB_MONTHS = 12 * 2
    NB_WEEKS = 4 * 12
    NB_DAYS = 7 * 4
    NB_HOURS = 24 * 7
    NB_MINUTES = 60 * 24
    dtype = np.dtype([('year', int), ('month', int), ('week', int), ('day', int), ('hour', int), ('minute', int)])
    year_avg_predictor = None
    month_rel_predictor = None
    week_rel_predictor = None
    day_rel_predictor = None
    hour_rel_predictor = None
    min_rel_predictor = None
    ts_year = get_years_avg(ts).tail(NB_YEARS)
    ts_month = get_months_avg(ts).tail(NB_MONTHS)
    ts_week = get_weeks_avg(ts).tail(NB_WEEKS)
    ts_day = get_days_avg(ts).tail(NB_DAYS)
    ts_hour = get_hours_avg(ts).tail(NB_HOURS)
    ts_min = get_minutes_avg(ts).tail(NB_MINUTES)
    """
    ts_month_rel = (ts_month).dropna().tail(NB_MONTHS)#.fillna(method='bfill').fillna(method='ffill')
    ts_week_rel = (ts_week - get_weeks_avg(ts_month_rel)).dropna().tail(NB_WEEKS)#.fillna(method='bfill').fillna(method='ffill')
    ts_day_rel = (ts_day - get_days_avg(ts_week-ts_week_rel)).dropna().tail(NB_DAYS)#.fillna(method='bfill').fillna(method='ffill')
    ts_hour_rel = (ts_hour - get_hours_avg(ts_day-ts_day_rel)).dropna().tail(NB_HOURS)#.fillna(method='bfill').fillna(method='ffill')
    """
    #ts_min_rel = (get_min_avg(ts_hour - ts_hour_rel))
    #print ts_hour_rel
    #print ts_hour_rel.abs().mean().values, ts_day_rel.abs().mean().values, ts_week_rel.abs().mean().values, ts_month_rel.abs().mean().values
    #print np.recarray(ts.index.values, dtype=dtype)
    #year_avg_predictor = np.poly1d(np.polyfit(np.array([get_time(dt, 'Y') for dt in ts_year.index]), ts_year.values.flat, poly_deg))
    
    #month_rel_predictor = np.poly1d(np.polyfit(np.array([get_time(dt, 'M') for dt in ts_month_rel.index][-NB_MONTHS:]), ts_month_rel.values.flat[-NB_MONTHS:], poly_deg))
    #week_rel_predictor = np.poly1d(np.polyfit(np.array([get_time(dt, 'W') for dt in ts_week_rel.index][-NB_WEEKS:]), ts_week_rel.values.flat[-NB_WEEKS:], 3))
    #day_rel_predictor = np.poly1d(np.polyfit(np.array([get_time(dt, 'D') for dt in ts_day_rel.index][-NB_DAYS:]), ts_day_rel.values.flat[-NB_DAYS:], 3))
    #hour_rel_predictor = np.poly1d(np.polyfit(np.array([get_time(dt, 'H') for dt in ts_hour_rel.index][-NB_HOURS:]), ts_hour_rel.values.flat[-NB_HOURS:], 3))
    #month_rel_predictor = get_sub_price_predictor(ts_month_rel, 'M', NB_MONTHS, poly_deg)
    #week_rel_predictor = get_sub_price_predictor(ts_week_rel, 'W', NB_DAYS, poly_deg)
    #day_rel_predictor = get_sub_price_predictor(ts_day_rel, 'D', NB_WEEKS, poly_deg)

    year_avg_predictor = np.poly1d(np.polyfit(np.array([get_time(dt, 'Y') for dt in ts_year.index]), ts_year.values.flat, poly_deg))

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
    print ts_min_rel_y
    #hour_rel_predictor = lambda x: 0
    #print ts_hour_rel_y[-1], ts_day_rel_y[-1], ts_week_rel_y[-1], ts_week_rel_y[-1], ts_month_rel_y[-1], ts_year[-1]
    #hour_rel_predictor = get_sub_price_predictor(ts_hour_rel, 'H', NB_HOURS, poly_deg)

    #year_avg_predictor = interpolate.UnivariateSpline(np.array([get_time(dt, 'Y') for dt in ts_year.index]), ts_year.values.flat, poly_deg)
    #month_rel_predictor = interpolate.UnivariateSpline(np.array([get_time(dt, 'M') for dt in ts_month_rel.index][-NB_MONTHS:]), ts_month_rel.values.flat[-NB_MONTHS:], poly_deg)
    #week_rel_predictor = interpolate.UnivariateSpline(np.array([get_time(dt, 'W') for dt in ts_week_rel.index][-NB_WEEKS:]), ts_week_rel.values.flat[-NB_WEEKS:], poly_deg)
    #day_rel_predictor = interpolate.UnivariateSpline(np.array([get_time(dt, 'D') for dt in ts_day_rel.index][-NB_DAYS:]), ts_day_rel.values.flat[-NB_DAYS:], poly_deg)
    #hour_rel_predictor = interpolate.UnivariateSpline(np.array([get_time(dt, 'H') for dt in ts_hour_rel.index][-NB_HOURS:]), ts_hour_rel.values.flat[-NB_HOURS:], poly_deg)
    #print ts_hour_rel_y[-1], ts_day_rel_y[-1], ts_week_rel_y[-1], ts_month[-1]
    def predictor(timestamp):
        timestamp = pd.Timestamp(timestamp)
        res = year_avg_predictor(get_time(timestamp, 'Y'))\
                + month_rel_predictor(get_time(timestamp, 'M'))\
                + week_rel_predictor(get_time(timestamp, 'W'))\
                + day_rel_predictor(get_time(timestamp, 'D'))\
                + hour_rel_predictor(get_time(timestamp, 'H'))\
                + min_rel_predictor(get_time(timestamp, 'T'))\
        #print "HOUR_v:", hour_rel_predictor(get_time(timestamp, 'H'))
        return int(round(res))
    import cPickle as pickle
    with open("out.dump", 'w') as out_f:
        pickle.dump(month_rel_predictor, out_f)
    if cache_key:
        CACHE_PREDICTORS[cache_key] = predictor
    return predictor

def get_price_predictor_tmp(station_id=None, ts=None, end_timestamp=TEST_END_TIMESTAMP, poly_deg=3):
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
        print "From cache"
        return CACHE_PREDICTORS[cache_key]
    ts = ts if ts is not None else get_station_dataframe(station_id)
    if end_timestamp is not None:
        ts = ts[:pd.Timestamp(end_timestamp)]
    predictor_f = np.poly1d(np.polyfit(ts.index.values.astype(int).flat, ts.values.flat, poly_deg))
    def predictor(timestamp):
        timestamp = pd.Timestamp(timestamp)
        return int(round(predictor_f(timestamp.to_datetime64().astype(int))))
    if cache_key:
        CACHE_PREDICTORS[cache_key] = predictor
    return predictor

#def predict_price(predictor, timestamp):
#    return predictor(pd.Timestamp(timestamp).to_datetime64().astype(int))

def predict_price(station_id, timestamp, end_timestamp=None, debug=False):
    if debug:
        ts = get_station_dataframe(station_id)
        predictor = get_price_predictor(station_id, ts, end_timestamp)
        res = int(round(predictor(pd.Timestamp(timestamp).to_datetime64().astype(int))))
        return res, ts[timestamp.split()[0]].values[0], res-ts[timestamp.split()[0]].values[0], "#%s items" % len(ts)
    else:
        predictor = get_price_predictor(station_id, end_timestamp=end_timestamp)
        return predictor(timestamp)

def get_test_range(ts):
    return ts[TEST_BEGIN_RANGE_TIMESTAMP:TEST_END_RANGE_TIMESTAMP]

def evaluate(ts, predictor, begin=TEST_BEGIN_RANGE_TIMESTAMP, end=TEST_END_RANGE_TIMESTAMP):
    orginal_values = ts[begin:end]
    predicted_values = predictor(orginal_values.index.values.astype(int))
    diff = orginal_values.values - predicted_values
    diff = abs(diff)
    #print (diff.min(), diff.max())
    return np.average(diff**2)**0.5

def test_station(station_id):
    ts = get_station_dataframe(station_id)
    predictor = get_price_predictor(station_id, ts)
    return evaluate(ts, predictor)

#p = get_price_predictor(TEST_STATION_ID, ts=df)
#print evaluate(df, p)

if __name__ == "__main__":
    for i in [1,3,77]:
        print (i, test_station(i))

"""
print df.index.values[0]
print p(df.index.values.astype(int).flat[0])
today = pd.Timestamp.utcnow().to_datetime64().astype(int)
friday = pd.Timestamp('2017-11-17 14:15:00').to_datetime64().astype(int)
day = pd.Timestamp('2014-06-08 22:00:00').to_datetime64().astype(int)
print p(today), p(friday), p(day)
print get_test_range(df).index
"""