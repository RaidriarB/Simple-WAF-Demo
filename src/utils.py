import constants as C

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

# 修改文件中某一行
def edit_line(file,lineno,newline):
	# 删除文件第n行
	import os
	cur_line = 0
	try:
		newfile = file+'.bak'
		with open(newfile,'w+')as f:
			for k in open(file,'r'):
				cur_line += 1
				if cur_line == lineno:
					f.write(newline+'\n')
				else:
					f.write(k)
		os.remove(file)
		os.rename(newfile,file)	
		return True
	except:
		# 失败，回滚
		os.remove(newfile)
		return False

# 删除文件中某一行
def delete_line(file,lineno):
	return edit_line(file,lineno,'')

