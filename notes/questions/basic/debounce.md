#防抖：
<br />

## 解释

>>防止抖动，单位时间内事件触发会被重置，避免事件被误伤触发多次

- 代码实现重在**清零**

## 应用场景
- 调整浏览器窗口大小
- 文本编辑起实时保存

```JavaScript
const debounce = (f, wait) => {
    let timer

    return (...args) => {
        timer && clearTimeout(timer)

        timer = setTimeout(() => {
            f(...args)
        }, wait)
    }
}
```