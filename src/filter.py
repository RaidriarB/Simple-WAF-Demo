import os
import re

# 状态码
ACTION_BLOCK = "BLOCK"
ACTION_PASS = "PASS"
ACTION_LOG = "LOG"

RULE_PATH = "../rules/"

def init_filter():

	print("正在加载规则...")

	compiled_rules = []

	# 加载规则列表
	rule_filenames = []
	file_lst = os.walk(RULE_PATH).__next__()[2]

	for file in file_lst:
		# print(file)
		if file.endswith(".rule"):
			rule_filenames.append(file)

	for rule_file_name in rule_filenames:

		with open(RULE_PATH + rule_file_name,'r') as rule_file:
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
						action = ACTION_BLOCK
					elif action == "PASS":
						action = ACTION_PASS
					elif action == "LOG":
						action = ACTION_LOG
					else:
						raise Exception()

					compiled_rule = (re.compile(regexp),action)
				except:
					print("编译出错，出错的行为\n"+rule)
				compiled_rules.append(compiled_rule)
			print("规则文件{}加载完毕。".format(rule_file_name))
	return compiled_rules

def do_filter(client_req,compiled_rules):
	action = do_filter_rule_list(client_req,compiled_rules)
	# 接下来还需要黑白名单判断
	return action

# 从规则列表中匹配
def do_filter_rule_list(msg,compiled_rules):

	# print(msg)

	for each in compiled_rules:
		rule,action = each[0], each[1]
		if re.search(rule,msg) is not None:
			print(action+"\n")
			return action
	
	print("no rules matched,pass\n")
	return ACTION_PASS

def do_filter_blacklist():
	pass

def do_filter_whitelist():
	pass

def test():
	compiled_rules = init_filter()
	print("inited.\n")