import socket

import config as C
from utils import log
from log import do_log

'''
根据动作代码决定处理方法
'''
def do_response(client_conn,proxy_req,action):
	if action == C.ACTION_PASS:
		do_response_pass(client_conn,proxy_req)
	elif action == C.ACTION_BLOCK:
		do_response_block(client_conn,proxy_req)
	elif action == C.ACTION_LOG:
		log("log it",1)
		do_response_log(client_conn,proxy_req)
	else:
		log("action not supported!",2)

'''
动作是PASS，放行
'''
def do_response_pass(client_conn,client_req):

	ip = client_conn.getpeername()[0]

	proxy_addr = C.PROXY_HOST+':'+str(C.PROXY_PORT)
	real_addr = C.REAL_HOST+':'+str(C.REAL_PORT)

	proxy_req = client_req.replace(proxy_addr, real_addr)\
		.replace('keep-alive', 'close').replace('gzip','')

	proxy_client_socket = socket.socket()
	proxy_client_socket.connect((C.REAL_HOST, C.REAL_PORT))
	proxy_client_socket.sendall(proxy_req.encode())

	target_resp = b''
	while 1:
		try:
			buf = proxy_client_socket.recv(1024*8)
		except socket.timeout as e:
			log(e)
			break

		target_resp += buf
		if not buf:
			break
	
	log("服务器回应：\n",1)
	print(target_resp[:300])

	proxy_resp = target_resp.replace(b'Content-Encoding: gzip\r\n', b'')\
		.replace((real_addr).encode(), (proxy_addr).encode())

	client_conn.sendall(proxy_resp)
	client_conn.close()

	do_log(client_req,ip,C.ACTION_PASS,full=False)

'''
动作是LOG
'''
def do_response_log(client_conn,client_req):

	ip = client_conn.getpeername()[0]

	proxy_addr = C.PROXY_HOST+':'+str(C.PROXY_PORT)
	real_addr = C.REAL_HOST+':'+str(C.REAL_PORT)

	proxy_req = client_req.replace(proxy_addr, real_addr)\
		.replace('keep-alive', 'close').replace('gzip','')

	proxy_client_socket = socket.socket()
	proxy_client_socket.connect((C.REAL_HOST, C.REAL_PORT))
	proxy_client_socket.sendall(proxy_req.encode())

	target_resp = b''
	while 1:
		try:
			buf = proxy_client_socket.recv(1024*8)
		except socket.timeout as e:
			log(e)
			break

		target_resp += buf
		if not buf:
			break
	
	log("服务器回应：\n",1)
	print(target_resp[:300])

	proxy_resp = target_resp.replace(b'Content-Encoding: gzip\r\n', b'')\
		.replace((real_addr).encode(), (proxy_addr).encode())

	client_conn.sendall(proxy_resp)
	client_conn.close()
	
	do_log(client_req,ip,C.ACTION_LOG,full=True)

'''
动作是BLOCK，拦截
'''
def do_response_block(client_conn,client_req):

	ip = client_conn.getpeername()[0]

	block_message = 'HTTP/1.1 200 OK\r\nHost: 127.0.0.1:1025\r\nDate: Tue, 02 Feb 2021 11:18:17 GMT\r\nConnection: close\r\nX-Powered-By: PHP/7.3.22-(to be removed in future macOS)\r\nContent-type: text/html; charset=UTF-8\r\n\r\n访问不合法！已被拦截和记录。'.encode("utf-8")

	client_conn.sendall(block_message)
	client_conn.close()

	log("waf blocked",1)
	do_log(client_req,ip,C.ACTION_BLOCK,full=True)
