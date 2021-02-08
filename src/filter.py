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
	failed_rules = []

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

'''
判断请求，返回动作代码
其中分为很多部分
'''
def do_filter(client_req,compiled_rules):

	client_req = rebuild_chunked_encoding(client_req)

	action = do_filter_rule_list(client_req,compiled_rules)
	# TODO:
	# 接下来还需要黑白名单判断
	return action

'''
还原TrunkedEncoding消息，防止bypass
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
def do_filter_blacklist():
	# TODO
	pass

'''
从白名单匹配
'''
def do_filter_whitelist():
	# TODO
	pass


def test():
	rebuild_trunked_encoding("header1\ntransfer-encoding: chunked\nheadern\n\n2;18f9*ja\n1' o\n6;f1dfsdv\nr 1=1")
test()