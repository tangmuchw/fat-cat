防止云服务器流量盗刷（如恶意刷量、CC 攻击、资源滥用）需要多层次防护策略。以下是全面解决方案：

---

### 一、基础防护措施

1. **防火墙配置**

    ```bash
    # 只开放必要端口（SSH/HTTP/HTTPS）
    sudo ufw allow 22/tcp
    sudo ufw allow 80/tcp
    sudo ufw allow 443/tcp
    sudo ufw enable
    ```

2. **修改 SSH 端口**

    ```bash
    sudo nano /etc/ssh/sshd_config
    # 修改 Port 22 → Port 2222
    sudo systemctl restart sshd
    sudo ufw allow 2222/tcp
    ```

3. **密钥登录+禁用密码**
    ```bash
    sudo nano /etc/ssh/sshd_config
    PasswordAuthentication no
    PermitRootLogin no
    ```

---

### 二、Web 应用防护（Nginx 为例）

1. **流量限制配置**

    ```nginx
    http {
       # 限制单个IP每秒10个请求
       limit_req_zone $binary_remote_addr zone=one:10m rate=10r/s;

       server {
           location / {
               # 突发流量缓冲20个请求
               limit_req zone=one burst=20 nodelay;
           }

           # 关键接口更严格限制
           location /api/ {
               limit_req zone=one burst=5;
           }
       }
    }
    ```

2. **封禁恶意 IP**

    ```bash
    # 手动封禁IP
    sudo iptables -A INPUT -s 123.123.123.123 -j DROP

    # 自动封禁工具
    sudo apt install fail2ban
    ```

---

### 三、高级防护方案

1. **启用 WAF（Web 应用防火墙）**

    - 免费方案：安装 **ModSecurity**
        ```bash
        sudo apt install libapache2-mod-security2 -y  # Apache
        sudo apt install nginx-module-security -y    # Nginx
        ```
    - 商业方案：阿里云 WAF/腾讯云 WAF/AWS Shield

2. **CDN 防护（推荐必做）**

    - 开启 Cloudflare 免费防护：
        - 开启"Under Attack Mode"
        - 配置防火墙规则：拦截可疑国家/IP 段
        - 启用 Bot Fight Mode
    - 国内 CDN：阿里云 DCDN/腾讯云 CDN

3. **API 接口防护**
    ```javascript
    // Express.js示例：添加验证码中间件
    app.post("/api/submit", (req, res) => {
        if (!validateCaptcha(req.body.captcha)) {
            return res.status(429).send("请求过于频繁");
        }
        // 正常业务逻辑
    });
    ```

---

### 四、实时监控与告警

1. **安装监控工具**

    ```bash
    # 实时流量监控
    sudo apt install vnstat
    vnstat -l

    # 进程级监控
    sudo apt install nmon
    ```

2. **云平台告警设置**
    - 创建告警规则：
        - 带宽 > 50Mbps 时通知
        - CPU > 90% 持续 5 分钟
        - 异常 HTTP 错误率

---

### 五、业务层防护策略

1. **关键操作验证**

    - 短信/邮件操作：添加图形验证码
    - 支付环节：强制二次密码验证

2. **用户行为分析**

    ```python
    # 示例：检测异常请求频率
    from flask_limiter import Limiter
    limiter = Limiter(key_func=get_remote_address)

    @app.route("/checkout")
    @limiter.limit("5 per minute")  # 每分钟5次
    def checkout():
        return process_payment()
    ```

3. **经济风控手段**
    - 优惠活动：设置单用户领取上限
    - 付费接口：添加小额支付验证

---

### 六、应急响应流程

1. **攻击识别**

    ```bash
    # 查看实时连接
    sudo netstat -tunlp | grep :80

    # 分析访问日志
    sudo tail -f /var/log/nginx/access.log | grep -E '404|500'
    ```

2. **快速止损**
    - 临时切换至 Cloudflare 的"5 秒盾"
    - 启用云平台的 DDoS 清洗服务
    - 临时关闭非核心服务

---

### 防护方案对比

| **防护层** | **免费方案**   | **商业方案** | **效果** |
| ---------- | -------------- | ------------ | -------- |
| 网络层     | iptables 封 IP | 云防火墙     | ★★★      |
| 应用层     | Nginx 限流     | WAF 服务     | ★★★★     |
| 业务层     | 验证码         | 行为分析系统 | ★★★★★    |
| 加速层     | Cloudflare     | 专业 CDN     | ★★★★     |

> 💡 **终极建议**：
>
> 1. **必做**：CDN + 基础防火墙 + Nginx 限流
> 2. **加强**：WAF + 行为验证码
> 3. **高阶**：接入专业风控系统如阿里云风控引擎

通过组合使用这些方案，可有效防御 99%的流量盗刷和恶意攻击，保障服务器稳定运行。
