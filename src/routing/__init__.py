"""routing - gas tank strategy manager"""

from .graph import Graph
from .node import Node
from ..dao.db import StationDAO


def generate_tank_infos(capacity, timestamps_stations_prices):
    """generate routing informations,
    capacity: int, the tank capacity
    timestamps_stations_prices: lst<str, int, int>, the predicted price informations
    return routing informations according to the Intellitank format"""
    g = Graph(capacity)
    for timestamp, station_id, pred_price in timestamps_stations_prices:
        latitude, longitude = StationDAO.get_latitude_longitude(station_id)
        node = Node(station_id, latitude, longitude, pred_price, timestamp)
        g.nodes.append(node)
    g.nodes.sort(key=lambda gr: gr.datetime)
    g.start = g.nodes[0]
    g.goal = g.nodes[-1]
    g.find_nexts()
    g.find_prevs()
    g.find_nexts()
    g.find_prevs()
    routing_infos = g.generate_refuel_infos()
    return routing_infos