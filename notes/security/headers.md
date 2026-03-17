# 安全头部与防护

Strict-Transport-Security (HSTS)：强制浏览器仅用 HTTPS 访问，防止降级攻击。
X-Content-Type-Options：防止 MIME 类型嗅探，避免恶意文件执行。
X-XSS-Protection：内置 XSS 过滤器，检测并阻断脚本注入。

## Strict-Transport-Security

```js
Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

说明
max-age=31536000：一年有效期
includeSubDomains：所有子域名也强制 HTTPS
always：即使是 301/404 也会返回头，更安全, Nginx 的附加参数

## X-Content-Type-Options

```js
X-Content-Type-Options "nosniff" always;
```

说明

- nosniff：字面意思是 “不要嗅探”：
    -   1. 对脚本 / 样式文件：浏览器只会按 Content-Type 解析（如 text/javascript 才会当脚本执行），就算文件内容是脚本，但 Content-Type 标为 text/plain，也不会执行；
    -   2. 对其他文件：避免恶意攻击者把可执行文件（如 JS、HTML）伪装成图片 / 文本文件，诱骗浏览器执行。
- always：即使是 301/404 也会返回头，更安全, Nginx 的附加参数

## X-XSS-Protection

```js
X-XSS-Protection "1; mode=block" always;
```

该响应头的核心参数（分两部分）：

1. 1：表示开启 XSS 过滤器（值为 0 则关闭）；
2. mode=block：表示一旦检测到 XSS 攻击，直接阻断整个页面加载
