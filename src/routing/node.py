"""node.py - Nodes for graph based representation of gas stations in a route"""
from math import cos, asin, sqrt
import datetime



class Node:
    def __init__(self, id_, lat, lon, price=0, timestamp=''):
        """Node for representing a gas station
        id_: int, station id
        lat: float, the station latitude
        lon: float, the station longitude
        price: int, the gas price at the station
        timestamp: str, the time of visiting this station"""
        self.id = id_
        self.lat = lat
        self.lon = lon
        self.price = price
        self.datetime = timestamp
        self.prev = self
        self.next = self
        self.startpoint = None
        self.current_gas = 0
        self.expected_amount = 0

    def __lt__(self, other):  # comparison method for priority queue
        return self.price < other.price
    
    def __le__(self, other):
        return self.price <= other.price

    def __eq__(self, other):
        return self.key == other.key

    def __str__(self):
        return "Node:(id %s, price %s, prev %s, next %s, expected amount %s)" % \
               (self.id, self.price, self.prev.id, self.next.id, self.expected_amount)

    def __repr__(self):
        return self.__str__()
    
    def distance_to(self, other, g, use_tolerance=False):
        """determine the distance between this node and <other>,
        if <use_tolerance> is set to True, the tolerance set in <g> is used.
        other:  Node, the other node to determine distance to
        g:  Graph, the graph containing all nodes of the route
        use_tolerance: bool, weither to use tolerance or not

        return the calculated distance"""
        y = self
        result = 0
        while True:
            if y == other:
                break
            next_y = g.nodes[g.nodes.index(y) + 1]
            p = 0.017453292519943295  # Pi/180
            a = 0.5 - cos((next_y.lat - y.lat) * p) / 2 + cos(y.lat * p) * cos(next_y.lat * p) * \
                (1 - cos((next_y.lon - y.lon) * p)) / 2
            single_distance = 12742 * asin(sqrt(a))  # 2*R*asin...
            result = result + single_distance
            y = next_y
            if y == g.goal:
                break
        if use_tolerance:
            return result+g.tolerance_km
        else:
            return result

    def price_for_gas(self, amount):
        """return the cost for <amount> of gas at this station"""
        return amount * self.price

    def set_price(self, price):
        """set the price for this station"""
        self.price = price

    @property
    def key(self):
        """a unique station identifier at a given time"""
        return self.datetime, self.id, self.price
