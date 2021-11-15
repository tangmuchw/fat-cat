# apply

> apply()方法调用一个具有给定 this 的函数，以及作为一个数组（或类似数组对象）提供参数

SyntaxError

```JavaScript
 Function.prototype._apply = function(thisArg, args){
     if(typeof this !== 'function') {
         throw new TypeError('Apply must be called on a function')
         return
     }

     const fn = Symbol('fn')

     const me = thisArg || window
     me[fn] = this // 这里的 this 指的是调用 apply 方法的构造函数

     const result = me[fn](...args)

     delete me[fn]
     return result
 }
```
