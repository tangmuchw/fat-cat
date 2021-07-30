[toc]

# TCP 传输

> TCP 流是分段的、又 IP 分组传送

- HTTP: 网络接口(数据链路层)， IP(网络层)， TCP(传输层)， HTTP(应用层)
- HTTPS: 网络接口(数据链路层)， IP(网络层)， TCP(传输层)， HTTP(应用层)，**TSL or SSL(安全层)**

## TPC 段

> 每个 TCP 段都是由 IP 分组承载，从一个 IP 地址发送到另一个 IP 地址的。
> 每个 IP 分组中都包括

- 一个 IP 分组首部(通常为 20 字节): 包含了源和目的 IP 地址、长度和其他一些标记
- 一个 TCP 段首部(通常为 20 字节): TCP 端口号、TCP 控制标记，以及用于数据排序和完整性检查的一些数字值
- 一个 TCP 数据块(0 个或多个字节)

## 保持 TCP 连接的正确运行

> TCP 连接是通过 4 个值来识别的: **<源 IP 地址、源端口号、目的 IP 地址、目的端口号、>**