import dbutils
from utils import log
import time

def do_log(req,ip,action,full=False):

	conn = dbutils.get_conn()
	timestr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
	line = req.split('\n')[0]
	url = line.split(" ")[1]

	if full:
		dbutils.add_log(conn,timestr,ip,url,action,req)
		log("req full logged.",1)
	else:
		dbutils.add_log(conn,timestr,ip,url,action,None)
		log("req partially logged.",1)