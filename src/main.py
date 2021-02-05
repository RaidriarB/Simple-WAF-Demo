import socket,sqlite3

from threading import Thread

from filter import do_filter,init_filter
from response import do_response
from log import do_log
import constants as C
from utils import log

# 全局变量，代理主socket和连接池
proxy_server_socket = None
proxy_conn_pool = []

# 全局变量，编译好的规则列表
compiled_rules = None

# 全局变量，数据库连接
db_conn = None

def handle(client_conn):

	log("开了个新线程")
	client_req = ''
	client_conn.settimeout(C.CLIENT_SOCKET_TIMEOUT)

	try:
		# 缓冲区不满说明读取完了，否则还应继续读取
		while 1:
			buf = client_conn.recv(2048).decode('utf-8')
			client_req += buf
			if len(buf) < 2048:
				break

		log("接收到请求\n" + client_req)

	except Exception as e:
		print("超时了，接收到的信息如下\n"+client_req)
		print(e)
		return
	
	if not client_req:
		log("出现空请求，丢弃")
		return

	action = do_filter(client_req,compiled_rules)
	do_response(client_conn,client_req,action)

def proxy_main_loop():

	# 初始化规则
	global compiled_rules
	compiled_rules = init_filter()

	# 初始化 server socket
	proxy_server_socket = socket.socket()
	proxy_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	proxy_server_socket.bind((C.PROXY_HOST, C.PROXY_PORT))
	proxy_server_socket.listen(1024)

	while True:
		# 每来一个连接创建新线程，加入连接池
		client_conn, addr = proxy_server_socket.accept()
		proxy_conn_pool.append(client_conn)
		thread = Thread(target = handle, args=(client_conn,))
		thread.setDaemon(True)
		thread.start()

def __main__():
	proxy_main_loop()

if __name__ == "__main__":
	__main__()