# 节流：

<br />

## 解释

> 控制事件发生的频率，**基于时间的频率来进行抽样更改**

- 重在**加锁**

## 应用场景

- scroll 事件，每隔一秒计算一次位置信息等
- 浏览器播放事件，每隔一秒计算一次进度信息等

```JavaScript
const throttle = (fn, wait) => {
    let timer

    return (...args) => {
        if(timer) return

        timer = setTimeout(() => {
            fn(...args)
            timer = null
        }, wait)
    }
}
```
