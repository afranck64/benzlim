import os
import glob

from ..exceptions_ import (BadFormatException, BenzlimException)
from ..compat import printf
from ..config import Configuration
from ..prediction import (process_predictions, process_routing)



def get_route_files_prices():
    src_dir = Configuration.get_instance().src_dir
    rel_path = "tests/data_route/*.csv"
    filenames = glob.glob(os.path.join(src_dir, rel_path))
    res = []
    for filename in filenames:
        filename_price = os.path.splitext(filename)[0] + "_prices.csv"
        if not filename.endswith("prices.csv") and filename_price in filenames:
            res.append((filename, filename_price))
    return res

def get_predict_files_prices():
    src_dir = Configuration.get_instance().src_dir
    rel_path = "tests/data_predict/*.csv"
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
    for p_file, p_file_price in predict_infos:
        try:
            predict_res = process_predictions(p_file, config.prices_dir, None, config.nb_workers)
        except BenzlimException as err:
            printf(err)

def test_route():
    routes_prices = get_route_files_prices()
    config = Configuration.get_instance()
    for route, route_pred in routes_prices:
        try:
            printf("File: %s" % route)
            process_routing(route, config.prices_dir, None, None, nb_workers=config.nb_workers)
        except BenzlimException as err:
            printf(err)

def test():
    test_predict()