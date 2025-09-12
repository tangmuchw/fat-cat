在 Docker 中运行 MySQL 5.7.40 是一个常见且高效的方式，特别适用于开发、测试甚至某些生产环境。下面我将为你详细介绍如何操作，包括安装步骤、配置说明以及一些实用技巧。

# Docker 部署 MySQL 5.7.40 指南

## ✨ 1. 拉取 MySQL 5.7.40 镜像

首先，你需要从 Docker Hub 拉取官方 MySQL 5.7.40 镜像。打开终端，执行以下命令：

```bash
docker pull mysql:5.7.40
```

如果未指定版本，Docker 会拉取最新的 MySQL 5.7 系列镜像。标签`5.7.40`、`5.7`、`5`通常指向同一版本。

## 📁 2. 创建宿主机目录

为了持久化 MySQL 的数据、配置和日志，需要在宿主机上创建相关目录：

```bash
mkdir -p /mydata/mysql/{data,conf,log}
```

-   `data`：用于存放数据库数据，避免容器删除后数据丢失。
-   `conf`：存放自定义配置文件。
-   `log`：存放 MySQL 日志文件。

## ⚙️ 3. 创建自定义配置文件

在`/mydata/mysql/conf`目录下创建自定义配置文件（如`custom.cnf`），以设置字符集等参数：

```bash
vim /mydata/mysql/conf/custom.cnf
```

以下是一个常见的配置示例，用于设置 UTF-8 编码：

```ini
[client]
default-character-set=utf8mb4

[mysql]
default-character-set=utf8mb4

[mysqld]
init_connect="SET collation_connection = utf8mb4_unicode_ci"
init_connect="SET NAMES utf8mb4"
character-set-server=utf8mb4
collation-server=utf8mb4_unicode_ci
skip-character-set-client-handshake
skip-name-resolve
```

## 🐳 4. 运行 MySQL 容器

使用以下命令启动 MySQL 容器：

```bash
docker run --name mysql \
-p 3306:3306 \
-v /mydata/mysql/conf:/etc/mysql/conf.d \
-v /mydata/mysql/data:/var/lib/mysql \
-v /mydata/mysql/log:/var/log/mysql \
-e MYSQL_ROOT_PASSWORD=123456 \
-d mysql:5.7.40
```

**参数说明**：

-   `--name mysql`：容器名称。
-   `-p 3306:3306`：将宿主机的 3306 端口映射到容器的 3306 端口。
-   `-v`：挂载目录，实现数据持久化。
-   `-e MYSQL_ROOT_PASSWORD=123456`：设置 MySQL root 用户的密码。
-   `-d`：后台运行容器。

## 🔒 5. 安全配置

为了提高安全性，建议禁用 root 账户的远程访问，并创建专用账户用于外部连接：

1.  **进入容器并登录 MySQL**：

    ```bash
    docker exec -it mysql bash
    mysql -u root -p
    ```

2.  **删除远程 root 访问权限**（如果存在）：

    ```sql
    DELETE FROM mysql.user WHERE user='root' AND host='%';
    FLUSH PRIVILEGES;
    ```

3.  **创建新用户并授权**（例如创建一个允许远程连接的用户）：
    ```sql
    CREATE USER 'newuser'@'%' IDENTIFIED BY 'userpassword';
    GRANT ALL PRIVILEGES ON *.* TO 'newuser'@'%' WITH GRANT OPTION;
    FLUSH PRIVILEGES;
    ```

## 🔧 6. 容器管理

-   **设置容器自启动**：

    ```bash
    docker update --restart=always mysql
    ```

-   **常用容器操作命令**：
    ```bash
    docker start mysql    # 启动容器
    docker stop mysql     # 停止容器
    docker restart mysql  # 重启容器
    docker rm mysql       # 删除容器（需先停止）
    ```

## 🗂️ 7. 验证部署

1.  **检查容器状态**：

    ```bash
    docker ps
    ```

2.  **连接 MySQL 数据库**：

    ```bash
    docker exec -it mysql mysql -u root -p
    ```

