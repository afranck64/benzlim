from math import cos, asin, sqrt


class Node:
    id = 0
    lat = 0
    lon = 0
    price = 0
    prev = None
    next = None

    def __init__(self, id, lat, lon):
        self.id = id
        self.lat = lat
        self.lon = lon
        # self.price = price

    def __lt__(self, other):  # comparison method for priority queue
        return self.price < other.price

    def __eq__(self, other):
        return self.id == other.id

    def set_price(self, price):
        self.price = price
        # TODO: get gas prognosis

    def distance_to(self, other):
        p = 0.017453292519943295  # Pi/180
        a = 0.5 - cos((other.lat - self.lat) * p) / 2 + cos(self.lat * p) * cos(other.lat * p) * (1 - cos((other.lon - self.lon) * p)) / 2
        return 12742 * asin(sqrt(a))  # 2*R*asin...