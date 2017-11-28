# -- coding: utf-8 --
import sqlite3
import codecs
import os
from .. import utils



DB_PATH = "resources/db/db.sqlite3"

# id: the station id
# name: the station name
# mark: the startion mark
# street: the streetname
# street_number: the street number
# zipcode: the postal zipcode
# place: the place/region
# nb_pos: the number of positive matches during training
# nb_neg: the number of negative matches during training
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
    daily_updates INT NOT NULL,
    update_interval INT NOT NULL,
    avg_price INT NOT NULL,
    stdev_price INT NOT NULL
);"""

DB_SQL_SCHEMA_PRICES = """CREATE TABLE IF NOT EXISTS prices(
    id INTEGER PRIMARY KEY,
    station_id INTEGER NOT NULL,
    timestamp TEXT NOT NULL,
    price INT NOT NULL,
	    FOREIGN KEY (station_id) REFERENCES stations(station_id)
);"""

DB_SQL_INDEX_NAME = "CREATE INDEX IF NOT EXISTS word_index on stations(name COLLATE NOCASE);"
DB_SQL_INDEX_MARK = "CREATE INDEX IF NOT EXISTS mark_index on stations(mark COLLATE NOCASE);"
DB_SQL_INDEX_PLACE = "CREATE INDEX IF NOT EXISTS place_index on stations(place COLLATE NOCASE);"
DB_SQL_INDEX_STATION = "CREATE INDEX IF NOT EXISTS station_index on prices(station_id COLLATE NOCASE);"

def icompare(text1, text2):
    return (u"%s" % text1).lower() == (u"%s" % text2).lower()



class DBManager(object):
    sql_schemas = (DB_SQL_SCHEMA_STATIONS, DB_SQL_SCHEMA_PRICES)
    sql_indexes = (DB_SQL_INDEX_MARK, DB_SQL_INDEX_NAME, DB_SQL_INDEX_PLACE, DB_SQL_INDEX_STATION)
    filename = DB_PATH
    conn = None
    table = "Stations"
    table_stations = "Stations"
    table_prices = "Prices"
    sql_insert_price = "insert into %s (id, station_id, timestamp, price) values(NULL, ?, ?, ?);" % table_prices
    sql_insert_station = "insert into %s (id, name, mark, street, street_number, zipcode, place, latitude, longitude, daily_updates, update_interval, avg_price, stdev_price) "\
            "values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);" % table_stations
    sql_get = ""
    sql_update = ""
    sql_delete = ""
    sql_save = ""
    _auto_commit = True

    @classmethod
    def open(cls):
        if cls.conn:
            return
        cls.conn = sqlite3.connect(cls.filename)
        cls.conn.create_function("icompare", 2, icompare)

    @classmethod
    def getConn(cls):
        if cls.conn is None:
            cls.open()
        return cls.conn

    @classmethod
    def close(cls):
        if cls.conn:
            cls.conn.commit()
            cls.conn.close()
            cls.conn = None

    @classmethod
    def init_db(cls):
        """Init the database if it doesn't exist yet."""
        if not os.path.exists(cls.filename):
            cursor = cls.getConn().cursor()
            for sql in cls.sql_schemas:
                cursor.execute(sql)
            for sql in cls.sql_indexes:
                cursor.execute(sql)
            cursor.close()
            if cls._auto_commit:
                cls.getConn().commit()
        else:
            #TODO make-sure this is optimal
            cursor = cls.getConn().cursor()
            for sql in cls.sql_schemas:
                cursor.execute(sql)
            for sql in cls.sql_indexes:
                cursor.execute(sql)
            cursor.close()
            if cls._auto_commit:
                cls.getConn().commit()


    @classmethod
    def force_init_db(cls):
        """Force the initialisation of the database and overwrite it."""
        if os.path.exists(cls.filename):
            os.remove(cls.filename)
        cls.init_db()

    @classmethod
    def execute(cls, sql, data=None):
        res = tuple()
        try:
            conn = cls.getConn()
            cursor = conn.cursor()
            if data is None:
                res = tuple(cursor.execute(sql))
            else:
                res = tuple(cursor.execute(sql, data))
            cursor.close()
            if cls._auto_commit:
                conn.commit()
        except (sqlite3.IntegrityError, sqlite3.InternalError):
            print "Error on: ", sql, data
            pass
        return res

    @classmethod
    def executemany(cls, sql, data=None):
        res = []
        conn = cls.getConn()
        cursor = conn.cursor()
        if data is not None:
            for data_row in data:
                try:
                    res.append(cursor.execute(sql, data_row))
                except (sqlite3.IntegrityError, sqlite3.InternalError) as err:
                    print "Error on: ", sql, data, err
        else:
            try:
                res.append(cursor.execute(sql))
            except (sqlite3.IntegrityError, sqlite3.InternalError) as err:
                print "Error on: ", sql, data, err
        cursor.close()
        if cls._auto_commit:
            conn.commit()
        return res

    @classmethod
    def populate_db(cls, data, sql_query=None):
        """Populate the database with items in data."""
        sql_query = sql_query or cls.sql_insert_station
        return cls.executemany(sql_query, data)

    @classmethod
    def set_auto_commit(cls, value=True):
        cls._auto_commit = value
        if value:
            cls.getConn().commit()

class StationDAO:
    table = "stations"
    select_all_query = "select * from %s" % table
    select_query = "select * from %s where id=?" % table
    
    @classmethod
    def getAll(cls):
        return DBManager.execute(cls.select_all_query)

    @classmethod
    def get(cls, pk):
        pk = str(pk)
        return DBManager.execute(cls.select_query, pk)[0]


class PriceDAO:
    table = "prices"
    select_all_query = "select * from %s" % table
    select_query = "select * from %s where id=?" % table
    
    @classmethod
    def getAll(cls):
        return DBManager.execute(cls.select_all_query)

    @classmethod
    def get(cls, pk=None):
        pk = str(pk)
        return DBManager.execute(cls.select_query, pk)[0]



if __name__ == "__main__":
    DBManager.init_db()
    dir_prices = None
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
    STATION_ID = 4
    res = utils.get_station_prices(STATION_ID, dir_prices) 
    WINDOW = 50
    res = tuple(res)
    print len(res)
    res = res[:100+WINDOW]
    avg_abs_err = 0.0
    pow_fact = 1.5
    for id_, time_price in enumerate(res[WINDOW:]):
        vals = (res[id_:id_+WINDOW])
        avg = sum(v[1]*(i+1)**pow_fact for i,v in enumerate(vals))
        avg /= 1.0*sum(i**pow_fact for i in range(1,WINDOW+1))
        
        #avg = sum(v[1] for v in vals)
        #avg /= len(vals)
        #print avg - time_price[1]
        avg_abs_err += abs(avg - time_price[1])**2
    print "AVG_ABS_ERR: ", avg_abs_err/len(res)
    #print len(inf)

