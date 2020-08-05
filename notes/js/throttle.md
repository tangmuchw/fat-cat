#节流：
<br />

## 解释

>>控制事件发生的频率
- 重在**加锁**

## 应用场景
- scroll事件，每隔一秒计算一次位置信息等
- 浏览器播放事件，每隔一秒计算一次进度信息等

```JavaScript
const throttle = (f, wait) => {
    let timer

    return (...args) => {
        if(timer) return

        timer = setTimeout(() => {
            f(...args)
            timer = null
        }, wait)
    }
}
```