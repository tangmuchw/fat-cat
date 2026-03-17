# apply

> apply()方法调用一个具有给定 this 的函数，以及作为一个数组（或类似数组对象）提供参数

SyntaxError

```JavaScript
Function.prototype._apply = function(thisArg, args){
// 类型校验：确保调用_apply的必须是函数
    if(typeof this !== 'function') {
        throw new TypeError('Apply must be called on a function')
        return
    }

    // 创建唯一标识的Symbol，避免覆盖 thisArg 原有属性
    const fn = Symbol('fn')

    // 处理thisArg：如果传 null/undefined，默认绑定 window（浏览器环境）
    const me = thisArg || window
    // 把当前要执行的函数挂载到me（目标this）上
    me[fn] = this // 这里的this是调用_apply的函数（比如fn._apply()中的fn）

    // 执行函数：用扩展运算符把args数组拆成参数，绑定me作为this
    const result = me[fn](...args)

    delete me[fn]
    return result
}

// 测试函数
function sum(a, b) {
    console.log('this 指向：', this);
    return a + b;
}

// 测试1：绑定this到自定义对象
const obj = { name: 'test' };
const result1 = sum._apply(obj, [10, 20]);
console.log(result1); // 输出：this指向：{ name: 'test' }  30

// 测试2：不传thisArg，默认绑定window
const result2 = sum._apply(null, [5, 5]);
console.log(result2); // 输出：this指向：window  10
```
