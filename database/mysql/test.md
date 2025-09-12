启动 RPC 服务:

bash
cd service/rpc/user
go run user.go -f etc/user.yaml
启动 API 服务:

bash
cd service/api
go run user.go -f etc/user-api.yaml
12. 测试 API
使用 curl 测试登录接口:

bash
# 注册用户
curl -X POST -H "Content-Type: application/json" -d '{"username":"testuser","password":"testpass","email":"test@example.com"}' http://localhost:8888/api/user/register

# 用户登录
curl -X POST -H "Content-Type: application/json" -d '{"username":"testuser","password":"testpass"}' http://localhost:8888/api/user/login


