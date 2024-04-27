from fops_log import *
import os
import sys
import pathlib
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import mariadb
from configparser import ConfigParser

logpath=os.path.join(pathlib.Path(__file__).parent.absolute(), "log/fileops.log")
tolog=Log(logpath)

def initdb():
    conf=ConfigParser()
    try:
        p=pathlib.Path(__file__).parent.absolute() / "dbconf.ini"
        conf.read(p)
    except Exception as e:
        tolog.printlog("E", "Unable to read database config file")  
        tolog.printlog('E',e)
        exit 
    try:
    
        conn_param={
            "host" : conf.get("dbconf","host"),
            "port" : int(conf.get("dbconf","port")),
            "user" :conf.get("dbconf","user"),
            "password" : conf.get("dbconf","password")
            }
        c=mariadb.connect(**conn_param)
        print(conn_param)
    except Exception as e:
        tolog.printlog("E", ("Unable to connect to DB -- " + repr(e)))  
        exit 
         
    return c  

def setup_db():
    cr1=conn.cursor()
    table_qry={
        "tab_flist" : """CREATE TABLE `tab_flist` (
	                    `id` BIGINT NOT NULL AUTO_INCREMENT,
	                    `f_name` VARCHAR(300) NOT NULL,
	                    `b_path` VARCHAR(500),
	                    `r_path` VARCHAR(500),
	                    `a_time` DATETIME,
	                    `p_time` DATETIME,
	                    `processed` TINYINT,
	                    PRIMARY KEY (`id`)
                        )""",
        "regx_list" : """CREATE TABLE `regx_list` (
                    	`id` INT NOT NULL AUTO_INCREMENT,
	                    `r_type_id` INT NOT NULL,
	                    `r_value` VARCHAR(300),
	                    PRIMARY KEY (`id`)
                        )""",
        "reg_result" : """CREATE TABLE `reg_result` (
                    	`id` BIGINT unsigned NOT NULL AUTO_INCREMENT,
	                    `r_regx_type_id` int NOT NULL,
	                    `r_regx_id` int NOT NULL,
                    	`f_id` BIGINT NOT NULL,
	                    `ln_number` BIGINT unsigned,
	                    `r_match` VARCHAR(200),
                    	PRIMARY KEY (`id`)
                        )""",
        "regx_types" : """CREATE TABLE `regx_types` (
                    	`id` SMALLINT NOT NULL AUTO_INCREMENT,
	                    `name` VARCHAR(200) NOT NULL,
	                    PRIMARY KEY (`id`)
                        );"""
    }
    
    
    try:
        cr1.execute("show databases like 'piidb'")
        o=cr1.fetchall()
    except Exception as e:
        tolog.printlog("E", ("Unable to fetch result from DB -- " + repr(e)))
        
    if (len(o)<1):
        try:
            cr1.execute("create database piidb")
            conn.database="piidb"
            conn.commit()
        except Exception as e:
            tolog.printlog("E", ("Unable to create Database PIIDB -- " + repr(e)))
        
        try:
            cr1.execute(table_qry["reg_result"])
            tolog.printlog("I", "Created reg_result table...")
            cr1.execute(table_qry["regx_types"])
            tolog.printlog("I", "Created reg_types table...")
            cr1.execute(table_qry["regx_list"])
            tolog.printlog("I", "Created regex_list table...")
            cr1.execute(table_qry["tab_flist"])
            tolog.printlog("I", "Created tab_flist table...")
            conn.commit()
        except Exception as e:
            tolog.printlog("E", ("Unable to create tables -- " + repr(e)))
            
            #insert sample data 
        try:
            emlregx="[A-Z0-9a-z._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,6}"
            cr1.execute("SET GLOBAL sql_mode = 'NO_BACKSLASH_ESCAPES'")
            cr1.execute("insert into piidb.regx_types(name) values('EMAIL')")
            cr1.execute("insert into piidb.regx_list(r_type_id, r_value) values(%s,%s)", (str(1),emlregx))
            tolog.printlog("I", "Inserted initial data...")
        except Exception as e:
            tolog.printlog("E", ("Unable to insert sample data -- " + repr(e)) )
    conn.commit()
    cr1.close()

class watchrepo:
    # Set the directory on watch
    watchDirectory = pathlib.Path(__file__).parent.absolute() / "filerepo"
 
    def __init__(self):
        self.observer = Observer()
 
    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDirectory, recursive = True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except Exception as e:
            self.observer.stop()
            tolog.printlog("E", ("Unable to insert sample data -- " + repr(e)) )
           
        self.observer.join()
 
 
class Handler(FileSystemEventHandler):
 
        
    @staticmethod
    def on_any_event(event):
        c1=conn.cursor()
        q="insert into piidb.tab_flist(f_name, b_path, r_path, a_time, processed) values(%s,%s,%s,%s,%s)"
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            # Event is created, you can process it now
            #add_file_to_db(event.src_path)
            head, tail = os.path.split(event.src_path)
            dt=time.strftime('%Y-%m-%d %H:%M:%S')
            c1.execute(q,(tail,head,'./filerepo',dt,0))
            print(head, tail)
            conn.commit()
            #print("Watchdog received created event - % s." % event.src_path)
        #elif event.event_type == 'modified':
            # Event is modified, you can process it now
        #    print("Watchdog received modified event - % s." % event.src_path)
     
    
    
    
def main():
    global conn
    conn=initdb()
    setup_db()
    repo_mon=watchrepo()
    repo_mon.run()
    
    conn.close()
    
if __name__ == '__main__':
    main()
