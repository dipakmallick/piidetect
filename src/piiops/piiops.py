from piiops_log import *
import os
import pathlib
import time
import mariadb
from configparser import ConfigParser
import re
import schedule

logpath=os.path.join(pathlib.Path(__file__).parent.absolute(), "log/piiops.log")
tolog=Log(logpath)

def initdb():
    conf=ConfigParser()
    try:
        p=pathlib.Path(__file__).parent.absolute() / "dbconf.ini"
        conf.read(p)
    except Exception as e:
        tolog.printlog("E", "Unable to read database config file" + str(e))  
        exit 
    
    
    conn_param={
            "host" : conf.get("dbconf","host"),
            "port" : int(conf.get("dbconf","port")),
            "user" :conf.get("dbconf","user"),
            "password" : conf.get("dbconf","password"),
            "database" : "piidb"
            }
    try:
        c=mariadb.connect(**conn_param)
        #print(conn_param)
    except Exception as e:
        tolog.printlog("E", ("Unable to connect to DB -- " + str(e)))  
        exit 
    return c

def insert_to_db(f_matches,fid):
    c1=conn.cursor()
    print(f_matches)
    query="insert into piidb.reg_result(r_regx_type_id, r_regx_id, f_id, ln_number, r_match) values(%s,%s,%s,%s,%s)"
    try:
        c1.executemany(query,f_matches)
        tolog.printlog("I", "Inserted total  " + len(f_matches) + "  matches...")
    except Exception as e:
        tolog.printlog("E", "Unable to insert results..." + str(e))
         
    t=time.strftime('%Y-%m-%d %H:%M:%S')
    query="update piidb.tab_flist set processed=1, p_time=%s where id=%s"
    try:
        c1.execute(query,(t,str(fid)))
        tolog.printlog("I", "File table update...")
    except Exception as e:
        tolog.printlog("E", "Unable to update file table..." + str(e))
    conn.commit()
    c1.close()
        
    
def load_r_types():
    c1=conn.cursor()
    query="select a.id, a.name, b.id, b.r_value from piidb.regx_types a join piidb.regx_list b on a.id=b.r_type_id"
    c1.execute(query)
    r=c1.fetchall()
    c1.close()
    return r

def get_f_list():
    c2=conn.cursor()
    c2.execute("select * from piidb.tab_flist where processed=0")
    f=c2.fetchall()
    print(f)
    c2.close()
    return f

def r_detect(p):
    flst=get_f_list()
    file_matches=list()
    bpath=os.path.dirname(__file__)
    if (len(flst)<1):
        tolog.printlog("I", "No files to process...")
        return

    for fl in flst:
        fpath=os.path.join(bpath,"filerepo",fl[1])
        print(bpath)
        with open(fpath) as file:
            lno=1
            fid=fl[0]
            for line in file:           
                for pattn in p:
                    ptn=pattn[3]
                    result=ptn.findall(line)
                    if (len(result)>0):
                        for m in result:
                            file_matches.append((pattn[0],pattn[2],fl[0],lno,m))
                        
                lno+=1
            insert_to_db(file_matches,fid)
            file.close()

            

def detect_regx():
    pattn=list()
    r_list=load_r_types()
    for r in r_list:
        pattn.append((r[0],r[1],r[2],re.compile(r[3])))
    r_detect(pattn)
     
    
def main():
    global conn
    time.sleep(120)
    conn=initdb()
    schedule.every(1).minutes.do(detect_regx)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
    

if __name__ == '__main__':
    main()