3.  **创建测试数据库**：
    ```sql
    CREATE DATABASE test_db;
    USE test_db;
    CREATE TABLE test_table (id INT, name VARCHAR(50));
    INSERT INTO test_table VALUES (1, 'Test');
    SELECT * FROM test_table;
    ```

## 💡 8. 高级配置与优化

### 8.1 配置优化

根据实际需求，你可以在`custom.cnf`中添加更多性能优化参数，例如：

```ini
[mysqld]
# 基础性能优化
server-id = 1
log-bin = mysql-bin
binlog-format = ROW
expire_logs_days = 7

# 内存相关
innodb_buffer_pool_size = 1G
innodb_log_file_size = 256M
innodb_flush_log_at_trx_commit = 1
innodb_file_per_table = 1

# 连接和超时设置
max_connections = 500
max_connect_errors = 6000
wait_timeout = 600
interactive_timeout = 600

# 其他优化
transaction_isolation = READ-COMMITTED
innodb_flush_method = O_DIRECT
innodb_lock_wait_timeout = 1800
skip-name-resolve
```

### 8.2 使用环境变量文件

对于生产环境，建议使用环境变量文件来管理敏感信息，避免在命令行历史中暴露密码：

1. 创建环境变量文件（如`mysql.env`）：

    ```
    MYSQL_ROOT_PASSWORD=your_secure_password
    MYSQL_DATABASE=my_app_db
    MYSQL_USER=app_user
    MYSQL_PASSWORD=app_user_password
    ```

2. 运行容器时使用`--env-file`参数：
    ```bash
    docker run --name mysql \
    -p 3306:3306 \
    -v /mydata/mysql/conf:/etc/mysql/conf.d \
    -v /mydata/mysql/data:/var/lib/mysql \
    -v /mydata/mysql/log:/var/log/mysql \
    --env-file /path/to/mysql.env \
    --restart=always \
    -d mysql:5.7.40
    ```

### 8.3 网络与安全配置

考虑使用自定义 Docker 网络增强安全性：

```bash
# 创建自定义网络
docker network create mysql-network

# 运行容器时加入该网络
docker run --name mysql \
--network mysql-network \
-p 3306:3306 \
# ...其他参数保持不变
```

这样可以将 MySQL 容器与其他服务隔离，只有同一网络中的容器才能直接访问 MySQL。

## 🚨 9. 常见问题与解决方法

1.  **权限问题**：如果遇到权限错误，尝试在运行容器时添加`--privileged=true`参数。
2.  **字符集问题**：确保配置文件中正确设置了字符集为`utf8mb4`，以支持所有 Unicode 字符（包括表情符号）。
3.  **端口冲突**：如果宿机的 3306 端口已被占用，可以更改映射端口，例如`-p 3307:3306`。
4.  **数据持久化**：确保挂载目录正确，避免容器删除后数据丢失。
5.  **忘记 root 密码**：
    -   停止 MySQL 容器：`docker stop mysql`
    -   使用跳过权限检查的方式启动新容器：
        ```bash
        docker run -it --rm \
        -v /mydata/mysql/data:/var/lib/mysql \
        mysql:5.7.40 \
        mysqld_safe --skip-grant-tables &
        ```
    -   连接到此容器并重置密码后，重新启动原容器。

## 📊 10. 监控与维护

### 10.1 日志查看

定期检查 MySQL 日志有助于发现问题：

```bash
# 查看容器日志
docker logs mysql

# 查看MySQL错误日志
tail -f /mydata/mysql/log/error.log
```

### 10.2 备份与恢复

定期备份是保障数据安全的重要措施：

```bash
# 备份数据库
docker exec mysql sh -c 'exec mysqldump --all-databases -uroot -p"$MYSQL_ROOT_PASSWORD"' > /path/to/backup/$(date +%Y%m%d).sql

# 恢复数据库
docker exec -i mysql sh -c 'exec mysql -uroot -p"$MYSQL_ROOT_PASSWORD"' < /path/to/backup/backupfile.sql
```

## 💎 总结

通过 Docker 部署 MySQL 5.7.40 提供了高度灵活性和便捷性。关键步骤包括：拉取指定版本镜像、合理配置数据持久化、调整性能参数、实施安全措施以及制定定期维护计划。这种部署方式不仅适合开发和测试环境，加上适当的配置和监控，也能满足生产环境的需求。

