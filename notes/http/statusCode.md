# 状态码

> [状态码详见](https://cloud.tencent.com/developer/section/1190186)

[TOC]

## 100 Continue

> 表明目前为止的所有内容都是正常的，并且客户端应该继续请求或者如果它已经完成则忽略它

## 200 OK

> 指示请求已成功。200 响应默认是可缓存的

## 300 Multiple Choices

> 指示该请求具有多个可能的响应

- 用户代理或用户应该选择其中的一个。由于没有选择其中一个响应的标准方式，因此此响应代码很少使用。

## 301 Moved Permanently

> 指示所请求的资源**已明确**移动到 <code>Location</code> 标题给定的 <code>URL</code>

- 有时可能会被错误地更改为 <code>GET</code> 方法
- 浏览器重定向到这个页面，搜索引擎更新它们到资源的链接（在 SEO 中，据说链接汁被发送到新的 URL）

## 302 Found

> 指示所请求的资源**已暂时**移动到 <code>Location</code> 标题给定的 <code>URL</code>

- **妥协处理**，允许请求方法从 <code>POST/PUT</code> 改为 <code>GET</code>
  - eg: 使用 302，一些老客户错误地将方法改变为 GET：使用非 GET 方法的行为，然后 302 在 Web 上不可预知。
- 浏览器重定向到这个页面，但是搜索引擎不会更新他们到资源的链接（在 SEO 中，据说链接不会被发送到新的 URL）

## 303 See Other

> 表示重定向不链接到新上载的资源，而是链接到其他页面，如确认页面或上载进度页面。用于显示此重定向页面的方法**始终**为<code>GET</code>, 属于**临时重定向**

- **重定向状态代码通常作为一个 <code>PUT</code> 或 <code>POST</code> 操作的结果发回**

## 304 Not Modified

> 指示不需要重新传输请求的资源。这是对缓存资源的隐式重定向。

- [见 http 缓存](./cache.md)

## 307 Temporary Redirect

> 指示所请求的资源已暂时移动到 <code>Location</code> 标题给定的 <code>URL</code>

- 原始请求的方法和主体被重用来执行重定向的请求。即**不允许浏览器修改请求方法**

## 308 Permanent Redirect

> 指示所请求的资源已明确移动到 Location 标题给定的 URL

- 请求方法和主体不会被更改
- 浏览器重定向到这个页面，搜索引擎更新它们到资源的链接（在 SEO 中，据说链接被发送到新的 URL）

> [301 与 308 的区别？ 302, 303 和 307 的区别？](../questions/byteDance/basic.md)

## 400 Bad Request

> 指示服务器无法理解请求。客户不应未经修改就重复此请求

## 401 Unauthorized

> 指示该请求尚未应用，因为它缺少目标资源的有效认证凭证。

## 403 Forbidden

> 指示服务器理解请求但拒绝授权

## 404 Not Found

> 指示服务器找不到请求的资源

## 500 Internal Server

> 指示服务器遇到阻止它履行请求的意外情况

## 502 Bad Gateway

> 指示服务器充当网关或代理时收到来自上游服务器的无效响应

## 503 Service Unavailable

> 指示服务器尚未准备好处理请求

## 504 Gateway Timeout

> 指示服务器充当网关或代理时无法及时得到响应

## 426 Upgrade Required

> 客户端错误响应代码指示服务器拒绝使用当前协议执行请求，但可能在客户端升级到其他协议后愿意这样做。服务器发送一个 Upgrade 包含此响应的头部以指示所需的协议。

```HTTP
HTTP/1.1 426 Upgrade Required
Upgrade: HTTP/3.0
Connection: Upgrade
Content-Length: 53
Content-Type: text/plain

This service requires use of the HTTP/3.0 protocol

```
