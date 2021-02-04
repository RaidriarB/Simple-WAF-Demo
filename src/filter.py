import os
import re

import constants as C
from utils import log

def init_filter():

	log("正在加载规则...",1)
	compiled_rules = []

	# 加载规则列表
	rule_filenames = []
	file_lst = os.walk(C.RULE_PATH).__next__()[2]

	for file in file_lst:
		# log(file)
		if file.endswith(".rule"):
			rule_filenames.append(file)

	for rule_file_name in rule_filenames:

		with open(C.RULE_PATH + rule_file_name,'r') as rule_file:
			rules = rule_file.read().split("\n")
			for rule in rules:
				rule = rule.strip()

				# 空行
				if not rule:
					continue

				# 注释
				if rule.startswith("#"):
					continue

				# 需要解析的行
				# example
				# BLOCK .*id=evil.*
				try:
					action,regexp = rule.split(" ")[0],rule.split(" ")[1]
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
					log("编译出错，出错的行为\n"+rule,2)
					
			log("规则文件{}加载完毕。".format(rule_file_name),1)
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