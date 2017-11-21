import sys

from .compat import printf
from . import utils
from . import predict

def generate_predictions(timestamps_stations, end_timestamp=None):
    """Generate a prediction for each row in <timestamps_stations> while using only data prior to <end_timespain>"""
    predictions = []
    for timestamp, station_id in timestamps_stations:
        pred_price = predict.predict_price(station_id, timestamp, end_timestamp)
        yield end_timestamp, timestamp, station_id, pred_price

def process(filename, end_timestamp=None, out_filename=None):
    out_filename = out_filename or 'predictions.csv'
    capacity, timestamps_stations = utils.get_route_params(filename)
    #print timestamps_stations
    #return
    res = generate_predictions(timestamps_stations, end_timestamp)
    with open(out_filename, 'w') as output_f:
        output_f.writelines("%s;%s;%s;%s\n"%(row) for row in res)
            

def help():
    printf ("  Usage:")
    printf ("    python2 benzlim $input_file")

def main():
    printf ("Benzlim")
    if len(sys.argv)<2:
        help()
    else:
        process(sys.argv[1], end_timestamp="2015-08-04")
