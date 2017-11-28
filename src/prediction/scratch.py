import pandas as pd
import numpy as np
import dateutil
import datetime
import math
from matplotlib import pyplot as plot
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline

from .db import DBManager
from .. import utils

datetime_parser = dateutil.parser.parse

STATION_ID = 4

def interpolate_delta(df, inplace=False):
    if not inplace:
        df = df.copy()
    ind = df.index
    #df.index = df.index.total_seconds()
    df.interpolate(method="time", inplace=True)
    df.index = ind
    return df

def demo():
    station_fic = utils.get_station_filename(STATION_ID)

    ts = pd.read_csv(station_fic, index_col='timestamp', delimiter=";", date_parser=datetime_parser, header=None, names=["timestamp", "price"], parse_dates='timestamp')
    #ts_log = np.log(ts)
    #month_avgs = []
    #ts_log_diff = ts_log - ts_log.shift()
    #moving_avg = pd.rolling_mean(ts_log, 12)
    #expwighted_avg = pd.ewma(ts_log, halflife=12)
    #plot.plot(ts['2015-04':'2015-04-28'])
    print ts.index.values[-1]
    print ts.groupby(['price'])
    return
    order = 3
    #xi = ts.index.values
    #yi = ts.values
    #s = InterpolatedUnivariateSpline(xi, yi, k=order)
    #plot.plot(xi, s(xi))
    plot.plot(ts)
    plot.plot(interpolate_delta(ts['2015-01':'2016-12']))
    #plot.plot(moving_avg, color='red')
    #plot.plot(ts_log_diff, color='yellow')
    plot.show()

demo()

# given values
xi = np.array([i/10.0 for i in xrange(-60, 60)])
#yi = np.array([0.3, -0.1, 0.2, 0.1])
yi = np.array([math.cos(x_i) for x_i in xi])
# positions to inter/extrapolate
x = np.linspace(-50, 50, 100)
# spline order: 1 linear, 2 quadratic, 3 cubic ... 
order = 3
# do inter/extrapolation
s = InterpolatedUnivariateSpline(xi, yi, k=order)
y = s(x)

# example showing the interpolation for linear, quadratic and cubic interpolation
plt.figure()
plt.plot(xi, yi)
"""
for order in range(1, 4):
    s = InterpolatedUnivariateSpline(xi, yi, k=order)
    y = s(x)
    plt.plot(x, y, label="F_%s"%order)
"""
#plt.show()

#res = utils.get_station_prices(STATION_ID) 
WINDOW = 50
#res = tuple(res)[:100+WINDOW]

def prices_to_MWDH(time_prices):
    last_timestamp = time_prices.last(1)
    first_timestamp = time_prices.head(1)
    month = 0

if __name__ == "__main__":
    #DBManager.init_db()
    #DBManager.populate_db(utils.get_all_prices(), DBManager.sql_insert_price)
    #DBManager.populate_db(utils.get_extended_stations_infos())
    #result = DBManager.execute("select * from stations")
    #print len(result)python db
    #infos =  StationDAO.getAll()
    #infos =  [{info[0]: info} for info in infos]
    #import ujson as json
    #import simplejson as json
    #infos = {}
    #with open("resources/ext_stations.json", "r") as in_json:
    #    #infos = json.load(in_json)
    #    infos = json.load(in_json)
    #with open("resources/ext_stations.json", "w") as out_json:
    #    json.dump(infos, out_json)
    #print len(infos)
    #for i in range(32):
    #res = DBManager.execute("select id, datetime(timestamp || ':00'), price from prices where station_id=1")
    #print len(res)
    """
    STATION_ID = 9
    res = utils.get_station_prices(STATION_ID) 
    WINDOW = 50
    res = tuple(res)[:100+WINDOW]
    avg_abs_err = 0.0
    pow_fact = 1.5
    for id_, time_price in enumerate(res[WINDOW:]):
        vals = (res[id_:id_+WINDOW])
        avg = sum(v[1]*(i+1)**pow_fact for i,v in enumerate(vals))
        avg /= 1.0*sum(i**pow_fact for i in range(1,WINDOW+1))
        
        #avg = sum(v[1] for v in vals)
        #avg /= len(vals)
        print avg - time_price[1], dir(time_price[0])
        avg_abs_err += abs(avg - time_price[1])**2
    print "AVG_ABS_ERR: ", avg_abs_err/len(res)
    """
    #pass