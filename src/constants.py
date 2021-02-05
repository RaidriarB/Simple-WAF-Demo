
# 调试级别
# -1 自闭 不输出任何信息
# 0 全都输出
# 1 输出1级绿色及以上信息
# 2 只输出2级红色信息
DEBUG_LEVEL = 0

# 被代理的真实地址和端口
REAL_HOST = '47.105.47.47'
REAL_PORT = 8000

# 代理服务器的工作地址和端口
PROXY_HOST = '127.0.0.1'
PROXY_PORT = 9999

# 每个客户端发起的连接的timeout
CLIENT_SOCKET_TIMEOUT = 10

# 状态码
ACTION_BLOCK = "BLOCK"
ACTION_PASS = "PASS"
ACTION_LOG = "LOG"

# 规则目录
RULE_PATH = "../rules/"

# 数据库文件
DATABASE_PATH = "../db/test.db"
DB_NAME_RULES = "rules"
DB_NAME_LOGS = "log"
DB_NAME_FULL_LOG = "full_log"

DB_TABLE_RULES = "(action,content,description)"
DB_TABLE_LOGS = "(time,ip,url,action)"
DB_TABLE_FULL_LOG = "(log_id,content)"