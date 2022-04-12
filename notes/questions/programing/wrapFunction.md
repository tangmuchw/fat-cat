# 检查输出值

```JavaScript
function wrapFunction(func) {
    return function () {
        // arguments 是一个对应于传递给函数的参数的类数组对象
        // 将 arguments 转换成普通数组
        const args = Array.prototype.slice.call(arguments);

        // args 绑定到 this
        func.apply(args)
    }
}
const ins = {
    method: (
        () => { return wrapFunction(function () { console.log(this) }) }
    )()
}

ins.method(10) // [10]
```
