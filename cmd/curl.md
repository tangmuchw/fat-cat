# curl

`curl` 是命令行下强大的网络请求工具，支持 HTTP/HTTPS/FTP 等多种协议，常用于接口调试、文件传输、网络排查。下面按功能分类介绍最常用参数，附示例与场景说明。

---

### 一、基础请求参数（最常用）

#### `-X, --request <method>`

指定 HTTP 请求方法（GET/POST/PUT/DELETE 等）。

```bash
curl -X POST https://api.example.com/login
curl -X DELETE https://api.example.com/user/123
```

#### `-d, --data <data>`

发送 POST 请求数据（表单/JSON），默认 `Content-Type: application/x-www-form-urlencoded`。

```bash
# 表单数据
curl -d "username=admin&password=123456" https://api.example.com/login
# JSON 数据（需配合 -H）
curl -d '{"name":"张三","age":25}' -H "Content-Type: application/json" https://api.example.com/user
```

#### `-H, --header <header>`

添加自定义请求头（认证、内容类型、Cookie 等）。

```bash
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" https://api.example.com/protected
curl -H "Content-Type: application/json" -H "Accept: application/json" https://api.example.com
```

#### `-L, --location`

自动跟随 HTTP 重定向（3xx 状态码）。

```bash
curl -L https://example.com/redirect
```

#### `-I, --head`

仅发送 HEAD 请求，只获取响应头（不下载响应体）。

```bash
curl -I https://www.baidu.com
```

---

### 二、输出控制参数

#### `-o, --output <file>`

将响应内容保存到指定文件。

```bash
curl -o page.html https://www.example.com
```

#### `-O, --remote-name`

用 URL 中的文件名保存（自动提取文件名）。

```bash
curl -O https://example.com/file.zip
```

#### `-i, --include`

输出包含响应头（默认只输出响应体）。

```bash
curl -i https://api.example.com/status
```

#### `-s, --silent`

静默模式，不显示进度条和错误信息。

```bash
curl -s https://api.example.com/data
```

#### `-w, --write-out <format>`

自定义输出格式（常用于性能统计）。

```bash
# 输出 DNS 解析、连接、总耗时
curl -o /dev/null -s -w "time_namelookup: %{time_namelookup}\ntime_connect: %{time_connect}\ntime_total: %{time_total}\n" https://www.baidu.com
```

---

### 三、文件传输参数

#### `-F, --form <name=content>`

表单上传（multipart/form-data），支持文件上传。

```bash
# 上传文件
curl -F "file=@/path/to/photo.jpg" https://api.example.com/upload
# 表单字段 + 文件
curl -F "title=测试图片" -F "file=@photo.jpg" https://api.example.com/upload
```

#### `-T, --upload-file <file>`

上传文件到 FTP/HTTP 服务器。

```bash
curl -T localfile.txt ftp://user:pass@example.com/upload/
```

#### `-C, --continue-at <offset>`

断点续传（下载大文件中断后继续）。

```bash
curl -C - -O https://example.com/largefile.zip
```

---

### 四、认证与安全参数

#### `-u, --user <user:password>`

基础认证（Basic Auth）。

```bash
curl -u admin:123456 https://api.example.com/admin
```

#### `-k, --insecure`

忽略 SSL 证书验证（测试环境用，生产不推荐）。

```bash
curl -k https://self-signed.example.com
```

#### `--cacert <file>`

指定 CA 证书文件（验证 HTTPS 证书）。

```bash
curl --cacert /path/to/ca.crt https://secure.example.com
```

---

### 五、调试与高级参数

#### `-v, --verbose`

详细输出（请求头、响应头、握手过程），调试必备。

```bash
curl -v https://api.example.com/debug
```

#### `--trace <file>`

输出完整请求/响应日志（含二进制），比 `-v` 更详细。

```bash
curl --trace trace.log https://api.example.com
```

#### `-A, --user-agent <agent>`

设置 User-Agent（模拟浏览器/客户端）。

```bash
curl -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0" https://www.example.com
```

#### `-b, --cookie <data/file>`

发送 Cookie（字符串或文件）。

```bash
curl -b "sessionid=abc123" https://example.com/dashboard
curl -b cookies.txt https://example.com
```

#### `-c, --cookie-jar <file>`

保存响应 Cookie 到文件。

```bash
curl -c cookies.txt https://example.com/login
```

---

### 六、常用组合示例

1. **POST JSON + 认证 + 跟随重定向**

```bash
curl -X POST -L \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer token" \
  -d '{"key":"value"}' \
  https://api.example.com/submit
```

2. **下载文件 + 断点续传 + 静默**

```bash
curl -C - -O -s https://example.com/largefile.zip
```

3. **接口性能测试**

```bash
curl -o /dev/null -s -w "状态码: %{http_code}\n总耗时: %{time_total}s\n" https://api.example.com
```

---

### 七、参数速查表

| 参数    | 作用           | 典型场景             |
| :------ | :------------- | :------------------- |
| `-X`    | 指定请求方法   | POST/PUT/DELETE 接口 |
| `-d`    | 发送 POST 数据 | 表单/JSON 提交       |
| `-H`    | 自定义请求头   | 认证、内容类型       |
| `-L`    | 跟随重定向     | 短链接、3xx 跳转     |
| `-o/-O` | 保存文件       | 下载资源             |
| `-F`    | 表单上传       | 文件上传接口         |
| `-v`    | 详细调试       | 排查请求异常         |
| `-k`    | 忽略证书       | 自签名 HTTPS 测试    |
| `-u`    | 基础认证       | 需要账号密码的接口   |

需要我把这些参数整理成一份可直接复制的 **curl 常用命令模板**（含 GET/POST/上传/下载/调试）吗？
