# -- coding: utf-8 --
import glob
import os.path
import csv
import datetime
import dateutil.parser
import codecs

from .b_exceptions import (PriceNotFoundException, StationNotFoundException)

SRC_DIR = os.path.abspath(os.path.join(os.path.split(__file__)[0], '.'))

PATH_EINGABEDATEN = os.path.abspath("../InformatiCup2018/Eingabedaten")
PATH_AUSGABEDATEN = os.path.abspath("../InformatiCup2018/Ausgabedaten")
PATH_OUTPUT = os.path.abspath("../out")
PATH_BENZINPREISE = "../InformatiCup2018/Eingabedaten/Benzinpreise"
FILENAME_TANKSTELLEN = "../InformatiCup2018/Eingabedaten/Tankstellen.csv"
TEST_STATION_ID = 1
DATE_BEGIN = datetime.datetime(2013, 6, 8)
DATE_END = datetime.datetime(2017, 9, 21)

MAX_STATIONS = 100000

STDEV_STEP = 1      #10
AVG_PRICE_STEP = 1  #50
UPDATE_INTERVAL_STEP = 1    #900


def str2latitute(value):
    if "." not in value:
        value = value[:2] + "." + value[2:]
    return float(value) 

def str2longitude(value):
    if "." not in value:
        value = value[:2] + "." + value[2:]
    return float(value)

def str2mark(value):
    return value.lower().decode('utf8')

def str2town(value):
    return value.lower().decode('utf8')

def str2zipcode(value):
    try:
        return int(value)
    except ValueError as err:
        print (err)
        return 0

def str2unicode(value):
    return value.decode('utf8')

def get_stations_infos(filename=FILENAME_TANKSTELLEN, max_stations=MAX_STATIONS):
    """return station informations:
    id: int => Station id
    name: str => Station name
    mark: str => Mark name
    street: str => streetname
    street-number: int => house number/ street number
    zipcode: int => zipcode
    town: str
    latitude: float
    longitude: float"""
    types = [int, str, str, str, str, str, str, float, float]
    #defaults = [0, '', '', '', '', '', '']

    type_infos = [
        [int, 0],
        [str2unicode, ''],
        [str2mark, ''],
        [str2unicode, ''],
        [str2unicode, ''],
        [str2zipcode, 0],
        [str2town, ''],
        [str2latitute, 0],
        [str2longitude, 0]
    ]
    with codecs.open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, dialect=None, delimiter=';')
        for cpt, row in enumerate(reader):
            yield [type_infos[index][0](value.strip() or type_infos[index][1]) for index, value in enumerate(row)]
            if (cpt+1 >= max_stations):
                return

def export_extended_stations_infos(filename=FILENAME_TANKSTELLEN, output_filename=None):
    """export stations informations, adding the fields 'avg_updates_per_day' 'avg_update_interval_in_secs'"""
    output_filename = output_filename or os.path.join(PATH_OUTPUT, 'Tankstellen_extended.csv')
    csvfile = open(output_filename, 'wb', 'utf8')
    writer = csv.writer(csvfile, delimiter=';')
    for row in get_stations_infos(filename):
        station_id = row[0]
        infos = get_station_extended_infos(station_id)
        extended_row = list(row)
        extended_row.extend(infos)
        writer.writerow(extended_row)
    csvfile.close()

def get_extended_stations_infos(filename=FILENAME_TANKSTELLEN):
    for row in get_stations_infos(filename):
        station_id = row[0]
        infos = get_station_extended_infos(station_id)
        extended_row = list(row)
        extended_row.extend(infos)
        yield extended_row


def get_station_filename(station_id):
    """return the filename containing prices for the station <station_id>"""
    return os.path.join(PATH_BENZINPREISE, str(station_id) + ".csv")

def get_file_line_count(filename):
    """return the number of lines contained in the file <filename>"""
    lines = 0
    with codecs.open(filename, 'rb', 'utf8') as f:
        buf_size = 1024 * 1024
        read_f = f.read # loop optimization
        buf = read_f(buf_size)
        while buf:
            lines += buf.count('\n')
            buf = read_f(buf_size)
    return lines


def get_station_prices(station_id=TEST_STATION_ID):
    """return the datetime and prices for the station <station_id>"""
    filename = os.path.join(PATH_BENZINPREISE, str(station_id) + ".csv")
    datetime_parse = dateutil.parser.parse
    try:
        with open(filename, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                yield datetime_parse(row[0]), int(row[1])
    except IOError as err:
        print (err.message)
        yield DATE_BEGIN, -1
        yield DATE_END, -1

def get_all_prices(dir_prices=PATH_BENZINPREISE, delimiter=";"):
    all_files = glob.glob(os.path.join(dir_prices, '*.csv'))
    for filename_path in all_files:
        _, filename = os.path.split(filename_path)
        station_id, _ = os.path.splitext(filename)
        with open(filename_path) as f_prices:
            line = f_prices.readline()
            while line:
                timestamp, price = line.split(delimiter)
                yield station_id, timestamp, price
                line = f_prices.readline()

def get_station_extended_infos(station_id=TEST_STATION_ID):
    """return the average updates for the station <station_id>,
    <avg_daily_updates>, <avg_update_interval_in_secs>, <avg_price>, <stdev_price>"""
    
    start_date = None
    last_processed_date = None
    n = 0
    now = datetime.datetime.now()
    avg_update_time = now - now
    sum_price = 0
    sum_price_sqr = 0
    for processed_date, price in get_station_prices(station_id):
        avg_update_time += (processed_date) - (last_processed_date or processed_date)
        start_date = start_date or processed_date
        last_processed_date = processed_date
        sum_price += price
        sum_price_sqr += price*price
        n += 1
    avg_price = sum_price/n
    stdev_price = ((sum_price_sqr/n) - (avg_price*avg_price))**0.5
    stdev_price -= stdev_price % STDEV_STEP
    stdev_price = int(stdev_price)
    avg_price -= avg_price % AVG_PRICE_STEP
    avg_update_interval_in_secs = int(avg_update_time.total_seconds()/n)
    avg_update_interval_in_secs -= avg_update_interval_in_secs % UPDATE_INTERVAL_STEP
    delta_date = (last_processed_date - start_date)
    avg_daily_updates = int(round(n*1.0/delta_date.days)) if delta_date.days else 0
    return avg_daily_updates, avg_update_interval_in_secs, avg_price, stdev_price

def get_route_params(filename):
    """return <capacity>, [<timestamp>, <station_id>]"""
    with codecs.open(filename, 'r') as input_f:
        capacity = int(input_f.readline())
        reader = csv.reader(input_f, dialect=None, delimiter=';')
        return capacity, tuple(row for row in reader)

if __name__ == "__main__":
    #export_extended_stations_infos()
    #infos = tuple(get_extended_stations_infos())
    #import json
    #with open("resources/ext_stations.json", "w") as out_json:
    #    json.dump(infos, out_json)
    pass