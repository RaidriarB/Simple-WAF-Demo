import socket

import constants as C
from utils import log

def do_response(client_conn,proxy_req,action):
	if action == C.ACTION_PASS:
		do_response_pass(client_conn,proxy_req)
	elif action == C.ACTION_BLOCK:
		do_response_block(client_conn,proxy_req)
	elif action == C.ACTION_LOG:
		log("log it",1)
		pass
	else:
		pass

def do_response_pass(client_conn,client_req):
	# 开始代理请求
	proxy_req = client_req.replace(C.PROXY_HOST+':'+str(C.PROXY_PORT), C.REAL_HOST+':'+str(C.REAL_PORT))\
		.replace('keep-alive', 'close').replace('gzip','')

	# log("替换后的请求\n"+proxy_req.split("\n",1)[0])

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
		if not buf or buf.startswith(b'WebSocket') and buf.endswith(b'\r\n\r\n'):
			break
	
	log("服务器回应：\n"+target_resp)

	proxy_resp = target_resp.replace(b'Content-Encoding: gzip\r\n', b'')\
		.replace(C.REAL_HOST.encode(), (C.PROXY_HOST+':'+str(C.PROXY_PORT)).encode())

	client_conn.sendall(proxy_resp)
	client_conn.close()

def do_response_block(client_conn,client_req):

	block_message = b'HTTP/1.1 200 OK\r\nHost: 127.0.0.1:1025\r\nDate: Tue, 02 Feb 2021 11:18:17 GMT\r\nConnection: close\r\nX-Powered-By: PHP/7.3.22-(to be removed in future macOS)\r\nContent-type: text/html; charset=UTF-8\r\n\r\nWAF Blocked!'

	client_conn.sendall(block_message)
	client_conn.close()

	log("waf blocked",1)


