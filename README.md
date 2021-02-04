# WAF-Core
文档待会再写。

使用方法：
```
# 可能需要chmod一下
./start-waf
```

然后访问`http://127.0.0.1:1025`就可以了。

尝试一下`http://127.0.0.1:1025/student/gpa?id=evil`，应该被拦截