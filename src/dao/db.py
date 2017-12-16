# -- coding: utf-8 --

"""db.py - access station related informations"""

import sqlite3
import os

from .. import utils
from ..compat import printf
from ..config import Configuration

__all__ = ["DBManager", "StationDAO"]

DB_PATH = "resources/db/db.sqlite3"

# id: the station id
# name: the station name
# mark: the startion mark
# street: the streetname
# street_number: the street number
# zipcode: the postal zipcode
# place: the place/region
# latitude: the number of positive matches during training
# longitude: the number of negative matches during training
# prices_available: boolean if prices are available for this station
# begin_timestamp: timestamp of the first price
DB_SQL_SCHEMA_STATIONS = """
CREATE TABLE IF NOT EXISTS stations(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    mark TEXT NOT NULL,
    street TEXT NOT NULL,
    street_number INT NOT NULL,
    zipcode INT NOT NULL,
    place TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    prices_available BOOLEAN NOT NULL,
    begin_timestamp TEXT NULL
);"""


DB_SQL_INDEX_PRICES_AVAILABLE = "CREATE INDEX IF NOT EXISTS mark_index on stations(mark COLLATE NOCASE);"
DB_SQL_INDEX_TIMESTAMP = "CREATE INDEX IF NOT EXISTS place_index on stations(place COLLATE NOCASE);"


def icompare(text1, text2):
    return (u"%s" % text1).lower() == (u"%s" % text2).lower()


class DBManager(object):
    sql_schemas = (DB_SQL_SCHEMA_STATIONS, )
    sql_indexes = (DB_SQL_INDEX_PRICES_AVAILABLE, DB_SQL_INDEX_TIMESTAMP,)
    conn = None
    table = "stations"
    table_stations = "stations"
    sql_insert_station_sql = "insert into %s (id, name, mark, street, street_number, zipcode, place, latitude, longitude, prices_available, begin_timestamp) "\
            "values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);" % table_stations
    sql_get = ""
    sql_update = ""
    sql_delete = ""
    sql_save = ""
    _auto_commit = True

    @classmethod
    def open(cls):
        if cls.conn:
            return
        filename = Configuration.get_instance().database_file
        cls.conn = sqlite3.connect(filename)
        cls.conn.create_function("icompare", 2, icompare)

    @classmethod
    def get_conn(cls):
        if cls.conn is None:
            cls.open()
        tmp_conn = cls.conn
        cls.conn = None
        return tmp_conn

    @classmethod
    def close(cls):
        if cls.conn:
            cls.conn.commit()
            cls.conn.close()
            cls.conn = None

    @classmethod
    def init_db(cls):
        """Init the database if it doesn't exist yet."""
        filename = Configuration.get_instance().database_file
        utils.create_file_dirs(filename)
        if not os.path.exists(filename):
            cursor = cls.get_conn().cursor()
            for sql in cls.sql_schemas:
                cursor.execute(sql)
            for sql in cls.sql_indexes:
                cursor.execute(sql)
            cursor.close()
            if cls._auto_commit:
                cls.get_conn().commit()
        else:
            #TODO make-sure this is optimal
            cursor = cls.get_conn().cursor()
            for sql in cls.sql_schemas:
                cursor.execute(sql)
            for sql in cls.sql_indexes:
                cursor.execute(sql)
            cursor.close()
            if cls._auto_commit:
                cls.get_conn().commit()


    @classmethod
    def force_init_db(cls):
        """Force the initialisation of the database and overwrite it."""
        filename = Configuration.get_instance().database_file
        if os.path.exists(filename):
            os.remove(filename)
        cls.init_db()

    @classmethod
    def execute(cls, sql, data=None):
        res = tuple()
        try:
            conn = cls.get_conn()
            cursor = conn.cursor()
            if data is None:
                res = tuple(cursor.execute(sql))
            else:
                res = tuple(cursor.execute(sql, data))
            cursor.close()
            if cls._auto_commit:
                conn.commit()
        except (sqlite3.IntegrityError, sqlite3.InternalError):
            printf("Error on: ", sql, data)
            #TODO logging?
        return res

    @classmethod
    def executemany(cls, sql, data=None):
        res = []
        conn = cls.get_conn()
        cursor = conn.cursor()
        if data is not None:
            for data_row in data:
                try:
                    res.append(cursor.execute(sql, data_row))
                except (sqlite3.IntegrityError, sqlite3.InternalError) as err:
                    printf("Error on: ", sql, data, err)
        else:
            try:
                res.append(cursor.execute(sql))
            except (sqlite3.IntegrityError, sqlite3.InternalError) as err:
                printf("Error on: ", sql, data, err)
        cursor.close()
        if cls._auto_commit:
            conn.commit()
        return res

    @classmethod
    def populate_db(cls, data, sql_query=None):
        """Populate the database with items in data."""
        sql_query = sql_query or cls.sql_insert_station_sql
        return cls.executemany(sql_query, data)

    @classmethod
    def set_auto_commit(cls, value=True):
        """enable/disable auto_commits to speed-up batch queries"""
        cls._auto_commit = value
        if value:
            cls.get_conn().commit()

class StationDAO(object):
    table = "stations"
    schema = DB_SQL_SCHEMA_STATIONS
    indexes = (DB_SQL_INDEX_PRICES_AVAILABLE, DB_SQL_INDEX_TIMESTAMP,)
    select_all_before_sql = "select * from %s where datetime(begin_timestamp||':00') < datetime(?||':00')" % table
    select_all_query_sql = "select * from %s" % table
    select_query_sql = "select * from %s where id=?" % table
    select_all_prices_available_sql = "select * from %s where prices_available" % table
    select_all_prices_missing_sql = "select * from %s where not (prices_available)" % table
    select_prices_is_available_sql = "select * from %s where id=?" % table
    select_latitude_longitude = "select latitude, longitude from %s where id=?" % table
    insert_station_sql = "insert into %s (id, name, mark, street, street_number, zipcode, place, latitude, longitude, prices_available, begin_timestamp) "\
            "values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);" % table 

    def __init__(self):
        pass

    @classmethod
    def get_all(cls):
        return DBManager.execute(cls.select_all_query_sql)

    @classmethod
    def get(cls, pk):
        pk = str(pk)
        try:
            return DBManager.execute(cls.select_query_sql, (pk,))[0]
        except:
            #TODO loggin?
            return None
    
    @classmethod
    def get_all_before(cls, timestamp):
        return DBManager.execute(cls.select_all_before_sql, (timestamp,))

    @classmethod
    def get_latitude_longitude(cls, pk):
        pk = str(pk)
        #try:
        return DBManager.execute(cls.select_latitude_longitude, (pk,))[0]
        #except:
        #    #TODO logging? exception
        #    return 0, 0

    @classmethod
    def is_prices_available(cls, pk):
        pk = str(pk)
        try:
            return DBManager.execute(cls.select_prices_is_available_sql, (pk,))[0]
        except:
            #TODO logging?
            return False

    @classmethod
    def get_all_with_prices(cls):
        return DBManager.execute(cls.select_all_prices_available_sql)

    @classmethod
    def get_all_without_prices(cls):
        return DBManager.execute(cls.select_all_prices_missing_sql)

    @classmethod
    def populate(cls, data):
        """Populate the corresponding table with items in data."""
        return DBManager.executemany(cls.insert_station_sql, data)


if __name__ == "__main__":
    Configuration.config(**os.environ)
    lst = tuple(StationDAO.get_all_before("2016-09-27 19:41:31+02"))
    for row in lst:
        printf(row[-1])