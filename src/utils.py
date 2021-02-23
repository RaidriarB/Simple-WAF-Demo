'''
一些常用的小工具，包括日志
'''

import config as C


'''
一个日志输出工具，可以指定级别。
0:正常白色输出 1:debug级别绿色 2:warning级别红色
设置全局选项DEBUG_LEVEL，可以决定日志显示的类别
'''
def log(message,level=0,):

	prefix0 = ""
	prefix1 = "\033[1;32m[+] "
	prefix2 = "\033[1;31m[!] "

	output = ""

	if level == 0:
		output = prefix0 + message
	elif level == 1:
		output = prefix1 + message
	elif level == 2:
		output = prefix2 + message
	else:
		raise ValueError("level cannot be "+level+".")

	if C.DEBUG_LEVEL <= level:
		print(output)

	# 还原颜色
	print("\033[0m",end='')
