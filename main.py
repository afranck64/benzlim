from InputFileReader import readRoute, read_id
from Node import Node
from Graph import Graph
from pg import DB
import random;


if __name__ == '__main__':

    #TODO: get lat/lon from a database?
    # db = DB(dbname='testdb', host='pgserver', port=5432, user='scott', passwd='tiger')
    # db.query("create table fruits(id serial primary key, name varchar)")

    g = Graph(200)
    d = readRoute("bb.csv")
    for i in d:
        n = read_id(i)
        n.set_price(random.randrange(20))
        g.nodes.append(n)
    g.start = g.nodes[0]
    g.goal = g.nodes[-1]

    g.find_nexts()
    g.find_prevs()
    print(g.drive_to_next())
