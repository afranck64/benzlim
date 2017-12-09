"""csv_.py - read/write/investigate csv related files"""
# -- coding: utf-8 --
import glob
import os.path
import csv
import datetime
import dateutil.parser
import codecs

from ..b_exceptions import (PriceNotFoundException, StationNotFoundException, BadFormatException)
from ..config import Configuration
from ..utils import (str2latitute, str2longitude, str2mark, str2town,
                     str2unicode, str2zipcode)


class CSVDAO(object):    
    @classmethod
    def get_station_filename(cls, station_id, prices_dir=None):
        """return the filename containing prices for the station <station_id>"""
        prices_dir = prices_dir or Configuration.get_instance().prices_dir
        return os.path.join(prices_dir, str(station_id) + ".csv")
    
    @classmethod
    def is_prices_available(cls, station_id):
        """return True if prices are avaiable for the given station else False"""
        filename = cls.get_station_filename(station_id)
        return os.path.exists(filename)
    
    @classmethod
    def get_all_extended_stations_infos(cls):
        """return station informations:
        id: int => Station id
        name: str => Station name
        mark: str => Mark name
        street: str => streetname
        street-number: int => house number/ street number
        zipcode: int => zipcode
        town: str
        latitude: float
        longitude: float
        prices_available: bool => if prices are available
        begin_timestamp: str => the first price timestamp"""
        for station_row in cls.get_all_stations_infos():
            yield cls._get_extended_station_infos(station_row)

    @classmethod
    def get_all_stations_infos(cls):
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
        with codecs.open(Configuration.get_instance().stations_file, 'r') as csvfile:
            reader = csv.reader(csvfile, dialect=None, delimiter=';')
            for _, row in enumerate(reader):
                yield [type_infos[index][0](value.strip() or type_infos[index][1]) for index, value in enumerate(row)]

    @classmethod
    def _get_begin_timestamp(cls, station_id):
        """return the first timestamp for the given station"""
        filename = cls.get_station_filename(station_id)
        begin_timestamp = None
        if cls.is_prices_available(station_id):
            with codecs.open(filename, 'r') as csvfile:
                reader = csv.reader(csvfile, dialect=None, delimiter=';')
                first_row = next(reader)
                begin_timestamp = first_row[0]
        return begin_timestamp

    @classmethod
    def _get_extended_station_infos(cls, station_row):
        """return the station informations extended with:
        prices_available: bool => if prices are available
        begin_timestamp: str => the first price timestamp"""
        station_id = station_row[0]
        begin_timestamp = cls._get_begin_timestamp(station_id)
        is_prices_available = begin_timestamp is not None
        sr = station_row
        return sr[0], sr[1], sr[2], sr[3], sr[4], sr[5], sr[6], sr[7], sr[8], is_prices_available, begin_timestamp

    @classmethod
    def get_predict_params(cls, filename):
        """return [<end_timestamp>, <prediction_timestamp>, <station_id>]"""
        try:
            with codecs.open(filename, 'r') as input_f:
                reader = csv.reader(input_f, dialect=None, delimiter=';')
                return tuple((row[0], row[1], row[2]) for row in reader)
        except IndexError:
            raise BadFormatException(filename)
        except ValueError:
            raise BadFormatException(filename)

    @classmethod
    def get_route_params(cls, filename):
        """return <capacity>, [<timestamp>, <station_id>]"""
        try:
            with codecs.open(filename, 'r') as input_f:
                capacity = int(input_f.readline())
                reader = csv.reader(input_f, dialect=None, delimiter=';')
                return capacity, tuple((row[0], row[1]) for row in reader)
        except IndexError:
            raise BadFormatException(filename)
        except ValueError:
            raise BadFormatException(filename)

    @classmethod
    def get_route_as_predict_params(cls, filename):
        capacity, timestamp_stations = cls.get_route_params(filename)
        for timestamp, station_id in timestamp_stations:
            yield None, timestamp, station_id


    @classmethod
    def get_predicted_prices(cls, filename):
        """return [<end_timestamp>, <prediction_timestamp>, <station_id>, <pred_price>]"""
        with codecs.open(filename, 'r') as input_f:
            reader = csv.reader(input_f, dialect=None, delimiter=';')
            return tuple((row[0], row[1], int(row[2]), int(row[3])) for row in reader)

