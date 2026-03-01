# Duration 类型

> Duration 表示的是“时间段” —— 两个时间点之间的差

- 以 纳秒 为单位

```go
const (
    Nanosecond Duration = 1
    Microsecond = 1000 * Nanosecond
    Millisecond = 1000 * Microsecond
    Second = 1000 * Millisecond
    Minute = 60 * Second
    Hour = 60 * Minute
)

a := 25 * time.Second // 25 秒
b := 10 * time.Minute // 10 分钟
c := 3 * time.Hour // 3 小时


```
