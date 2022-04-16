# DNS 解析

> DNS: Domain Name System
> 可参考书籍[计算机网络（原书第 7 版）](https://book.douban.com/subject/30280001/)

## DNS 服务器类型分类

- 根 DNS 服务器：其作用是管理它的下一级，即 TLD DNS 服务器。
  - <code>com</code>、<code>cn</code>、<code>org</code>与<code>edu</code> 等为顶级域名
  - 通过询问根 DNS 服务器，可以知道一个主机名对应的 TDL DNS 服务器的 IP 是多少，从而继续向 TDL DNS 服务器发起查询请求
- 顶级域（Top-level Domain，TLD） DNS 服务器：其作用提供了它的下一级，即权威 DNS 服务器的 IP 地址
- 权威 DNS 服务器：其作用是返回 主机-IP 的最终映射

## QA

### TLD 一定知道权威 DNS 服务器的 IP 么？

- 不一定。有时 TLD 只是知道中间的某个 DNS 服务器，再由这个中间 DNS 服务器去找到权威 DNS 服务器。
