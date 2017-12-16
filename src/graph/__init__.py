from .Graph import Graph
from .Node import Node
from ..dao.db import StationDAO


def generate_tank_infos(capacity, timestamps_stations_prices):
    g = Graph(capacity)
    for timestamp, station_id, pred_price in timestamps_stations_prices:
        latitude, longitude = StationDAO.get_latitude_longitude(station_id)
        n = Node(station_id, latitude, longitude)
        if n is not None:
            n.datetime = timestamp
            n.set_price(pred_price)
            g.nodes.append(n)
    g.nodes.sort(key=lambda gr: gr.datetime)
    g.start = g.nodes[0]
    g.goal = g.nodes[-1]
    g.find_nexts()
    g.find_prevs()
    info = g.drive_to_next()
    return info
