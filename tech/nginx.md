# nginx

## ubuntu 安装

> apt-get install nginx

## 查看 nginx log 日志

> /var/log/nginx/error.log

## 查询 nginx 主进程号

> ps -ef | grep nginx

## 重启 ng 两种方式

> systemctl restart nginx
> kill -HUP 主进程号或进程号文件路径
> service nginx restart
> /usr/local/nginx/sbin/nginx -s reload
> mac: nginx -s reload

location / {
proxy_pass http://extranet;

proxy_intercept_errors on;
error_page 404 = @fallback404;
}

location @fallback404 {
root /home/ubuntu/official-website-service/public;
index index.html index.htm;
try_files $uri = 404;
}

/usr/local/nginx/html

查看端口占用
netstat -anon | grep [端口]

杀掉占用的端口的进程
fuser -k [端口]/tcp

查看本机 ip
curl icanhazip.com

## 负载均衡

```Nginx
http {
    # upstream 模块来配置后端服务器群组
    # 使用 server 指令指定对应的地址和参数
    # 在 server 配置 proxy_pass 指令将请求转发到定义好的服务器群组
    # weight 参数，用于指定更高的权重，意味着在负载均衡中将更倾向于分配更多的请求给它
    upstream backend {
        server backend1.example.com;
        server backend2.example.com;
        server backend3.example.com;
        # 可以设置权重
        server backend4.example.com weight=2;
    }

    server {
        listen 80;

        location / {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```
