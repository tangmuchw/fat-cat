# bind

> bind() 方法创建一个新的函数，在 bind() 被调用时，这个新函数的 this 被指定为 bind()的第一个参数，而其余参数将作为新函数的参数，供调用时使用

## 注意点

- bind()除了 this 还接收其他参数，bind()返回的函数也接收参数，这两部分的参数都要传给返回的函数
- new 的优先级： 如果 bind 绑定后的函数被 new 了
  ，那么此时 this 指向就发生改变，this 就是当前函数的实例
- 没有保留原函数在原型链上的属性和方法

```JavaScript
 Function.prototype._bind = function(thisArg, args){
      if(typeof this !== 'function'){
         throw new TypeError('Bind must be called on a function')
         return
     }

     const me = this

     // new 优先级
     const bindFn = function(){
        // 判断是否用 new 调用 bindFn，决定最终的this指向
        // this instanceof me：判断bindFn是否被当作构造函数（new调用）
        // 是new调用：this指向bindFn的实例，此时this应该绑定到实例本身
        // 不是new调用：this绑定到传入的thisArg
        // 参数拼接：绑定阶段的args + 调用阶段的arguments（实现柯里化）
         me.apply(this instanceof me ? this : thisArg, args.concat(Array.prototype.slice.call(arguments)))
     }

     // 让绑定后的函数继承原函数的原型（保证实例能访问原函数原型的属性）
     bindFn.prototype = Object.create(me.prototype)

    // 返回绑定后的新函数（bind的核心特性：不立即执行，返回新函数）
     return bindFn
 }

function Person(name) {
  this.name = name;
}
const obj = { name: 'test' };
const BindPerson = Person._bind(obj);

// 普通调用：this指向obj
BindPerson('张三');
console.log(obj.name); // 张三

// new调用：this指向实例，obj不受影响
const p = new BindPerson('李四');
console.log(p.name); // 李四
console.log(obj.name); // 张三
```
