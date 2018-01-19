import logging
import os
import glob
from copy import deepcopy

import numpy as np

from ..exceptions_ import (BadFormatException, BenzlimException)
from ..compat import printf
from ..config import Configuration
from ..dao import CSVDAO, StationDAO
from ..prediction import (process_predictions, process_routing)
from ..routing import Graph, Node

def diff_prices(data1, data2):
    if data1 and data2:
        lst = [abs(data1[i][-1]-data2[i][-1]) for i in range(len(data1))]
        logging.debug("Diffs: %s" % str(lst))
        return min(lst), max(lst), sum(lst)/len(lst)
    else:
        return 0, 0, 0

def get_route_files_prices():
    src_dir = Configuration.get_instance().src_dir
    rel_path = os.path.join("tests", "data_route", "*.csv")
    filenames = glob.glob(os.path.join(src_dir, rel_path))
    res = []
    for filename in filenames:
        filename_price = os.path.splitext(filename)[0] + "_prices.csv"
        if not filename.endswith("prices.csv") and filename_price in filenames:
            res.append((filename, filename_price))
    return res

def get_predict_files_prices():
    src_dir = Configuration.get_instance().src_dir
    #TODO
    rel_path = os.path.join("tests", "data_predict", "*keine*.csv")
    rel_path = os.path.join("tests", "data_predict", "*.csv")
    filenames = glob.glob(os.path.join(src_dir, rel_path))
    res = []
    for filename in filenames:
        filename_price = os.path.splitext(filename)[0] + "_prices.csv"
        if not filename.endswith("prices.csv") and filename_price in filenames:
            res.append((filename, filename_price))
    return res


def verify(route_filename, nb_runs=20):
    route = CSVDAO.get_route_params(route_filename)
    base_capacity, node_rows = route
    max_tanked = -1
    capacity = 2
    base_g = Graph(base_capacity)
    for timestamp, station_id in node_rows:
        station_row = StationDAO.get(station_id)
        n = Node(station_id, station_row[-4], station_row[-3], timestamp)
        n.datetime = timestamp
        n.set_price(int(np.random.uniform(1200, 1700)))
        base_g.nodes.append(n)
    base_g.nodes.sort(key=lambda gr:gr.datetime)
    base_g.start = base_g.nodes[0]
    base_g.goal = base_g.nodes[-1]

    for i in range(nb_runs):
        EPS = 1e-3
        g = deepcopy(base_g)
        g.capacity = capacity
        g.find_prevs()
        g.find_nexts()
        infos = g.generate_refuel_infos()
        tanked = sum(n.expected_amount for n in g.nodes)
        price = sum(n.expected_amount*n.price for n in g.nodes)
        if tanked +EPS < max_tanked:
            printf("ERROR: You tanked only %f instead of at least %f while having more capacity %.2f, step: %s" % (tanked, max_tanked, capacity, i+1))
            max_tanked = tanked
            return
        else:
            max_tanked = tanked
            #print "You tanked: %.2f with capacity: %.2f at: %d" % (tanked, g.capacity, price)
        capacity += capacity/3.0


def test_predict():
    predict_infos = get_predict_files_prices()
    config = Configuration.get_instance()
    lst_min = []
    lst_max = []
    lst_avg = []
    for p_file, p_file_price in predict_infos:
        try:
            logging.debug("Predict file: %s" %p_file)
            data = process_predictions(p_file, config.prices_dir, None, config.nb_workers)
            real_data = CSVDAO.get_predicted_prices(p_file_price)
            min_, max_, avg = diff_prices(data, real_data)
            lst_min.append(min_)
            lst_max.append(max_)
            lst_avg.append(avg)
        except BadFormatException as err:
            assert "falsche" in p_file
        except BenzlimException as err:
            logging.error(err)
    if lst_avg:
        min_ = sum(lst_min)/len(lst_min)
        max_ = sum(lst_max)/len(lst_max)
        avg = sum(lst_avg)/len(lst_avg)
        logging.info("(avg_pred_errors) Min: %s, Max: %s, Avg: %s" % (min_, max_, avg))
    else:
        printf("No test result to show")

def test_route():
    routes_prices = get_route_files_prices()
    config = Configuration.get_instance()
    for r_file, r_pred_file in routes_prices:
        try:
            logging.debug("Route file: %s" % r_file)
            verify(r_file)
            #res = process_routing(r_file, config.prices_dir, None, None, nb_workers=config.nb_workers)
        except BadFormatException as err:
            assert "falsche" in r_file
        except BenzlimException as err:
            logging.error(err)


def test():
    printf("Testing benzlim...")
    test_predict()
    test_route()
