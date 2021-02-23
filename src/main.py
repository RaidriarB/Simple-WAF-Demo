import socket,sqlite3

from threading import Thread,Lock
from importlib import reload

from filter import do_filter
from response import do_response
from log import do_log
import config as C
from utils import log

import common

# 全局变量，代理主socket和连接池
proxy_server_socket = None
proxy_conn_pool = []

# 全局变量，数据库连接
db_conn = None

# 互斥锁
lock = Lock()

'''
处理请求
'''
def handle_socket(client_conn):

	BUF_SIZE = 2048 # 缓冲区大小
	client_req = ''
	client_conn.settimeout(C.CLIENT_SOCKET_TIMEOUT)
	try:
		# 缓冲区不满说明读取完毕，否则还应继续读取
		while True:
			buf = client_conn.recv(BUF_SIZE).decode('utf-8')
			client_req += buf
			if len(buf) < BUF_SIZE:
				break
		log("接收到请求:\n------\n" + client_req + '\n------',1)

	except Exception as e:
		print("超时了，接收到的信息如下\n-------\n"+client_req+"\n------")
		print(e)
		return
	
	if not client_req:
		log("出现空请求，丢弃",1)
		return

	ip = client_conn.getpeername()[0]
	log("请求ip:"+ip,1)

	action = do_filter(client_req,ip,common.compiled_rules,common.blacklists,common.whitelists)
	do_response(client_conn,client_req,action)
	log("-----------请求处理完毕。---------",1)

'''
WAF核心模块控制连接，用于异步更新、确认存活等
'''
def handle_controller():

	log("已经开启控制连接",1)

	# 初始化 server socket
	controller_server_socket = socket.socket()
	controller_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	controller_server_socket.bind(("0.0.0.0", C.CONTROLLER_PORT))
	controller_server_socket.listen(1024)

	while True:
		conn,addr = controller_server_socket.accept()

		log("建立控制连接",1)
		log(str(conn.getpeername())+"-->"+str(conn.getsockname()),1)

		thread = Thread(target = handle_ctlmsg, args=(conn,))
		thread.setDaemon(True)
		thread.start()

	log("控制连接出错",2)

'''
处理控制信息
'''
def handle_ctlmsg(conn):
	msg = ''
	BUF_SIZE = 1024
	try:
		# 缓冲区不满说明读取完毕，否则还应继续读取
		while True:
			buf = conn.recv(BUF_SIZE).decode('utf-8')
			msg += buf
			if len(buf) < BUF_SIZE:
				break
		log("接收到控制信息: " + msg ,1)
	except Exception as e:
		print("超时了，接收到的信息如下:"+msg)
		print(e)
		conn.close()
		return

	if not msg:
		log("出现空请求，丢弃",1)
		conn.close()
		return

	msg = msg.strip()

	if msg == C.CONTROL_UPDATE:

		import common
		reload(common)

		conn.sendall("FINISHED".encode())
		conn.close()
		log("完成规则更新",1)
	elif msg == C.CONTROL_CONFIRM:
		conn.sendall(C.CONTROL_CONFIRM.encode())
		conn.close()
		log("心跳包，确认存活",0)
	else:
		conn.sendall("INVALID COMMAND".encode())
		conn.close()
		log("非法信息！",2)


'''
初始化工作、代理主循环
将连接放入连接池，并创建新线程处理
TODO:与管理端的交互，热更新规则
'''
def proxy_main_loop():

	# 初始化 serversocket
	proxy_server_socket = socket.socket()
	proxy_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	proxy_server_socket.bind(("0.0.0.0", C.PROXY_PORT))
	proxy_server_socket.listen(1024)

	# 开启控制线程
	control_thread = Thread(target = handle_controller)
	control_thread.setDaemon(True)
	control_thread.start()

	while True:
		# 每来一个连接创建新线程，加入连接池
		client_conn, addr = proxy_server_socket.accept()
		proxy_conn_pool.append(client_conn)

		log("建立连接",1)
		log(str(client_conn.getpeername())+"-->"+str(client_conn.getsockname()),1)

		thread = Thread(target = handle_socket, args=(client_conn,))
		thread.setDaemon(True)
		thread.start()

def __main__():
	proxy_main_loop()

if __name__ == "__main__":
	__main__()