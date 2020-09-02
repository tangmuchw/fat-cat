# new运算符: 创建一个用户定义的兑现类型的实例，或具有构造函数的内置兑现的实例
<br />

## new关键字会进行如下的操作：
 - 创建一个空的全新JavaScript对象(即{})
 - 执行[[prototype]]链接, 即\_\_proto__链接（即设置该对象的构造函数，又叫设置原型链）
 - 使得**this**只想新创建的对象
 - 通过**new**创建的每个对象将最终被[[prototype]]连接到这个函数的[[prototype]]对象上
 - 如果函数没有返回对象类型[[Object]](包含[[Function]], [[Array]], [[Data]], [[RegExp]], [[Error]]), 那么**new**表达式中的函数调用将返回该对象引用
   - 参考[「你不知道的javascript」](http://blog.ifyouseewendy.com/blog/2017/07/03/review-you-dont-know-js-this-and-object-prototypes/#what-happened-when-we-callnew-)
   - 摘自掘金[「中高级前端面试」JavaScript手写代码无敌秘籍](https://juejin.im/post/5c9c3989e51d454e3a3902b6#heading-0)


## MDN版：
 - 创建一个空的简单JavaScript对象（即{}）
 - 链接该对象（即设置该对象的构造函数）到另一个对象
 - 将步骤1新创建的对象作为this的上下文
 - 如果该函数没有返回对象，则返回this

<br />

 ```Javascript
  function _new(func) {
    var obj = {};
    if(func.prototype !== null) obj.__proto__ = func.prototype;

    var params = Array.prototype.slice.call(arguments, 1); // arguments :[func, ...rest]
    var ret = func.apply(obj, params);
    if((typeof ret === 'object' || typeof ret === 'function') && ret !== null) return ret;

    return obj;
  }

  function A(){}

  var instanceA1 = _new(A, 1, 2);
  var instanceA2 = new A(1, 2);
  console.log(instanceA1 instanceof A) // true
  console.log(instanceA2 instanceof A) // true

 ```

 ## 举个栗子
 ```JavaScript
  function A(){
    this.a = 1 // 执行A(), 这里的 this 指向的是 window

    return {
      b: 2,
      c: 3
    }
  }

  A.prototype.a = 4
  A.prototype.b = 5
  A.prototype.c = 6

  const x = new A()

  console.log(x.a, x.b, x.c) // undefined, 2, 3
 ```