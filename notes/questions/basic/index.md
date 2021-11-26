[toc]

# 箭头函数与普通函数区别？能不能作为构造函数？

- 最大的区别其实就是 this 指向

* 箭头函数没有自己的 this，箭头函数的 this 指向**在定义时候**继承**自外层的一个普通函数**的 this，永远不会改变

- 箭头函数没有 prototype， 所以箭头函数本身没有 this
- 箭头函数不能作为构造函数使用
- 箭头函数不绑定 arguments，取而代之用 rest 参数...代替 arguments 对象，来访问箭头函数的参数列表

```JavaScript
const getRest = (...params) => {
    console.log(params)
}
```

- 箭头函数不能作 Generator 函数，不能使用 yield 关键字

# 如何让 (a == 1 && a ==2 && a == 3) 返回 true

```JavaScript
const a = {
    val: 1,
    toString: function(){
        return a.val++
    },
    // valueOf: function(){
    //     return a.val++
    // }
}

// 利用 Proxy，可以将读取属性的操作（get），转变为执行某个函数，从而实现属性的链式操作
// const a = new Proxy({ val: 1}, {
//     get(target){
//         return () => target.val++
//     }
// })

console.log(a == 1 && a ==2 && a == 3) // true

```

# 检查输出值

```JavaScript
function wrapFunction(func) {
    return function () {
        const args = Array.prototype.slice.call(arguments);
        func.apply(args)
    }
}
const ins = {
    method: (
        () => { return wrapFunction(function () { console.log(this) }) }
    )()
}

ins.method(10)
```
