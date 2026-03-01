# Time 类型

> Time 结构体用来表示时间实例，精度为纳秒

- Now：获取当前的系统时间，返回 Time 实例
- Date：通过向函数传入参数来初始化 Time 实例

```go
var now = time.Now()

year, month, day := now.Date()

hour, minute, second := now.Clock()

```
