# nslookup

nslookup 就是用来查「域名对应哪个 IP」的工具

```sh
nslookup github.com

Server:		192.168.31.1 # 你当前用的 DNS 服务器（一般是路由器）
Address:	192.168.31.1#53 # DNS 服务默认端口 53

Non-authoritative answer: # 不是权威 DNS 直接回答，是缓存结果
Name:	github.com
Address: 20.205.243.166
```
