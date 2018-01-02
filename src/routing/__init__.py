from .graph import Graph
from .node import Node
from ..dao.db import StationDAO


def generate_tank_infos(capacity, timestamps_stations_prices):
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
    routing_infos = g.drive_to_next()
    return routing_infos