[toc]

# CreateObject 创建对象

## 使用 Object 构造函数或对象字面量创建单个对象

-   缺点
    -   对于相似对象，使用同一个接口创建很多对象，会产生大量的重复代码

## 工厂模式

-   优点

    -   解决了创建多个相似对象的问题

-   缺点
    -   没有解决对象识别的问题, 即怎么知道一个对象的类型

```JavaScript
function createPerson(name, age, job){
    var obj = new Object()
    obj.name = name
    obj.age = age
    obj.job = job
    obj.sayName = function(){
        console.log(this.name)
    }

    return obj
}

const p1 = createPerson('tom', 3, 'Software Engineer')
const p2 = createPerson('jack', 4, 'Doctor')
```

## 构造函数模式

-   优点
    -   可以将构造函数的实例标识为一种特定的类型
-   缺点
    -   每个方法都要在每个实例上重新创建一遍
    -   全局作用域中定义的函数实际上只能被某个对象调用，这让全局作用域优点名不副实
    -   如果对象需要定义很多方法，那么就要定义很多个全局函数，导致**自定义的引用类型没有封装性而言**

```JavaScript
function sayName(){
    console.log(this.name)
}

function Person(name, age, job){
    this.name = name
    this.age = age
    this.job = job
    // this.sayName = function(){
    //     console.log(this.name)
    // }
    this.sayName = sayName
}

const p1 = new Person('tom', 3, 'Software Engineer')
const p2 = new Person('jack', 4, 'Doctor')
```

## 原型模式

> **创建的每个函数**都有一个 prototype (原型) 属性，这个属性是一个指针，指向一个对象，而这个对象的用途是包含可以用特定类型的所有实例共享的属性和方法

-   isPrototypeOf(): 测试一个对象是否存在于另一个对象的原型链上
-   getPrototypeOf(): 返回 [[prototype]] 的值

```JavaScript
function Person(){}

Person.prototype = {
    constructor: Person,
    name: 'tom',
    age: 3,
    job: 'Software Engineer',
    friends: ['jack', 'hri'],
    sayName: function(){
        console.log(this.name)
    }
}

const p1 = new Person()
const p2 = new Person()

p1.friends.push('van')
console.log(p1.friends) // 'jack', 'hri', 'van'
console.log(p2.friends) // 'jack', 'hri', 'van'

```

```JavaScript
Person.prototype.constructor == Person // true

Person.prototype.isPrototypeOf(p1) // true

Object.getPrototypeOf(p1) == Person.prototype // true

```

## 组合使用构造函数模式和原型模式

```JavaScript
function Person(){
  this.friends = ['tom', 'jack']
}

Person.prototype = {
    constructor: Person,
    sayName: function(){
        console.log(this.name)
    }
}

const p1 = new Person()
const p2 = new Person()

p1.friends.push('van')
console.log(p1.friends) // ['tom', 'jack', 'van']
console.log(p1.friends) // ['tom', 'jack']
```

## 动态原型模式

```JavaScript
function Person(){
  this.friends = ['tom', 'jack']

  if(typeof this.sayName !== 'function') {
    Person.prototype.sayName = function(){
      console.log(this.name)
    }
  }
}
```

## 寄生构造函数模式

> 基本思想：创建一个函数，该函数的作用仅仅是封装创建对象的代码, 然后再返回新创建的对象

```JavaScript
function Person(name){
  var obj = new Object()
  obj.name = name
  obj.sayName = function(){
    console.log(this.name)
  }

  return obj
}
```

## 稳妥构造函数模式

> 所谓稳妥对象，指的是没有公共属性，而且其方法也不引用 this 的对象

```JavaScript
function Person(){
  var obj = new Object()

  // 可以再这里定义私有变量和函数

  // 添加方法
  obj.sayName = function(){
    console.log(this.name)
  }

  return obj
}
```

## QA

```JavaScript

function Person(){
    this.name = 'hello'
    this.skin = ['white', 'yellow', 'black']

    return {
        name: 'world',
    }
}

Person.prototype.name = 'helle world'

const p1 = new Person()
console.log(p1.name) // world
console.log(p1.skin) // undefined

function Parent(){
    this.skin = ['white', 'yellow', 'black']
}
function Child(){}
Child.prototype = new Parent()

const m1 = new Child()
const m2 = new Child()
m1.name = 'man1'
m1.skin.push('red')

console.log(m1.name) // man1
console.log(m1.skin) // [ 'white', 'yellow', 'black', 'red' ]
console.log(m2.name) // undefined
console.log(m2.skin) // [ 'white', 'yellow', 'black', 'red' ]

```
