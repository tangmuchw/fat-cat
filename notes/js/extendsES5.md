# 继承 ES5

```JavaScript
 function Parent(name){
     this.name = name
 }

 Parent.prototype.getName = function(){
     return this.name
 }

 function Child(){
     // 构造函数继承
     Parent.call(this, 'tom')
 }

 // 寄生组合式继承
 //  Child.prototype = new Parent()
 Child.prototype = Object.create(Parent.prototype)
 Child.prototype.constructor = Child
```
