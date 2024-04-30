from inc.db import initdb

class add_data:
    def __init__(self) -> None:
        self.conn=initdb.initconn()
        self.cur=self.conn.cursor()
	
    def add_type(self,rval):
        query="insert into piidb.regx_types(name) values(%s)"
        self.cur.execute(query,(rval,))
        self.conn.commit()
        return 1
        
    def add_regex(self,td, tval):
        query="insert into piidb.regx_list(r_type_id, r_value) values(%s,%s)"
        try:
            self.cur.execute(query,(str(td),tval))
            self.conn.commit()
        except Exception as e:     
            return e
        return 0
    
    def __del__(self):
        self.conn.close()