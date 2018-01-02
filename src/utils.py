# -- coding: utf-8 --

"""utils.py - usefool tools"""
import sys
import os.path
from .compat import printf
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

def cosine_sim(v1, v2):
    """returns the cosine similarity between iterables v1 and v2.
    If one v1 or v2 is null-vector, zero is returned."""
    scalar_product = 0.0
    for i, x1 in enumerate(v1):
        scalar_product += x1*v2[i]
    norm_v1 = sum(x**2 for x in v1)**.5
    norm_v2 = sum(x**2 for x in v2)**.5

    if norm_v1 * norm_v2 == 0:
        return 0
    return scalar_product/(norm_v1*norm_v2)


def extend2norm(v):
    """extends the passed vector to its normalized representation
    and appends its norm at the end."""
    norm = sum(x**2 for x in v)**0.5
    if norm:
        res = [x/norm for x in v]
    else:
        res = [x for x in v]
    res.append(norm)
    return res


def cosine_sim2(v1, v2):
    """returns a similarity score between -1 and 1,
    based on the cosine similarity extended with vectors' norm."""
    v1_ext = extend2norm(v1)
    v2_ext = extend2norm(v2)
    n1 = v1_ext[-1]
    n2 = v2_ext[-1]
    k1 = k2 = 1.0
    if n1*n2 != 0:
        if n1 > n2:
            k1 = 1.0
            k2 = n2/n1
        else :
            k1 = n1/n2
            k2 = 1.0
    elif n1 == n2:
        #both vectors are null therefore total similary
        return 1.0
    else:
        #only one vector is null therefore absolutely not similary
        return 0

    v1_ext[-1] = k1
    v2_ext[-1] = k2

    return cosine_sim(v1_ext, v2_ext)

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
    return value.decode('utf8').lower()

def str2town(value):
    """convert a str to unicode"""
    return value.decode('utf8').lower()

def str2zipcode(value):
    """convert a str to int"""
    try:
        return int(value)
    except ValueError as err:
        logging.error("str2zipcode: <%s>" % (value, err))
        return 0

def str2unicode(value):
    """convert a str to unicode"""
    return value.decode('utf8')

def create_file_dirs(filename):
    """create all directories contenained in the tree to filename"""
    try:
        path_dir = os.path.split(filename)[0]
        if not os.path.exists(path_dir):
            os.makedirs(path_dir)
    except OSError as err:
        logging.warn(err.message)

def create_dirs(path):
    """craete all directories leading to path (inclusive itself)"""
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError as err:
        logging.warn(err.message)

class Logger(object):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    def __init__(self):
        pass

    @classmethod
    def log(self, message):
        pass

    @classmethod
    def info(self, message):
        pass

    @classmethod
    def debug(self, message):
        pass

    @classmethod
    def warning(self, message):
        pass

    @classmethod
    def error(self, message):
        pass

if __name__ == "__main__":
    pass