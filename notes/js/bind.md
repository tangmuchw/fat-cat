# bind
>> bind() 方法穿件一个新的函数，在bind() 被调用时，这个新函数的this被指定为bind()的第一个参数，而其余参数将作为新函数的参数，供调用时使用

## 注意点
- bind()除了this还接收其他参数，bind()返回的函数也接收参数，这两部分的参数都要传给返回的函
- new的优先级： 如果bind绑定后的函数被new了
，那么此时this指向就发生改变，this就是当前函数的实例
- 没有保留原函数在原型链上的属性和方法

```JavaScript
 Function.prototype._bind = function(thisArg, args){
      if(typeof this !== 'function'){
         throw new TypeError('Call must be called on a function')
         return
     }

     const me = this

     // new 优先级
     const fnBind = function(){
         me.apply(this instanceof me ? this : thisArg, args.concat(Array.prototype.slice.call(arguments)))
     }

     // 继承原型上的属性和方法
     fnBind.prototype = Object.create(me.prototype)

     return fnBind
 }
```