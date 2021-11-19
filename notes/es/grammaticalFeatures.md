# JS 语法 ES6、ES7、ES8、ES9、ES10、ES11、ES12 新特性

## ES6（2015）

- 类（class）
- 模块化（ES Module）
- 箭头函数
- 函数参数默认值
- 模版字符串
- 解构赋值
- 扩展操作符
- 对象属性简写

```JavaScript
    const name='tm',
    const obj = { name };
```

- Promise
- let 和 const

## ES7（2016）

- Array.prototype.includes()
- 指数操作符

```JavaScript
   3 ** 2 // 9
```

## ES8（2017）

- async/await 异步终极解决方案
- Object.values()
- Object.entries()
- String padding

```JavaScript
  'cat'.padStart(2)
  'cat'.padEnd(2)
```

- 函数参数列表结尾允许逗号
- Object.getOwnPropertyDescriptors()
  > 获取一个对象的所有自身属性的描述符,如果没有任何自身属性，则返回空对象
- SharedArrayBuffer 对象
  > SharedArrayBuffer 对象用来表示一个通用的，固定长度的原始二进制数据缓冲区
- Atomics 对象
  > Atomics 对象提供了一组静态方法用来对 SharedArrayBuffer 对象进行原子操作

## ES9（2018）

- 异步迭代
  > await 可以和 for...of 循环一起使用，以串行的方式运行异步操作

```JavaScript
  async function process(list){
      for await (lei i of list) {
          // do something
      }
  }
```

- Promise.finally()
- Rest/Spread 属性

```JavaScript
    const values = [1, 2, 3, 5, 6];
    console.log( Math.max(...values) ); // 6
```

- 正则表达式命名捕获组

```JavaScript
   const reg = /(?<year>[0-9]{4})-(?<month>[0-9]{2})-(?<day>[0-9]{2})/;
const match = reg.exec('2021-02-23'); // groups:{ day: '23', month: '02', year: '2021' }
```

- 正则表达时反向断言

  - ?=pattern 先行断言
  - ?!pattern 正向否定查找
  - ?<=pattern 后行断言
  - ?<!pattern 反向否定查找

```JavaScript
   (?=p)、(?<=p)  p 前面(位置)、p 后面(位置)
(?!p)、(?<!p>) 除了 p 前面(位置)、除了 p 后面(位置)
```

- 正则表达式 dotAll 模式
  > 正则表达式中点.匹配除回车外的任何单字符，标记 s 改变这种行为，允许行终止符的出现

```JavaScript
    /foo.bar/s.test('foo\nbar'); // true
    /foo.bar/.test('foo\nbar'); // false
```

## ES10（2019）

- Array.flat() 和 Array.flatMap()

```JavaScript
    var arr = [1, 2, 3, 4];

    arr.flatMap(x => [x, x * 2]);
    // is equivalent to
    arr.reduce((acc, x) => acc.concat([x, x * 2]), []);
    // [1, 2, 2, 4, 3, 6, 4, 8]

```

- String.trimStart() 和 String.trimEnd()
- String.prototype.machAll
- Symbol.prototype.description
  > 只读属性，回 Symbol 对象的可选描述的字符串。
- Object.fromEntries()
  > 返回一个给定对象自身可枚举属性的键值对数组

```JavaScript
    // 通过 Object.fromEntries， 可以将 Map 转化为 Object:
    const map = new Map([ ['foo', 'bar'], ['baz', 42] ]);
    console.log(Object.fromEntries(map)); // { foo: "bar", baz: 42 }
```

## ES11 (2020)

- ?? 空值处理
- ?. 可选链
- Promise.allSettled
- import() 按需导入
- 新基本数据类型 BigInt
- globalThis
  - 浏览器: window
  - worker: self
  - node: global

## ES12（2021）

- replaceAll
- Promise.any

  > Promise.any() 接收一个 Promise 可迭代对象，只要其中的一个 promise 成功，就返回那个已经成功的 promise 。如果可迭代对象中没有一个 promise 成功（即所有的 promises 都失败/拒绝），就返回一个失败的 promise。**返回所有失败的, 有一个成功就返回这成功的**

- WeakRefs
  > 使用 WeakRefs 的 Class 类创建对对象的弱引用(对对象的弱引用是指当该对象应该被 GC 回收时不会阻止 GC 的回收行为)
- 逻辑运算符和赋值表达式

  > 逻辑运算符和赋值表达式，新特性结合了逻辑运算符（&&，||，??）和赋值表达式而 JavaScript 已存在的 复合赋值

- 数字分隔符
  > 数字分隔符，可以在数字之间创建可视化分隔符，通过\_下划线来分割数字，使数字更具可读性

```JavaScript
    const money = 1_000_000_000;
    //等价于
    const money = 1000000000;
```
