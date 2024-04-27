import logging
from logging.handlers import RotatingFileHandler
import os
import pathlib

class Log:
    logpath=os.path.join(pathlib.Path(__file__).parent.parent.absolute(), "log/fend.log")
    def __init__(self,) -> None:
        logging.basicConfig(
                            encoding='utf-8',
                            level=logging.DEBUG,format='%(asctime)s %(levelname)s %(filename)s:%(lineno)s: %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S'
                            )
        self.logger= logging.getLogger(__name__)
        handlers=RotatingFileHandler(self.logpath, maxBytes=1000000, backupCount=3)
        self.logger.addHandler(handlers)
    
    def printlog(self,lvl, msg):
            if(lvl=='I'):
                self.logger.info(msg)
            elif(lvl=='E'):
                self.logger.error(msg)
            elif(lvl=='D'):
                self.logger.debug(msg)
            elif(lvl=='C'):
                self.logger.critical(msg)
                   