# call

> call()方法使用一个指定的 this 值和单独给出的一个或多个参数来调用一个函数

## 原理

> 由于函数的 this 指向它的直接调用者，因此变更调用者即完成 this 指向

```JavaScript
 Function.prototype._call = function(thisArg, ...args){
     if(typeof this !== 'function'){
         throw new TypeError('Call must be called on a function')
         return
     }

     const fn = Symbol('fn')
     caller = thisArg || window

     caller[fn] = this // this 指向调用call的对象, 即改变this 指向的函数

     const result = caller[fn](...arg) // 执行当前函数

     delete caller[fn] // 删除声明的fn属性
     return result
 }

 // ==================
 //变更函数调用者示例
 function foo() {
    console.log(this.name)
 }

 // 测试
 const obj = {
    name: 'hello word'
 }
 obj.foo = foo   // 变更foo的调用者
 obj.foo()       // 'hello word'

 foo._call(obj) // 输出'hello word'
```

## 在转换 class extent 语法时会在转换后的 ES5 代码里注入 extent 辅助函数用于实现继承:

```JavaScript
    function _extend(target) {
        for(var i = 1; i < arguments.length; i++) {
            var source = arguments[i]
            for(var key in source) {
                if(Object.prototype.hasOwnProperty.call(source, key)) target[key] = source[key]
            }
        }

        return target
    }
```