Docker 部署 MySQL 的优势包括环境一致性、快速部署和易于扩展。遵循最佳实践，如使用数据卷持久化数据、适当配置安全选项和定期备份，可以确保数据库的稳定性和安全性。

---

docker run --name mysql \
-p 3306:3306 \
-v /Users/tmchw/mydata/mysql/conf:/etc/mysql/conf.d \
-v /Users/tmchw/mydata/mysql/data:/var/lib/mysql \
-v /Users/tmchw/mydata/mysql/log:/var/log/mysql \
-e MYSQL_ROOT_PASSWORD=123456 \
-d mysql:5.7.40

docker exec -it some-mysql bash
mysql -u root -p

---

# 用户登录示例项目（基于 Go-Zero）

下面我将创建一个完整的用户登录示例项目，展示 go-zero 中 API、RPC 和 Model 层如何交互。

## 项目结构

```
user-login-demo/
├── api/
│   ├── user.api
│   ├── etc/
│   │   └── user-api.yaml
│   └── internal/
│       ├── config/
│       ├── handler/
│       ├── logic/
│       ├── svc/
│       └── types/
├── rpc/
│   ├── user/
│   │   ├── user.proto
│   │   ├── etc/
│   │   │   └── user.yaml
│   │   └── internal/
│   │       ├── config/
│   │       ├── logic/
│   │       ├── server/
│   │       └── svc/
└── model/
    ├── user.sql
    └── user.go
```

## 1. 数据库设计

首先创建用户表：

```sql
-- model/user.sql
CREATE TABLE `user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL DEFAULT '' COMMENT '用户名',
  `password` varchar(255) NOT NULL DEFAULT '' COMMENT '密码',
  `email` varchar(255) NOT NULL DEFAULT '' COMMENT '邮箱',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username_unique` (`username`),
  UNIQUE KEY `email_unique` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';
```

## 2. 生成 Model 层代码

```bash
# 生成 Model 代码
goctl model mysql ddl -url="root:123456@tcp(127.0.0.1:3306)/test" -table="user" -dir="./model" -c
```

这会生成包含基本 CRUD 操作的 Model 代码。

## 3. 定义 RPC 服务

创建 RPC 服务的 proto 文件：

```protobuf
// rpc/user/user.proto
syntax = "proto3";

package user;

option go_package = "./user";

message LoginRequest {
  string username = 1;
  string password = 2;
}

message LoginResponse {
  int64  id = 1;
  string username = 2;
  string email = 3;
  string token = 4;
}

message RegisterRequest {
  string username = 1;
  string password = 2;
  string email = 3;
}

message RegisterResponse {
  int64 id = 1;
}

service User {
  rpc Login(LoginRequest) returns (LoginResponse);
  rpc Register(RegisterRequest) returns (RegisterResponse);
}
```

生成 RPC 代码：

```bash
goctl rpc protoc user.proto --go_out=./ --go-grpc_out=./ --zrpc_out=.
```

## 4. 实现 RPC 服务逻辑

首先配置 RPC 服务：

```yaml
# rpc/user/etc/user.yaml
Name: user.rpc
ListenOn: 0.0.0.0:8080
DataSource: username:password@tcp(127.0.0.1:3306)/database
```

实现 RPC 服务逻辑：

