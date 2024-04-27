from inc.db import initdb

class piireport:
	def __init__(self) -> None:
		self.conn=initdb.initconn()
		self.cur=self.conn.cursor()
	
	def get_regx(self,rid):
		query="select a.id, a.name, b.id, b.r_value from piidb.regx_types a join piidb.regx_list b on a.id=b.r_type_id order by a.id"
		f_query="select a.id, a.name, b.id, b.r_value from piidb.regx_types a join piidb.regx_list b on a.id=b.r_type_id where a.id=%s"
		if(rid>0):
			self.cur.execute(f_query,str(rid))
		else:
			self.cur.execute(query)
		res=self.cur.fetchall()
		return res

	def get_types(self):
		query="select * from piidb.regx_types"
		self.cur.execute(query)
		res=self.cur.fetchall()
		return res

	