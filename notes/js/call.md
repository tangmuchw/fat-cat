# call
>> call()方法使用一个指定的this值和单独给出的一个或多个参数来调用一个函数

## 原理
>> 由于函数的 this 指向它的直接调用者，因此变更调用者即完成 this 指向


```JavaScript
 Function.prototype._call = function(thisArg, ...args){
     if(typeof this !== 'function'){
         throw new TypeError('Call must be called on a function')
         return
     }

     const fn = Symbol('fn')
     caller = thisArg || window

    
     caller[fn] = this // this 指向调用call的对象, 即改变this指向的函数
     
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