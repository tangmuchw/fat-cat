[toc]

# HTTPS 细节介绍

> HTTPS 就是在安全的传输层上发送 HTTP

- HTTP 安全层是通过 SSL（Secure Sockets Layer 安全套接字协议）及其现代替换协议 TLS（Transport Layer Security 传输层安全性协议） 来实现的

## SSL 握手

> 在发送已加密的 HTTP 报文之前，客户端和服务器要进行一次 SSL 握手，在这个握手过程中，它们完成以下工作

- 交换协议版本号
- 选择一个两端都了解的密码
- 对两端的身份进行认证
- 生成临时的会话密钥，以便加密信道
