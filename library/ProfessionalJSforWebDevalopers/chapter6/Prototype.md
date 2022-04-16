# 原型

```JavaScript
    function Foo() {}

    let f1 = new Foo()
    let f2 = new Foo()

    console.log(f1.__proto__ === Foo.prototype) // true
    console.log(f1.prototype) // undefined
    console.log(Foo.prototype.constructor === Foo) // true
    console.log(Foo.prototype.__proto__ === Object.prototype) // true
    console.log(Object.prototype.__proto__ === null) // true

    // Foo created by Function
    console.log(Foo.__proto__ === Function.prototype) // true
    console.log(Function.prototype.constructor === Function) // true

    console.log(Function.prototype.__proto__ === Object.prototype) // true
    console.log(Object.prototype.constructor === Object) // true
    console.log(Object.__proto__ === Function.prototype) // true


```
