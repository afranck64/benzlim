from InputFileReader import readRoute, read_id
from Node import Node
from Graph import Graph
#from pg import DB


if __name__ == '__main__':

    #TODO: get lat/lon from a database?
    # db = DB(dbname='testdb', host='pgserver', port=5432, user='scott', passwd='tiger')
    # db.query("create table fruits(id serial primary key, name varchar)")

    d = readRoute("bb.csv")
    g = Graph(d.pop("capacity"))
    print(g.capacity)
    for i in d:
        n = read_id(i)
        n_datetime=d[i]
        if n is not None:
            g.nodes.append(n)
            n.datetime=n_datetime
    g.nodes.sort(key=lambda gr: gr.datetime)
    g.start = g.nodes[0]
    g.goal = g.nodes[-1]
    g.find_nexts()
    g.find_prevs()
    print(g.nodes[1].next.id)
    print(g.drive_to_next())
