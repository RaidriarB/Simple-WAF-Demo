import dbutils
from utils import log
import datetime
import pytz

'''
记录日志，根据full参数决定是否记录整个请求
'''
def do_log(req,ip,action,full=False):

	conn = dbutils.get_conn()
	timestr = datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y-%m-%d %H:%M:%S")
	line = req.split('\n')[0]
	url = line.split(" ")[1]
	if full:
		dbutils.add_log(conn,timestr,ip,url,action,req)
		log("req full logged.",1)
	else:
		dbutils.add_log(conn,timestr,ip,url,action,None)
		log("req partially logged.",1)