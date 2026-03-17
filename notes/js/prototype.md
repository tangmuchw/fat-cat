# JS 原型链

### 一、先理解核心概念（由浅入深）

#### 1. 原型（prototype）的本质

JavaScript 是一门基于**原型（Prototype）** 的语言，而非传统的类（Class）语言（ES6 的 `class` 只是语法糖）。

- 每个**函数（Function）** 都有一个 `prototype` 属性（原型对象），这个对象默认包含两个核心属性：
    - `constructor`：指向该函数本身（比如 `Person.prototype.constructor === Person`）。
    - `__proto__`：指向该原型对象的原型（即上一级原型）。
- 每个**实例对象**都有一个隐式的 `__proto__` 属性（ES6 中可通过 `Object.getPrototypeOf()` 访问），它会指向创建该实例的构造函数的 `prototype`。

#### 2. 原型链的定义

当你访问一个对象的属性/方法时，JS 会先在对象自身查找：

- 如果找到，直接返回；
- 如果没找到，就通过 `__proto__` 向上查找其原型对象的属性/方法；
- 这个“向上查找”的链条会一直延续，直到找到 `Object.prototype`（原型链的顶端）；
- 如果到 `Object.prototype` 还没找到，就返回 `undefined`。

这条由 `__proto__` 串联起来的查找链条，就是**原型链**。

### 二、代码示例：直观理解原型链

```javascript
// 1. 定义构造函数
function Person(name) {
    this.name = name; // 实例自身属性
}

// 2. 给构造函数的原型添加方法（所有实例共享）
Person.prototype.sayHello = function () {
    console.log(`Hello, I'm ${this.name}`);
};

// 3. 创建实例
const tom = new Person("Tom");

// 4. 验证原型关系
console.log(tom.__proto__ === Person.prototype); // true：实例的__proto__指向构造函数的prototype
console.log(Person.prototype.__proto__ === Object.prototype); // true：Person原型的原型指向Object原型
console.log(Object.prototype.__proto__); // null：原型链的顶端

// 5. 原型链查找演示
tom.sayHello(); // 自身没有sayHello，向上找Person.prototype，执行 → Hello, I'm Tom
console.log(tom.toString()); // 自身/Person.prototype都没有，向上找Object.prototype的toString方法 → [object Object]
console.log(tom.age); // 整条原型链都没有，返回undefined
```

#### 关键补充：ES6 Class 语法糖的原型链

```javascript
class Person {
    constructor(name) {
        this.name = name;
    }
    sayHello() {
        // 等价于 Person.prototype.sayHello
        console.log(`Hello, I'm ${this.name}`);
    }
}
const tom = new Person("Tom");
console.log(tom.__proto__ === Person.prototype); // 依然为true，class本质还是原型
```

### 三、原型链的核心作用

1. **属性/方法共享**：原型上的方法/属性会被所有实例共享，节省内存（比如上面的 `sayHello` 方法，所有 Person 实例都能用，且只存一份）。
2. **实现继承**：通过修改原型链的指向，让一个构造函数的原型指向另一个构造函数的实例，从而实现继承（比如经典的原型链继承）。

### 总结

1. **核心关系**：实例的 `__proto__` → 构造函数的 `prototype` → `Object.prototype` → `null`，这就是完整的原型链。
2. **查找规则**：访问对象属性/方法时，先查自身，再沿 `__proto__` 向上查，直到 `Object.prototype`，找不到则返回 `undefined`。
3. **本质价值**：原型链是 JS 实现属性共享和继承的核心机制，ES6 的 `class` 只是原型链的语法糖，底层逻辑不变。
