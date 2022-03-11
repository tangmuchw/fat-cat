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
