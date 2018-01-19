# -- coding: utf-8 --

"""utils.py - usefool tools"""
import sys
import os.path
from .compat import printf, str2unicode
import logging
#from .exceptions_ import (PriceNotFoundException, StationNotFoundException)


ERROR_FILE_EXISTS = 17

#Extended cosine similarity with respect to the vectors'norm. by afranck64
def diff_score(v1, v2):
    """return the norm of the difference between both vectors"""
    diff_norm = sum((x1-x2)**2 for x1, x2 in zip(v1, v2))**0.5
    if diff_norm == 0:
        return 0
    else:
        return 1.0/diff_norm

def str2latitute(value):
    """convert a str to valid latitude"""
    if "." not in value:
        value = value[:2] + "." + value[2:]
    return float(value) 

def str2longitude(value):
    """convert a str to valid longitude"""
    if "." not in value:
        value = value[:2] + "." + value[2:]
    return float(value)

def str2mark(value):
    """convert a str to unicode"""
    return str2unicode(value)

def str2town(value):
    """convert a str to unicode"""
    return str2unicode(value)

def str2zipcode(value):
    """convert a str to int"""
    try:
        return int(value)
    except ValueError as err:
        logging.warn("str2zipcode: <%s | %s>" % (value, err))
        return 0


def create_file_dirs(filename):
    """create all directories contained in the tree to filename"""
    try:
        path_dir = os.path.split(filename)[0]
        if not os.path.exists(path_dir):
            os.makedirs(path_dir)
    except OSError as err:
        logging.warn(err.message)

def create_dirs(path):
    """create all directories leading to path (inclusive itself)"""
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError as err:
        logging.warn(err.message)
