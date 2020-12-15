[toc]

# Inheritance 继承

## 原型链

- 缺点
  - 包含引用类型值的原型
  - 创建子类型的实例时，不能向超类型的构造函数中传递参数

```JavaScript
function SuperType(){
    this.property = true
}

SuperType.prototype.getSuperValue = function(){
    return this.property
}

function SubType(){
    this.subProperty = false
}

SubType.prototype = new SuperType()

SubType.prototype.getSubValue = function(){
    return this.subProperty
}

const ins = new SubType()
console.log(ins.getSuperValue()) // true

```

## 借用构造函数

- 优点: 可以再子类型构造函数中向超类型构造函数传递参数
- 缺点: 方法都在构造函数中定义，因此函数无法复用

```JavaScript
function SuperType(){
    this.colors = ['red', 'blue', 'green']
}

function SubType(){
    // 继承了 SuperType
    SuperType.call(this)
}

const ins1 = new SubType()
ins1.colors.push('black')
console.log(ins1.colors) // ['red', 'blue', 'green', 'black']

const ins2 = new SubType()
console.log(ins2.colors) // ['red', 'blue', 'green']

```

## 组合继承

```JavaScript
function SuperType(name){
    this.name = name
    this.colors = ['red', 'blue', 'green']
}

SuperType.prototype.sayName = function(){
    console.log(this.name)
}

function SubType(name, age){
    // 继承了 SuperType
    SuperType.call(this, name)
    this.age = age
}

SubType.prototype = new SuperType()

SubType.prototype.sayAge = function(){
    console.log(this.age)
}

const ins1 = new SubType('tom', 23)
ins1.colors.push('black')
console.log(ins1.colors) // ['red', 'blue', 'green', 'black']
ins1.sayName() // tom
ins1.sayAge() // 23

const ins2 = new SubType('jack', 24)
console.log(ins2.colors) // ['red', 'blue', 'green']
ins2.sayName() // jack
ins2.sayAge() // 24
```

## 原型式继承

```JavaScript
function object(obj){
    function F(){}
    F.prototype = obj
    return new F()
}
```

## 寄生式继承

- 缺点：不能做到函数复用

```JavaScript
function createAnother(origin){
  const clone = object(origin)
  clone.sayHi = function(){
      console.log('hi')
  }
  return clone
}
```

## 寄生组合式继承

> 基本思想: 通过构造函数来继承属性，通过原型链的混成形式来继承方法

```JavaScript
function SuperType(name){
    this.name = name
    this.colors = ['red', 'blue', 'green']
}

SuperType.prototype.sayName = function(){
    console.log(this.name)
}

function SubType(name, age){
    SuperType.call(this, name)
    this.age = age
}

SubType.prototype = new SuperType()
SubType.prototype.constructor = Subtype
```
