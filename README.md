# WAF-Core

![yUIymd.png](https://s3.ax1x.com/2021/02/08/yUIymd.png)

一个基于python原生socket的简单云WAF项目，可以根据正则定义的规则进行流量过滤和日志记录，支持漏报误报设置，并具有Web管理端。

所有的配置都写在`src/config.py`中

## 部署到远程

```
docker run -it python -v `pwd`/.:/app /bin/bash -p 9000:9000 -p 12345:12345 -p 8000:8000
cd app
python3 -m venv .venv
python3 -m pip install -r requirements.txt
./start.sh
```





## 项目结构简介

main.py为入口，编写了代理核心循环和控制连接。在控制连接中，程序监听socket控制端口获取控制信息，进行热更新操作；在核心循环中，程序调用请求的解析与匹配（filter.py）、请求的处理动作（response.py、log.py）。

filter.py中包含解析与匹配的逻辑。解析部分进行了编码还原工作；匹配部分进行了规则匹配、黑白名单匹配等工作。response.py中，根据不同的action（PASS、BLOCK、LOG）决定不同的动作，封装在不同函数中，其中调用了日志记录模块log.py。

剩下的文件中，config.py中记录了项目的一系列全局参数；utils.py中包含了一个可以根据不同级别输出信息的log工具；dbutils用于操作数据库，common.py包含了三个全局变量，用于热更新。

## 开发人员合作

如果没有更改`src/config.py`，访问`127.0.0.1:9999`为代理，`127.0.0.1:12345`是控制连接，`127.0.0.1:8000`是Django的测试服务器。

整个项目的数据模型都使用Django自带的Model自动生成，数据库文件在`/src_frontend/db.sqlite3`中。

### 部署到本地

首先clone项目

```
git clone https://github.com/RaidriarB/Simple-WAF-Demo.git
cd Simple-WAF-Demo
```

项目依赖于python虚拟环境，以下为配置方法

```
# 首次创建虚拟环境，需要执行下面两条
python3 -m venv .venv


# 使用虚拟环境的话，每新打开一个shell都要输入下面命令
# Mac/Linux下
source .venv/bin/activate
# Windows下
.venv/bin/activate.bat

# 安装依赖
pip install -r requirements.txt
```

接下来就可以启动项目了。

启动代理核心模块：

```
cd src
python main.py
```

启动Django模块（同样需要虚拟环境）：

```
cd src_frontend
python manage.py runserver
```

然后访问`host:port`就可以了。
### 编写功能

如果之前没有的话，创建并进入一个自己的分支:`git switch -c <your-branch-name>`
然后在这个分支上本地开发、调试、提交，形成稳定版本。
如果想把这个分支推送到远程（比如让其他人看看这个分支），使用`git push origin <your-branch-name>`

需要与远程主分支合并时，首先要在主分支下`git pull`，若有冲突需要解决，然后进行分支合并`git merge --no-ff -m "message" <your-branch-name>`。建议这里禁用Fast Forward（即 --no-ff 选项）
最后推送`git push origin main`

### 重要配置说明

其余配置请参见`src/config.py`中的参数说明。

```python
# 调试级别
# -1 自闭 不输出任何信息
# 0 包括白色正常信息全都输出
# 1 输出1级绿色debug及以上信息
# 2 只输出2级红色warning信息
DEBUG_LEVEL = 0

# 本地测试还是部署到服务器
# 会改变代理的端口、主机等信息
LOCAL_DEBUG = True

# 控制连接的监听端口
CONTROLLER_PORT = 12345
```

### 快速测试控制连接

使用ncat工具即可

```
nc 127.0.0.1 12345
# 然后发送
<-UPDATE->
# 或者发送心跳包
<-CONFIRM->
```