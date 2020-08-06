# 在ES5环境下实现 const
>> 实现const的关键在于Object.defineProperty()这个API

>> Object.defineProperty(obj, prop, descriptor)


## descriptor
| 属性描述符 | 说明 | 默认值 |
| ---- | ---- | ---- |
| value | 该属性对应的值。可以是任何有效的 JavaScript 值（数值，对象，函数等） | undefined |
| get | 属性的 getter 函数 | undefined |
| set | 属性的 setter 函数 | undefined |
| writable | 当且仅当该属性的writable为true时，value才能被赋值运算符改变。默认为false | false |
| enumerable | enumerable定义了对象的属性是否可以在 for...in 循环和 Object.keys() 中被枚举 | false |
| configurable | 当且仅当该属性的 configurable 键值为 true 时，该属性的描述符才能够被改变，同时该属性也能从对应的对象上被删除 | false |


```JavaScript
    function _const(key, value) {
        var descriptor = {
            value,
            writeable: false
        }

        Object.defineProperty(window, key, descriptor)
    }

    _const('data', { list: 1 })
    data.tree = 2 //可以正常给 data 的属性赋值
    data = {} // 抛出错误，提示对象read-only
```