# 部署静态网页到云服务器操作

## 密钥登录

> ssh -i ~/Downloads/key.pem ubuntu@123.123.123.123
> /usr/share/nginx/html

部署静态网页到云服务器是一个直接的过程，以下是详细步骤：

### 一、准备工作

1. **获取服务器信息**

    - IP 地址、SSH 端口（默认 22）
    - 用户名（如 `root` 或 `ubuntu`）
    - 密码或 SSH 密钥（推荐密钥登录更安全）

2. **准备网页文件**
    - 本地整理好网站文件（如 `index.html`、`css/`、`js/`、`images/` 等）

---

### 二、连接服务器

1. **通过 SSH 登录**
    ```bash
    ssh 用户名@服务器IP -p 端口号
    # 示例：ssh root@123.123.123.123
    ```
    - 首次登录需确认指纹
    - 使用密钥登录：添加 `-i 密钥路径` 参数

---

### 三、安装 Web 服务器（Nginx 为例）

1. **更新系统并安装 Nginx**

    ```bash
    sudo apt update && sudo apt upgrade -y  # Ubuntu/Debian
    sudo apt install nginx -y
    ```

2. **启动并设置开机自启**
    ```bash
    sudo systemctl start nginx
    sudo systemctl enable nginx
    ```

---

### 四、上传网页文件

#### 方法 1：SCP 命令（推荐）

```bash
# 本地终端执行（非服务器）
scp -r -P SSH端口 本地文件夹路径 用户名@服务器IP:/var/www/html/
# 示例：scp -r ./my_site root@123.123.123.123:/var/www/html/
```

#### 方法 2：SFTP 工具（如 FileZilla）

-   连接：协议选 `SFTP`，输入服务器信息
-   拖拽本地文件到服务器目录 `/var/www/html/`

---

### 五、配置 Nginx

1. **设置网站根目录**  
   编辑配置文件：

    ```bash
    sudo nano /etc/nginx/sites-available/default
    ```

    修改 `root` 路径（确保指向上传目录）：

    ```nginx
    server {
        listen 80;
        root /var/www/html;   # 确认此路径
        index index.html;
        server_name _;
    }
    ```

2. **测试并重启 Nginx**
    ```bash
    sudo nginx -t       # 检查配置语法
    sudo systemctl restart nginx
    ```

---

### 六、防火墙设置

```bash
sudo ufw allow 80/tcp   # 开放HTTP端口
sudo ufw allow 443/tcp  # 开放HTTPS（如需）
sudo ufw reload
```

---

### 七、访问网站

浏览器输入服务器 IP 地址，即可看到网页（如 `http://123.123.123.123`）

---

### 八、进阶配置（可选）

1. **域名绑定**

    - 在域名商处添加 A 记录解析到服务器 IP
    - 修改 Nginx 配置中的 `server_name`：
        ```nginx
        server_name yourdomain.com www.yourdomain.com;
        ```

2. **启用 HTTPS**  
   使用 Let's Encrypt 免费证书：

    ```bash
    sudo apt install certbot python3-certbot-nginx
    sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
    ```

3. **权限修正**  
   若遇到 403 错误：
    ```bash
    sudo chmod -R 755 /var/www/html
    sudo chown -R www-data:www-data /var/www/html
    ```

---

### 常见问题排查

-   **无法访问**：检查服务器安全组是否放行 80/443 端口
-   **403 错误**：确保 `index.html` 存在且 Nginx 有读取权限
-   **502 错误**：运行 `sudo systemctl status nginx` 查看日志

> 💡 **提示**：静态网站部署后，更新内容只需重新上传文件并重启 Nginx（`sudo systemctl reload nginx`）。

通过以上步骤，你的静态网站即可成功上线！
