# 请求方法

## http/1.1 规定了以下请求方法

- GET：请求获取 Request-URL 所标识的资源
- POST：在 Request-URL 所标识的资源后附加新的数据
- HEAD：请求获取由 Request-URL 所标识的资源的响应消息报头
- PUT：请求服务器存储一个资源，并用 Request-URL 作为起标识（修改数据）
- DELETE：请求服务器删除对应所标识的资源
- TRACE：请求附曲奇会送收到的请求信息，主要用于测试或诊断
- CONNECT：建立连接隧道，用于代理服务器
- OPTIONS： 列出可对资源实行的请求方法，用来跨域请求

> GET 和 POST 的区别

- 从缓存角度：GET 请求后浏览器会主动缓存，POST 默认情况下不会
- 从参数角度：GET 请求一般放在 URL 中，因此不安全；POST 请求放在请求体中，相对而言较为安全，但是在抓包的情况下都是一样的
- 从编码角度：GET 请求只能经行 URL 编码，只能接受 ASCII 码，而 POST 支持更多的编码类型且不对数据类型限值
- GET 请求幂等，POST 请求不幂等。（幂等指发送 M 和 N 次请求，两者不相同且大于 1，服务器资源的状态一致）
- 从 TCP 的角度，GET 请求会一次性发送请求报文；POST 请求通常分为两个 TCP 数据包，首先发 header 部分，如果服务器响应 100（continue），然后发 body 部分
- 从应用场景：GET 多用于无副作用，幂等的场景，例如搜索关键字；POST 多用于副作用，不幂等的场景

## 复杂请求

- 使用方法 put 或者 delete
- 发送 json 格式饿数据（content-type: application/json）
- 请求中带有自定义头部

## options 请求

> 跨域请求中，options 请求是浏览器自发起的 preflight request (预检请求)，以检测实际请求是否可以被浏览器接受

### preflight request 请求报文中有两个需要关注的首部字段

- Access-Control-Request-Method: 告知服务器实际请求所使用的 HTTP 方法
- Access-Control-Request-Headers: 告知服务器实际请求所携带的自定义首部字段

### 为什么跨域的复杂请求需要 preflight request?

> 复杂请求可能对服务器数据产生副作用。

- 例如 delete 或者 put ，都会对服务器数据进行修改
- 所以在请求之前都要先询问服务器，当前网页所在域名是否在服务器的许可名单中，服务器允许后，浏览器才会发出正式的请求，否则不发送正式请求
