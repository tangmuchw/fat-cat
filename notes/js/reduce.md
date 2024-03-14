# reduce

> reduce 方法对数组中的每一个元素执行一个自定义函数 reducer，将其结果汇总为单个返回值
> array.reducer(function(total, currentValue, currentIndex, arr), initialValue)

```JavaScript
Array.prototype._reduce = function(fn, initialValue){
    const arr = this

    let total = initialValue !== null || initialValue !== undefined ? initialValue : arr[0],
        startIdx = initialValue !== null || initialValue !== undefined ? 1 : 0

    const len = arr.length
    for(let i = startIdx; i < len; i++) {
        const currentValue = arr[i]
        total = fn(total, currentValue, i, arr)
    }

    return total
}
```
