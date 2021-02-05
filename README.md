# WAF-Core
文档待会再写。

一个基于python原生socket的简单云WAF项目，可以根据正则定义的规则进行流量过滤和日志记录，支持漏报误报设置，并具有Web管理端。

所有的配置都写在`config.py`中

使用方法：
```
git clone https://github.com/RaidriarB/ByteDanceProject-WAF-core.git
cd ByteDanceProject-WAF-core
chmod +x ./start-waf
./start-waf
```

然后访问`host:port`就可以了。

