# 跨站请求伪造 CSRF（Cross Site Request Forgery）

> 通过盗用用户的身份信息，以你的名义向第三方网站发起恶意请求

- 核心思想：在打开 A 网站的情况下，另开 Tab 页面打开恶意网站 B，此时在 B 页面的“唆使”下，浏览器发起一个对网站 A 的 HTTP 请求

## 防御手段：

- 将 cookie 设置为 HttpOnly： cookie 设置 HttpOnly 属性，JS 脚本就无法读取到 cookie 中的信息，避免攻击者伪造 cookie 的情况出现
- 增加 token
