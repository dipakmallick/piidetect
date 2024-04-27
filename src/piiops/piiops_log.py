import logging
from logging.handlers import RotatingFileHandler

class Log:
    def __init__(self, logfl) -> None:
        logging.basicConfig(
                            encoding='utf-8',
                            level=logging.DEBUG,format='%(asctime)s %(levelname)s %(filename)s:%(lineno)s: %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S'
                            )
        self.logger= logging.getLogger(__name__)
        handlers=RotatingFileHandler(logfl, maxBytes=1000000, backupCount=3)
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
                   