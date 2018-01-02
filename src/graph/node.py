from math import cos, asin, sqrt
import datetime


class Node:
    def __init__(self, id, lat, lon, price=0, timestamp=''):
        self.id = id
        self.lat = lat
        self.lon = lon
        # set_price
        self.price = price
        self.datetime = timestamp
        self.prev = None
        self.next = None

    def __lt__(self, other):  # comparison method for priority queue
        return self.price < other.price

    def __eq__(self, other):
        return self.key == other.key
    
    def __str__(self):
        return "Node:(%s, %s)" % (self.id, self.price)

    def __repr__(self):
        return self.__str__()

    def distance_to(self, other):
        #if other is None:
        #    return -1
        #else:
            p = 0.017453292519943295  # Pi/180
            a = 0.5 - cos((other.lat - self.lat) * p) / 2 + cos(self.lat * p) * cos(other.lat * p) *\
                                                            (1 - cos((other.lon - self.lon) * p)) / 2
            return 12742 * asin(sqrt(a))  # 2*R*asin...

    def price_for_gas(self, amount):
        return amount * self.price

    def set_price(self, price):
        self.price = price;

    @property
    def key(self):
        return (self.datetime, self.id, self.price)