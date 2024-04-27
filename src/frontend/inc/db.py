import mariadb
from inc.fendlog import *
import pathlib
import os
from configparser import ConfigParser

class initdb:
    def __init__(self) -> None:
        pass
    
    def initconn():
        c=""
        tolog=Log()
        conf=ConfigParser()
        try:
            p=os.path.join(pathlib.Path(__file__).parent.absolute(), "dbconf.ini")
            conf.read(p)
        except Exception as e:
            tolog.printlog("E", "Unable to read database config file" + repr(e))  
            exit 
        try:
            conn_param={
                "host" : conf.get("dbconf","host"),
                "port" : int(conf.get("dbconf","port")),
                "user" :conf.get("dbconf","user"),
                "password" : conf.get("dbconf","password"),
                "database" : "piidb"
                 }
            c=mariadb.connect(**conn_param)
            print(conn_param)
        except Exception as e:
            tolog.printlog("E", ("Unable to connect to DB -- " + repr(e)))  
            exit 
        return c  