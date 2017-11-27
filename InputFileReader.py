import csv
from Node import Node

FILE = "Tankstellen.csv"


def readRoute(pathRoute):
    routeReader = csv.reader(open(pathRoute))
    d = {}
    for row in routeReader:
        #TODO: get capacity
        date, id=row[0].split(";")
        # dayte,timehh=date.split()
        # year,month,day=dayte.split("-")
        # time, hh=timehh.split("+")
        # hour,minute,second=time.split(":")
        d[id] = date
    return d


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


def read_id(id):
    headers = ['id', 'name', 'brand', 'adr', 'no', 'plz', 'ort', 'lat', 'lon']
    with open(FILE) as cvsfile:
        reader = csv.DictReader(cvsfile, fieldnames=headers, delimiter=';')
        for row in reader:
            if row['id'] == id:
                lat = float(row['lat'])
                lon = float(row['lon'])
                return Node(id, lat, lon)
        print('id not found')
        return None

if __name__ == '__main__':
    readRoute("bb.csv")
    idList=[1,2,3,4,5,6,7,8,9]
    #TODO:distance berechnet falsche werte?
    #TODO:bei auslese-funktionen müssen unguenstige faelle abgefangen werden
