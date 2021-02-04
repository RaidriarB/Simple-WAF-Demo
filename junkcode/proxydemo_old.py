from socketserver import BaseRequestHandler,ThreadingTCPServer

import threading, socket


block_message = b'HTTP/1.1 200 OK\r\nHost: 127.0.0.1:1025\r\nDate: Tue, 02 Feb 2021 11:18:17 GMT\r\nConnection: close\r\nX-Powered-By: PHP/7.3.22-(to be removed in future macOS)\r\nContent-type: text/html; charset=UTF-8\r\n\r\nWAF Blocked!'

proxy_host = '0.0.0.0'
proxy_port = 11113

real_host = '47.105.47.47'
real_port = 8000

def doFilter(req):
	# 检测请求
	# 这里比较复杂，需要读取规则、检测规则变更
	if b'evil' in req:
		return 'block'
	else:
		return 'pass'
	
	# 返回状态码

def doResponse(client,req,status):

	# 根据状态码决定动作

	if status == 'block':
		client.send(block_message)
		dolog(status,req)
	elif status == 'pass':
		proxy_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		proxy_client.connect((real_host,real_port))
		proxy_client.send(req)
		resp = proxy_client.recv(1<<29)
		with open("resplog.txt",'ab+') as f:
			f.write(resp)
		client.send(resp)
		client.close()
	else:
		pass


def dolog(req,status):
	# 记录日志
	pass

def proxy():
	'''
		http proxy main loop
		这样写不行的，是阻塞式，需要建个进程池
	'''
	proxy_server_socket_socket = socket.socket()
	proxy_server_socket.bind((proxy_host,proxy_port))
	proxy_server_socket.listen()
	while True:
		client,addr = proxy_server_socket.accept()
		req = client.recv(1<<29)
		with open("reqlog.txt",'ab+') as f:
			f.write(req)
		status = doFilter(req)
		doResponse(client,req,status)


def __main__():
	proxy()
	#server = ThreadingTCPServer(ADDR,Handler)
	#server.serve_forever()


if __name__ == '__main__':
	__main__()
	