# 跨站请求伪造CSRF（Cross Site Request Forgery）: 通过盗用用户的身份信息，以你的名义向第三方网站发起恶意请求。
<br />

### 防御手段：
 - 将cookie设置为HttpOnly： cookie设置HttpOnly属性，JS脚本就无法读取到cookie中的信息，避免攻击者伪造cookie的情况出现
 - 增加token