# Literal 字面量

> 字面量: 一般**固定值**称为字面量，或者说是不用 js 的 new 操作符创建实例

## 字面量分类

- 字符串字面量
- 数组字面量
- 对象字面量
- 函数字面量
- 表达式字面量

```JavaScript
// {} 为 对象字面量
const a = {}

// [] 为 数组字面量
const b = []

// 'hello word' 为字符串字面量
const c = 'hello word'

// 2 + 3 为表达式字面量
const s = 2 + 3


// myFunction 为字符串字面量
function myFunction(a, b) { return a * b;}
```

## 优点

> 省略了构造函数传参初始化这一过程

## 缺点

> 初始化的值都是一致的
