"""train.py - manage the whole training"""

import os
from .dao import (CSVDAO, DBManager, StationDAO)
from .config import Configuration

class Trainer(object):
    @staticmethod
    def train():
        config = Configuration.get_instance()

        #TODO Warning message, everithing will be lost!!!

        #Set-up database to speedup stations-informations'access
        DBManager.force_init_db()
        StationDAO.populate(CSVDAO.get_all_extended_stations_infos())

        #Set-up classifier



if __name__ == "__main__":
    #print os.environ.get("informaticup2018_dir")
    Configuration.config(**os.environ)
    print Configuration.get_instance().database_file
    Trainer.train()