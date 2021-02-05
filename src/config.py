'''
常量和配置信息
'''

# 调试级别
# -1 自闭 不输出任何信息
# 0 包括白色正常信息全都输出
# 1 输出1级绿色debug及以上信息
# 2 只输出2级红色warning信息
DEBUG_LEVEL = 0

# 被代理的真实地址和端口
# 如果在本机，直接写127.0.0.1即可
REAL_HOST = '47.105.47.47'
REAL_PORT = 8000

# 代理服务器的工作地址和端口
# 即用户访问的地址和端口
PROXY_HOST = '127.0.0.1'
PROXY_PORT = 9999

# 每个客户端发起的连接timeout
CLIENT_SOCKET_TIMEOUT = 10

# 动作状态码的定义
ACTION_BLOCK = "BLOCK"
ACTION_PASS = "PASS"
ACTION_LOG = "LOG"

# 使用文件存放规则的目录
RULE_PATH = "../rules/"

# 数据库信息
## 数据库位置
DATABASE_PATH = "../db/data.db"
## 数据库表名
DB_NAME_RULES = "rules"
DB_NAME_LOGS = "log"
DB_NAME_FULL_LOG = "full_log"
## 数据库表中字段名
DB_TABLE_RULES = "(action,content,description)"
DB_TABLE_LOGS = "(time,ip,url,action)"
DB_TABLE_FULL_LOG = "(log_id,content)"