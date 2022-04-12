# 编程 compose 实现

```JavaScript
/**
 * 解析实现
 * foo = (num) => add(multiply(num))
*/

const compose = (...funcs) => {
    if(!funcs.length) return (num) => { console.log(num) }

    return funcs.reduce((a, f) => (...arg) => a(f(...arg)))
}

// 问题描述
const add = num => num  + 10
const multiply = num => num * 2
const foo = compose(multiply, add)
console.log(foo(5)) // 30
```
