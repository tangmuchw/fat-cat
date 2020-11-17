# 跨站请求伪造 CSRF（Cross Site Request Forgery）: 通过盗用用户的身份信息，以你的名义向第三方网站发起恶意请求。

<br />

### 防御手段：

- 将 cookie 设置为 HttpOnly： cookie 设置 HttpOnly 属性，JS 脚本就无法读取到 cookie 中的信息，避免攻击者伪造 cookie 的情况出现
- 增加 token
