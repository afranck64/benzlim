import logging
import os
import glob

from ..exceptions_ import (BadFormatException, BenzlimException)
from ..compat import printf
from ..config import Configuration
from ..dao import CSVDAO
from ..prediction import (process_predictions, process_routing)

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
    for route, route_pred in routes_prices:
        try:
            #printf("File: %s" % route)
            logging.debug("Route file: %s" % route)
            res = process_routing(route, config.prices_dir, None, None, nb_workers=config.nb_workers)
        except BadFormatException as err:
            assert "falsche" in route
        except BenzlimException as err:
            logging.error(err)

def test():
    printf("Testing benzlim...")
    test_predict()
    #test_route()