```go
// rpc/user/internal/logic/loginlogic.go
package logic

import (
    "context"
    "errors"
    "strings"
    "time"

    "user-login-demo/model"
    "user-login-demo/rpc/user/internal/svc"
    "user-login-demo/rpc/user/user"

    "github.com/zeromicro/go-zero/core/logx"
    "golang.org/x/crypto/bcrypt"
)

type LoginLogic struct {
    ctx    context.Context
    svcCtx *svc.ServiceContext
    logx.Logger
}

func NewLoginLogic(ctx context.Context, svcCtx *svc.ServiceContext) *LoginLogic {
    return &LoginLogic{
        ctx:    ctx,
        svcCtx: svcCtx,
        Logger: logx.WithContext(ctx),
    }
}

func (l *LoginLogic) Login(in *user.LoginRequest) (*user.LoginResponse, error) {
    // 参数校验
    if len(strings.TrimSpace(in.Username)) == 0 {
        return nil, errors.New("用户名不能为空")
    }
    if len(in.Password) < 6 {
        return nil, errors.New("密码长度不能少于6位")
    }

    // 查询用户
    userInfo, err := l.svcCtx.UserModel.FindOneByUsername(l.ctx, in.Username)
    if err != nil {
        if err == model.ErrNotFound {
            return nil, errors.New("用户不存在")
        }
        return nil, err
    }

    // 验证密码
    err = bcrypt.CompareHashAndPassword([]byte(userInfo.Password), []byte(in.Password))
    if err != nil {
        return nil, errors.New("密码错误")
    }

    // 生成 token (这里简化处理，实际应用中应使用JWT等)
    token := generateToken(userInfo.Id)

    return &user.LoginResponse{
        Id:       userInfo.Id,
        Username: userInfo.Username,
        Email:    userInfo.Email,
        Token:    token,
    }, nil
}

func generateToken(userId int64) string {
    // 实际应用中应该使用JWT等标准方法生成token
    // 这里只是示例
    return fmt.Sprintf("token-%d-%d", userId, time.Now().Unix())
}
```

```go
// rpc/user/internal/logic/registerlogic.go
package logic

import (
    "context"
    "errors"
    "strings"
    "time"

    "user-login-demo/model"
    "user-login-demo/rpc/user/internal/svc"
    "user-login-demo/rpc/user/user"

    "github.com/zeromicro/go-zero/core/logx"
    "golang.org/x/crypto/bcrypt"
)

type RegisterLogic struct {
    ctx    context.Context
    svcCtx *svc.ServiceContext
    logx.Logger
}

func NewRegisterLogic(ctx context.Context, svcCtx *svc.ServiceContext) *RegisterLogic {
    return &RegisterLogic{
        ctx:    ctx,
        svcCtx: svcCtx,
        Logger: logx.WithContext(ctx),
    }
}

func (l *RegisterLogic) Register(in *user.RegisterRequest) (*user.RegisterResponse, error) {
    // 参数校验
    if len(strings.TrimSpace(in.Username)) == 0 {
        return nil, errors.New("用户名不能为空")
    }
    if len(in.Password) < 6 {
        return nil, errors.New("密码长度不能少于6位")
    }
    if !strings.Contains(in.Email, "@") {
        return nil, errors.New("邮箱格式不正确")
    }

    // 检查用户名是否已存在
    _, err := l.svcCtx.UserModel.FindOneByUsername(l.ctx, in.Username)
    if err == nil {
        return nil, errors.New("用户名已存在")
    } else if err != model.ErrNotFound {
        return nil, err
    }

    // 检查邮箱是否已存在
    _, err = l.svcCtx.UserModel.FindOneByEmail(l.ctx, in.Email)
    if err == nil {
        return nil, errors.New("邮箱已存在")
    } else if err != model.ErrNotFound {
        return nil, err
    }

    // 加密密码
    hashedPassword, err := bcrypt.GenerateFromPassword([]byte(in.Password), bcrypt.DefaultCost)
    if err != nil {
        return nil, err
    }

    // 创建用户
    newUser := &model.User{
        Username: in.Username,
        Password: string(hashedPassword),
        Email:    in.Email,
    }

    result, err := l.svcCtx.UserModel.Insert(l.ctx, newUser)
    if err != nil {
        return nil, err
    }

    userId, _ := result.LastInsertId()

    return &user.RegisterResponse{
        Id: userId,
    }, nil
}
```

## 5. 定义 API 服务

创建 API 定义文件：

```go
// api/user.api
type (
    LoginRequest {
        Username string `json:"username"`
        Password string `json:"password"`
    }

    LoginResponse {
        ID       int64  `json:"id"`
        Username string `json:"username"`
        Email    string `json:"email"`
        Token    string `json:"token"`
    }

    RegisterRequest {
        Username string `json:"username"`
        Password string `json:"password"`
        Email    string `json:"email"`
    }

    RegisterResponse {
        ID int64 `json:"id"`
    }
)

service user-api {
    @handler Login
    post /api/user/login (LoginRequest) returns (LoginResponse)

    @handler Register
    post /api/user/register (RegisterRequest) returns (RegisterResponse)
}
```

