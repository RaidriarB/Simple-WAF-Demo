'''
常量和配置信息
'''

# 调试级别
# -1 自闭 不输出任何信息
# 0 包括白色正常信息全都输出
# 1 输出1级绿色debug及以上信息
# 2 只输出2级红色warning信息
DEBUG_LEVEL = 0

# 本地测试还是部署到服务器
# 会改变代理的端口、主机等信息
LOCAL_DEBUG = False

# 控制连接的监听端口
CONTROLLER_PORT = 12345


################################################################
# 常量部分

# 动作状态码的定义
ACTION_BLOCK = "BLOCK"
ACTION_PASS = "PASS"
ACTION_LOG = "LOG"

# 控制端信号：更新规则
CONTROL_UPDATE = "<-UPDATE->"
# 控制端信号：确认存活
CONTROL_CONFIRM = "<-CONFIRM->"

################################################################
# 代理的主机和端口配置
if LOCAL_DEBUG:
	# 被代理的真实地址和端口
	# 如果在本机，直接写127.0.0.1即可
	REAL_HOST = '47.105.47.47'
	REAL_PORT = 8000

	# 代理服务器的工作地址和端口
	# 即用户访问的地址和端口
	PROXY_HOST = '127.0.0.1'
	PROXY_PORT = 9999
else:
	# 被代理的真实地址和端口
	# 如果在本机，直接写127.0.0.1即可
	REAL_HOST = '127.0.0.1'
	REAL_PORT = 8000

	# 代理服务器的工作地址和端口
	# 即用户访问的地址和端口
	PROXY_HOST = '47.105.47.47'
	PROXY_PORT = 80

################################################################
# 其他配置

# 每个客户端发起的连接timeout
CLIENT_SOCKET_TIMEOUT = 10

################################################################
# 数据库配置
## Django 数据库位置
DATABASE_PATH = "../src_frontend/db.sqlite3"
## Django 数据库表名
DB_NAME_RULES = "waf_rule"
DB_NAME_LOGS = "waf_log"
DB_NAME_FULL_LOG = "waf_fulllog"
DB_NAME_WHITELIST = "waf_whitelist"
DB_NAME_BLACKLIST = "waf_blacklist"
## Django 数据库表中字段名
DB_TABLE_RULES = "(action,content,description)"
DB_TABLE_LOGS = "(time,ip,url,action)"
DB_TABLE_FULL_LOG = "(log_id,content)"
DB_TABLE_WHITELIST = "(url,ip)"
DB_TABLE_BLACKLIST = "(url,ip)"
################################################################