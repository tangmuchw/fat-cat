[toc]

# CreateObject 创建对像

## 工厂模式

## 构造函数模式

## 原型模式

## 组合使用构造函数模式和原型模式

## 动态原型模式

## 寄生构造函数模式

## 稳妥构造函数模式

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
console.log(p1.name)
console.log(p1.skin)

function Parent(){
    this.skin = ['white', 'yellow', 'black']
}
function Child(){}
Child.prototype = new Person2()

const m1 = new Child()
const m2 = new Child()
m1.name = 'man1'
m1.skin.push('red')

console.log(m1.name)
console.log(m1.skin)
console.log(m2.name)
console.log(m2.skin)

```