生成 API 代码：

```bash
goctl api go -api user.api -dir ./api
```

## 6. 实现 API 服务逻辑

配置 API 服务：

```yaml
# api/etc/user-api.yaml
Name: user-api
Host: 0.0.0.0
Port: 8888
UserRpc:
    Etcd:
        Hosts:
            - 127.0.0.1:2379
        Key: user.rpc
```

实现 API 逻辑：

```go
// api/internal/logic/loginlogic.go
package logic

import (
    "context"

    "user-login-demo/api/internal/svc"
    "user-login-demo/api/internal/types"
    "user-login-demo/rpc/user/user"

    "github.com/zeromicro/go-zero/core/logx"
)

type LoginLogic struct {
    logx.Logger
    ctx    context.Context
    svcCtx *svc.ServiceContext
}

func NewLoginLogic(ctx context.Context, svcCtx *svc.ServiceContext) *LoginLogic {
    return &LoginLogic{
        Logger: logx.WithContext(ctx),
        ctx:    ctx,
        svcCtx: svcCtx,
    }
}

func (l *LoginLogic) Login(req *types.LoginRequest) (*types.LoginResponse, error) {
    // 调用 RPC 服务的 Login 方法
    resp, err := l.svcCtx.UserRpc.Login(l.ctx, &user.LoginRequest{
        Username: req.Username,
        Password: req.Password,
    })
    if err != nil {
        return nil, err
    }

    return &types.LoginResponse{
        ID:       resp.Id,
        Username: resp.Username,
        Email:    resp.Email,
        Token:    resp.Token,
    }, nil
}
```

```go
// api/internal/logic/registerlogic.go
package logic

import (
    "context"

    "user-login-demo/api/internal/svc"
    "user-login-demo/api/internal/types"
    "user-login-demo/rpc/user/user"

    "github.com/zeromicro/go-zero/core/logx"
)

type RegisterLogic struct {
    logx.Logger
    ctx    context.Context
    svcCtx *svc.ServiceContext
}

func NewRegisterLogic(ctx context.Context, svcCtx *svc.ServiceContext) *RegisterLogic {
    return &RegisterLogic{
        Logger: logx.WithContext(ctx),
        ctx:    ctx,
        svcCtx: svcCtx,
    }
}

func (l *RegisterLogic) Register(req *types.RegisterRequest) (*types.RegisterResponse, error) {
    // 调用 RPC 服务的 Register 方法
    resp, err := l.svcCtx.UserRpc.Register(l.ctx, &user.RegisterRequest{
        Username: req.Username,
        Password: req.Password,
        Email:    req.Email,
    })
    if err != nil {
        return nil, err
    }

    return &types.RegisterResponse{
        ID: resp.Id,
    }, nil
}
```

## 7. 运行项目

1. 启动 etcd（用于服务发现）：

```bash
etcd
```

2. 启动 RPC 服务：

```bash
cd rpc/user
go run user.go -f etc/user.yaml
```

3. 启动 API 服务：

```bash
cd api
go run user.go -f etc/user-api.yaml
```

## 8. 测试接口

使用 curl 测试登录接口：

```bash
# 注册用户
curl -X POST -H "Content-Type: application/json" -d '{"username":"testuser","password":"password123","email":"test@example.com"}' http://localhost:8888/api/user/register

# 用户登录
curl -X POST -H "Content-Type: application/json" -d '{"username":"testuser","password":"password123"}' http://localhost:8888/api/user/login
```

## 总结

这个示例项目展示了 go-zero 中 API、RPC 和 Model 层的完整交互流程：

1. **API 层**：接收 HTTP 请求，参数校验，调用 RPC 客户端
2. **RPC 层**：处理业务逻辑，调用 Model 层进行数据操作
3. **Model 层**：封装数据库操作，提供数据访问接口

这种分层架构使得代码职责清晰，易于维护和扩展。在实际项目中，你还可以添加更多的功能，如 JWT 令牌验证、密码强度验证、邮件验证等。


