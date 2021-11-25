# DNS 劫持

> DNS 提供服务用来将域名转换成 IP 地址，然而在早期协议的设计中并没有太多考虑其安全性

- 对于查询方来说：
  - 我去请求的真的是一个 DNS 服务器吗？是不是别人冒充的？
  - 查询的结果有没有被人篡改过？这个 IP 真是这个网站的吗？

## 防御手段

> 使用 HttpDNS