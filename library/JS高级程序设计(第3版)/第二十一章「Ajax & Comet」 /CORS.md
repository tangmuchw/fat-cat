[toc]

# CORS 跨域资源共享

> 默认情况下，XHR 对象只能访问与包含它的页面位于同一个域中的资源

> CORS（Cross-Origin Resource Sharing）: 其背后的基本思想，就是使用自定义的 HTTP 头部让浏览器与服务器进行沟通，从而决定请求或响应是应该成功，还是应该失败

- Access-Control-Allow-Origin

## IE 对 CORS 的实现

> 微软在 IE8 中引入了 XDR（XDomainRequest）类型。

### XDR 特点

- cookie 不会随请求发送, 也不会随响应返回
- 只能设置请求头部信息中的 Content-Type 字段
- 不能访问响应头部信息
- 只支持 GET 和 POST 请求
