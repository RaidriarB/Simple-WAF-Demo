import os
import re

import config as C
import dbutils
from utils import log

'''
从数据库中初始化规则列表
@return 规则列表
'''
def init_filter():

	log("正在加载规则...",1)
	compiled_rules = []

	conn = dbutils.get_conn()
	rules = dbutils.get_rules(conn)

	for rule in rules:
		try:
			uid,regexp,description,action = rule
			if action == "BLOCK":
				action = C.ACTION_BLOCK
			elif action == "PASS":
				action = C.ACTION_PASS
			elif action == "LOG":
				action = C.ACTION_LOG
			else:
				raise Exception()

			compiled_rule = (re.compile(regexp),action)
			compiled_rules.append(compiled_rule)
		except:
			log("编译出错，出错的条目为",2)
			log(str(rule),2)

	log("规则加载完毕。",1)
	return compiled_rules

def init_blacklist():
	log("正在加载黑名单...",1)
	blacklist = []

	conn = dbutils.get_conn()
	lists = dbutils.get_blacklists(conn)

	for item in lists:
		try:
			uid,url,ip = item
			listitem = (url,ip)
			blacklist.append(listitem)
		except:
			log("加载出错，出错的条目为",2)
			log(str(item),2)
				
	return blacklist

def init_whitelist():
	log("正在加载白名单...",1)
	whitelist = []

	conn = dbutils.get_conn()
	lists = dbutils.get_whitelists(conn)

	for item in lists:
		try:
			uid,url,ip = item
			listitem = (url,ip)
			whitelist.append(listitem)
		except:
			log("加载出错，出错的条目为",2)
			log(str(item),2)
	return whitelist
	
'''
判断请求，返回动作代码
其中分为很多部分
'''
def do_filter(client_req,ip,compiled_rules,blacklists,whitelists):


	action = None

	client_req = rebuild_chunked_encoding(client_req)

	action = do_filter_blacklist(client_req,ip,blacklists)
	if action is not None:
		return action

	action = do_filter_whitelist(client_req,ip,whitelists)
	if action is not None:
		return action

	action = do_filter_rule_list(client_req,compiled_rules)

	return action

'''
还原ChunkedEncoding消息，防止bypass
'''
def rebuild_chunked_encoding(msg):

	if "transfer-encoding: chunked" not in msg.lower():
		return msg
	else:
		try:
			headers,body = msg.split("\n\n",1)
		except:
			try:
				headers,body = msg.split("\r\n\r\n",1)
			except:
				return msg

		data = re.split(r"[0-9]+;.*",body)

		new_msg = ''
		for each in data:
			new_msg += each.replace("\r",'').replace("\n",'')

		print(new_msg)
		return new_msg

'''
从数据库中的规则列表匹配
默认放行
'''
def do_filter_rule_list(msg,compiled_rules):

	line = msg.split("\n")[0]
	
	log("根据规则判断",0)
	log(line,0)

	if not line:
		print(msg)
	# 短路判断，默认放行
	for each in compiled_rules:
		rule,action = each[0], each[1]
		if re.search(rule,msg) is not None:
			log("action:"+action,1)
			return action
	log("no rules matched,PASS\n",1)
	return C.ACTION_PASS

'''
从黑名单匹配
'''
def do_filter_blacklist(msg,ip,blacklists):

	log("根据黑名单判断")

	line = msg.split('\n')[0]
	url = line.split(" ")[1]

	log("ip:{},url:{}".format(ip,url))

	for item in blacklists:
		if (url.startswith(item[0]) or item[0] == "*") and (ip == item[1] or item[1] == "*"):
			log("在黑名单里")
			return C.ACTION_BLOCK
	
	return None


'''
从白名单匹配
'''
def do_filter_whitelist(msg,ip,whitelists):

	log("根据白名单判断")

	line = msg.split('\n')[0]
	url = line.split(" ")[1]

	log("ip:{},url:{}".format(ip,url))

	for item in whitelists:
		if (url.startswith(item[0]) or item[0] == "*") and (ip == item[1] or item[1] == "*"):
			log("在白名单里",1)
			return C.ACTION_PASS
	
	return None
