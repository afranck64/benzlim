import csv
import datetime
from Node import Node

FILE = "../../Data/Tankstellen.csv"


def readRoute(pathRoute):
    routeReader = csv.reader(open(pathRoute))
    d = {}
    try:
        capacity=next(routeReader)
        capacity=int(''.join(map(str,capacity)))
        d["capacity"]=capacity
    except ValueError:
        print("ValueError")
        d["capacity"]=-1
    for row in routeReader:
        date, id=row[0].split(";")
        date_time, tz=date.split("+")
        #timezone verarbeiten?
        # dayte,timehh=date.split()
        # year,month,day=dayte.split("-")
        # time, hh=timehh.split("+")
        # hour,minute,second=time.split(":")
        #print(date)
        try:
            datetime.datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
            d[id] = date_time
        except ValueError:
            print("Incorrect data format at id %s, should be YYYY-MM-DD HH:MM:SS" %id)
    return d


def read_id(id):
    headers = ['id', 'name', 'brand', 'adr', 'no', 'plz', 'ort', 'lat', 'lon']
    with open(FILE) as cvsfile:
        reader = csv.DictReader(cvsfile, fieldnames=headers, delimiter=';')
        for row in reader:
            if row['id'] == id:
                lat = float(row['lat'])
                lon = float(row['lon'])
                return Node(id, lat, lon)
        print('id %s not found' %id)
        return None


if __name__ == '__main__':
    readRoute("bb.csv")
    idList=[1,2,3,4,5,6,7,8,9] #??
    #TODO:distance berechnet falsche werte?
    #TODO:bei auslese-funktionen muessen unguenstige faelle abgefangen werden

def readID(gasStationID, pathIDs):
    idReader= csv.reader(open(pathIDs))
    for row in idReader:
        #TODO:try catch except irgendwas
        currentID= [list(map(int, x)) for x in row[0]]
        if currentID[0][0]==gasStationID:
            lat=float(row[7])
            lon=float(row[8])
            return lat,lon
    return -1,-1
