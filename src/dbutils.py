'''
数据库相关接口
'''

import config as C
import sqlite3

def get_conn():
	return sqlite3.connect(C.DATABASE_PATH)

def execute(conn,sql):
	return conn.cursor().execute(sql)

def get_logs(conn):
	sql = "select * from {};".format(C.DB_NAME_LOGS)
	return execute(conn,sql)

def add_log(conn,time,ip,url,action,content=None):
	
	tables = C.DB_TABLE_LOGS
	args = {"time":time,"ip":ip,"url":url,"action":action}
	conn.cursor().execute('INSERT INTO {} {} VALUES (:time, :ip ,:url, :action)'.format(C.DB_NAME_LOGS,tables),args)

	# 写入完整记录
	if content and ( action == C.ACTION_LOG or action == C.ACTION_BLOCK):
		last_insert_rowid = execute(conn,'select last_insert_rowid() from {}'.format(C.DB_NAME_LOGS))
		log_id = last_insert_rowid.__next__()[0]

		tables = C.DB_TABLE_FULL_LOG
		args = {"log_id":log_id,"content":content}
		conn.cursor().execute('INSERT INTO {} {} VALUES (:log_id, :content)'.format(C.DB_NAME_FULL_LOG,tables),args)
	conn.commit()

def get_rules(conn):
	sql = "select * from {};".format(C.DB_NAME_RULES)
	return execute(conn,sql)

def add_rule(conn,action,content,description=''):
	tables = C.DB_TABLE_RULES
	# 防止注入
	args = {"action":action,"content":content,"description":description}
	conn.cursor().execute('INSERT INTO {} {} VALUES (:action, :content, :description)'.format(C.DB_NAME_RULES,tables),args)
	conn.commit()

def delete_rule(conn,uid):
	# id是保留字
	sql = 'DELETE FROM {} WHERE id={}'.format(C.DB_NAME_RULES,uid)
	conn.execute(sql)
	conn.commit()

def get_whitelists(conn):
	sql = "select * from {};".format(C.DB_NAME_WHITELIST)
	return execute(conn,sql)

def add_whitelist(conn,url,ip):
	tables = C.DB_TABLE_WHITELIST
	# 防止注入
	args = {"url":url,"ip":ip,}
	conn.cursor().execute('INSERT INTO {} {} VALUES (:url, :ip)'.format(C.DB_NAME_WHITELIST,tables),args)
	conn.commit()

def delete_whitelist(conn,uid):
	sql = 'DELETE FROM {} WHERE id={}'.format(C.DB_NAME_WHITELIST,uid)
	conn.execute(sql)
	conn.commit()

def get_blacklists(conn):
	sql = "select * from {};".format(C.DB_NAME_BLACKLIST)
	return execute(conn,sql)

def add_blacklist(conn,url,ip):
	tables = C.DB_TABLE_WHITELIST
	# 防止注入
	args = {"url":url,"ip":ip,}
	conn.cursor().execute('INSERT INTO {} {} VALUES (:url, :ip)'.format(C.DB_NAME_BLACKLIST,tables),args)
	conn.commit()

def delete_blacklist(conn,uid):
	sql = 'DELETE FROM {} WHERE id={}'.format(C.DB_NAME_BLACKLIST,uid)
	conn.execute(sql)
	conn.commit()

def test():
	c = get_conn()
	# add_log(c,"2021-02-27","127.0.0.1","/src?id=123","PASS")
	# add_log(c,"2021-02-27","127.0.0.1","/src?id=evil","BLOCK","hello\n123\nthis\n\n123123")
	add_rule(c,"PASS",".*safe.*","test1")
	add_rule(c,"BLOCK",".*id=evil.*","test2")
	add_rule(c,"BLOCK",".*id=ev[0-9].*il.*","test3")
	add_rule(c,"LOG",".*id=evil[0-9].*","test4")
	add_rule(c,"LOG",".*id=.*evil.*","test5")
	add_rule(c,"LOG","\'\"\\1adhello","error compile test")

#test()