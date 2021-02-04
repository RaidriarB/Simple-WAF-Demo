import socket
from threading import Thread

from filter import do_filter,init_filter

# 被代理的真实地址和端口
REAL_HOST = '47.105.47.47'
REAL_PORT = 8000
# REAL_HOST = 'blog.arklight.xyz'
# REAL_PORT = 80

# 代理服务器的工作地址和端口
PROXY_HOST = '127.0.0.1'
PROXY_PORT = 1025

# 每个客户端发起的连接的timeout
client_socket_timeout = 2

# 状态码
ACTION_BLOCK = "BLOCK"
ACTION_PASS = "PASS"
ACTION_LOG = "LOG"

# 全局变量，代理主socket和连接池
proxy_server_socket = None
proxy_conn_pool = []

# 全局变量，编译好的规则列表
compiled_rules = None

def do_log():
	pass

def do_response(client_conn,proxy_req,action):
	if action == ACTION_PASS:
		do_response_pass(client_conn,proxy_req)
	elif action == ACTION_BLOCK:
		do_response_block(client_conn,proxy_req)
	elif action == ACTION_LOG:
		print("log")
		pass
	else:
		pass

def do_response_pass(client_conn,client_req):
	# 开始代理请求
	proxy_req = client_req.replace(PROXY_HOST+':'+str(PROXY_PORT), REAL_HOST+':'+str(REAL_PORT))\
		.replace('keep-alive', 'close').replace('gzip','')

	print("替换后的请求\n"+proxy_req.split("\n",1)[0])

	proxy_client_socket = socket.socket()
	proxy_client_socket.connect((REAL_HOST, REAL_PORT))
	proxy_client_socket.sendall(proxy_req.encode())

	target_resp = b''
	while 1:
		try:
			buf = proxy_client_socket.recv(1024*8)
		except socket.timeout as e:
			print(e)
			break

		target_resp += buf
		if not buf or buf.startswith(b'WebSocket') and buf.endswith(b'\r\n\r\n'):
			break

	proxy_resp = target_resp.replace(b'Content-Encoding: gzip\r\n', b'')\
		.replace(REAL_HOST.encode(), (PROXY_HOST+':'+str(PROXY_PORT)).encode())

	client_conn.sendall(proxy_resp)
	client_conn.close()

def do_response_block(client_conn,client_req):

	block_message = b'HTTP/1.1 200 OK\r\nHost: 127.0.0.1:1025\r\nDate: Tue, 02 Feb 2021 11:18:17 GMT\r\nConnection: close\r\nX-Powered-By: PHP/7.3.22-(to be removed in future macOS)\r\nContent-type: text/html; charset=UTF-8\r\n\r\nWAF Blocked!'

	client_conn.sendall(block_message)
	client_conn.close()

	print("waf blocked")

def handle(client_conn):
	client_req = ''
	client_conn.settimeout(client_socket_timeout)

	try:
		# 缓冲区不满说明读取完了，否则还应继续读取
		while 1:
			buf = client_conn.recv(2048).decode('utf-8')
			client_req += buf
			if len(buf) < 2048:
				break

		print("原始请求\n" + client_req.split("\n",1)[0])
	except:
		print("超时了，接收到的信息如下\n"+client_req)
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
	proxy_server_socket.bind((PROXY_HOST, PROXY_PORT))
	proxy_server_socket.listen(1024)

	while True:
		# 每来一个连接开新线程
		client_conn, addr = proxy_server_socket.accept()

		print(addr)
		# 加入连接池
		proxy_conn_pool.append(client_conn)

		thread = Thread(target = handle, args=(client_conn,))
		thread.setDaemon(True)
		thread.start()

def __main__():
	proxy_main_loop()

if __name__ == "__main__":
	__main__()