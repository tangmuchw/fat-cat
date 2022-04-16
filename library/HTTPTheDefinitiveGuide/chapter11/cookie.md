[toc]

# Cookie

> cookie 分为会话 cookie 和持久 cookie

- 会话 cookie 是一种临时 cookie，它记录了用户访问站点时的设置和偏好，用户退出浏览器时，会话 cookie 会被删除
- 持久 cookie 的生存时间更长一点，它存储在磁盘中，通用用于维护某个用户周期性访问站点的配置文件和登录名

## 其缺点

- 存储大小限制为 4KB
- http 请求时需要发送到服务器，增加请求数量
- 只能用 document.cookie = '...' 来修改，太过简陋
