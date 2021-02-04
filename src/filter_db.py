import os
import re

import constants as C
import dbutils
from utils import log


conn = None

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
			print(rule)

	log("规则加载完毕。",1)
	return compiled_rules

def do_filter(client_req,compiled_rules):
	# TODO:
	# TrunkedEncoding 还原
	action = do_filter_rule_list(client_req,compiled_rules)
	# TODO:
	# 接下来还需要黑白名单判断
	return action

def rebuild_trunked_encoding(msg):
	# TODO
	pass

# 从规则列表中匹配
def do_filter_rule_list(msg,compiled_rules):

	# 短路判断，默认放行
	for each in compiled_rules:
		rule,action = each[0], each[1]
		if re.search(rule,msg) is not None:
			log("action:"+action,1)
			return action
	log("no rules matched,pass\n",1)
	return C.ACTION_PASS

def do_filter_blacklist():
	pass

def do_filter_whitelist():
	pass

def test():
	compiled_rules = init_filter()
	log("inited.\n",1)

test()