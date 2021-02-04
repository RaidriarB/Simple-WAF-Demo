#coding= UTF-8
from __future__ import unicode_literals, print_function
import socket, sys, traceback, threading, time, select

MAX_HEADER_SIZE = 4096
RECV_SIZE = 512

def getHeader(string, name):
    name = name.upper()
    base, i, l = 0, 0, len(string)

    while i<l:
        # 根据约定，空行代表头的结束
        if string[i] == "\r" and i<l-1 and string[i+1] == "\n" : break
        # 找第一个冒号，拆解信息头
        while i<l and string[i] != ":" : i+=1
        # 判断信息头
        if i<l and string[base:i].strip().upper() == name:
            # 将base定位至冒号后面
            base = i+1
            # 找到行尾，获得信息
            while i<l and not(string[i] == "\n" and string[i-1] == "\r") : i+=1
            return string[base:i-1]
        else:
            # 找到行尾，跳过
            while i<l and not(string[i] == "\n" and string[i-1] == "\r") : i+=1
            base, i = i+1, i+1
    return None

def splitHeader(string):
    i, l = 3, len(string)
    while i<l and (string[i] != "\n" or string[i-3:i+1] !="\r\n\r\n") : i+=1
    return string[:i-3]

def transHost(raw_host):
    # 将raw_host解析为host和port
    for i in range(len(raw_host)): 
        if raw_host[i] == ":" : return raw_host[:i].strip(), int(raw_host[i+1:])
    else : return raw_host.strip(), 80

def recvBody(conn, base, size):
    if size==-1:
        while base[-5:] != "\r\n0\r\n\r\n" : base += conn.recv(RECV_SIZE)
    else:
        while len(base)<size:base += conn.recv(RECV_SIZE)
    return base


def thread_proxy(client, addr):

    thread_name = threading.currentThread().name

    print('%s->客户端接入:%s'%(thread_name, str(addr)))

    # 分离和分析请求头
    request = client.recv(MAX_HEADER_SIZE)
    requestHeader = splitHeader(request)
    # 请求头过长！
    if len(requestHeader)>MAX_HEADER_SIZE-11:
        print("%s->Host太长！限制长度为%ds"%(thread_name, MAX_HEADER_SIZE-11))
        client.close()
        return
    # 解析Host
    raw_host = getHeader(requestHeader, "Host")
    if not raw_host:
        print("%s->Host解析不正常%s"%(thread_name, str(addr)))
        print("%s->request_header:\n%s"%(thread_name, requestHeader))
        client.close()
        return
    host, port = transHost(raw_host)
    
    # 接受剩余Body
    if len(requestHeader) < len(request)-4:
        content_size = getHeader(requestHeader, "content-length")
        request = recvBody(client, request, len(requestHeader) + 4 + int(content_size) if content_size else -1)
    
    #建立 socket tcp 连接并发送原始请求头
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((host, port))
    #发送请求报文
    server.sendall(request)
   
    # 分离和分析响应头
    response = server.recv(MAX_HEADER_SIZE)
    responseHeader = splitHeader(response)
    # 响应头过长！
    if len(responseHeader)>MAX_HEADER_SIZE-11:
        print("%s->Header太长！限制长度为%ds"%(thread_name, MAX_HEADER_SIZE-11))
        server.close()
        client.close()
        return
    # 接受剩余Body
    if len(responseHeader) < len(response)-4:
        content_size = getHeader(responseHeader, "content-length")
        response = recvBody(server, response, len(responseHeader) + 4 + int(content_size) if content_size else -1)
    #发送响应报文
    client.sendall(response)

    server.close()
    client.close()

def thread_server(myserver):
    #循环接收不同ip，端口信息
    while True:
        conn, addr = myserver.accept()
        thread_p = threading.Thread(target=thread_proxy, args=(conn, addr))
        thread_p.setDaemon(True)
        thread_p.start()

# 启动server和监听退出命令
def main(_, port=8000):
    try:
        # 三行命令分别创建socket、绑定ip端口、设置排队数量
        myserver = socket.socket()
        myserver.bind(('127.0.0.1', port))
        myserver.listen(1024)
        # daemon命令用于让子线程跟随主线程一起结束
        thread_s = threading.Thread(target=thread_server, args=(myserver,))
        thread_s.setDaemon(True)
        thread_s.start()
        # 我也不知道这是什么奇葩做法。。。反正目的就是Ctrl+C可以终止程序然后阅读bug信息。。。
        while True: time.sleep(999)
    except KeyboardInterrupt:
        print("sys exit")
    finally:
        myserver.close()


# 命令入口
if __name__ == '__main__':
    try:
        print("start server")
        main(*sys.argv)
    except Exception as e:
        print("error exit")
        traceback.print_exc()
    finally:
        print("end server")
    sys.exit(0)
'''
实现了http1.1的服务器代理功能
其实现依赖于http请求头的固定格式
如请求中不包含Host信息，则终止代理过程
对于请求体和其它信息，本程序并没有做额外处理而是直接返回
对于http2.0所体现的持久连接，本程序尚未实现 - - - 其中的困难在于判断某个流是否结束
在参考资料中有一个想法是利用select实现端到端直传，从而让客户端和服务器自行判断是否结束
但我没有解决总是出现的阻塞卡死和死循环问题，这恐怕要向大佬们请教了
'''