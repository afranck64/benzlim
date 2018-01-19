"""train.py - manage the whole training"""

import os
import logging

from .dao import (CSVDAO, DBManager, StationDAO)
from .compat import printf
from .config import Configuration

class Trainer(object):
    @staticmethod
    def train():
        config = Configuration.get_instance()

        #TODO Warning message, everithing will be lost!!!
        if os.path.exists(config.database_file) and not config.force:
            logging.warn("Training data seems to already exist.\n\tRetry with --force to overwrite it")
            return
        DBManager.force_init_db()
        StationDAO.populate(CSVDAO.get_all_extended_stations_infos())

    @staticmethod
    def autotrain():
        config = Configuration.get_instance()
        if not os.path.exists(config.database_file):
            Trainer.train()



if __name__ == "__main__":  #pragma: no cover
    Configuration.config(**os.environ)
    printf(Configuration.get_instance().database_file)
    Trainer.train()