[toc]

# 防篡改对象

## 不可篡改对象

> **Object.preventExtensions()**，就不能给对象添加新属性和方法

```JavaScript
var person = { name: 'tmchw'}
console.log(Object.isExtensible(person)) // true

Object.preventExtensions(person)
console.log(Object.isExtensible(person)) // false

person.age = 29
console.log(person.age) // undefined
```

## 密封对象\*

> ES5 为对象定义的第二个保护级别是**密封对象（sealed object）**，要密封对象，使用方法**Object.seal()**

- 密封对象不可扩展
- 不能删除属性和方法

```JavaScript
var person = { name: 'tmchw'}
Object.seal(person)
console.log(Object.isSealed(person)) // true

person.age = 29
console.log(person.age) // undefined

delete person.name
console.log(person.name) // 'tmchw'

```

## 冻结的对象

> 最严格的防篡改级别是冻结对象（frozen object），ES5 定义 Object.freeze() 来冻结对象

- 不可扩展
- 密封的
