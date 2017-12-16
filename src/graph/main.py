from InputFileReader import readRoute, read_id
from Node import Node
from Graph import Graph
import random
import os

from ..compat import printf
from ..config import Configuration


if __name__ == '__main__':
    Configuration.config(**os.environ)
    d = readRoute("./Data/bb.csv")
    g = Graph(d.pop("capacity"))
    #printf(g.capacity)
    for i in d:
        n = read_id(i)
        if n is not None:
            n.datetime = d[i]
            n.set_price(random.randrange(10))
            g.nodes.append(n)
    g.nodes.sort(key=lambda gr: gr.datetime)
    g.start = g.nodes[0]
    g.goal = g.nodes[-1]
    g.find_nexts()
    g.find_prevs()
    #printf(g.nodes[1].next.id)
    info = g.drive_to_next()
    printf(info.items())
