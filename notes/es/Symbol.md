# Symbol

> ES6 引入了一种新的原始数据类型 Symbol，表示独一无二的值，防止属性名的冲突

## 注意事项

- Symbol 函数前不能使用 new 命令，否则会报错。这是因为生成的 Symbol 是一个原始类型的值，不是对象
- Symbol，基本上，它是一种类似于字符串的数据类型
- 如果 Symbol 的参数是一个对象，就会调用该对象的 toString 方法，将其转为字符串，然后才生成一个 Symbol 值
- ES2019 提供了一个实例属性 description，直接返回 Symbol 的描述,

```JavaScript
    const sym = Symbol('foo');

    sym.description // "foo"
```

## 属性名的遍历

- Symbol 作为属性名，遍历对象的时候，该属性不会出现在 **for...in**、**for...of** 循环中，也不会被 **Object.keys()**、**Object.getOwnPropertyNames()**、**JSON.stringify()**返回
- **Object.getOwnPropertySymbols()**方法，可以获取指定对象的所有 Symbol 属性名。该方法返回一个数组，成员是当前对象的所有用作属性名的 Symbol 值

```JavaScript
const obj = {};
const a = Symbol('a');
const b = Symbol('b');

obj[a] = 'Hello';
obj[b] = 'World';

const objectSymbols = Object.getOwnPropertySymbols(obj); // [Symbol(a), Symbol(b)]

```

- **Reflect.ownKeys()**方法可以返回所有类型的键名，包括常规键名和 Symbol 键名

```JavaScript
const obj = {
  [Symbol('my_key')]: 1,
  enum: 2,
  nonEnum: 3
};

Reflect.ownKeys(obj) //  ["enum", "nonEnum", Symbol(my_key)]
```

## Symbol.for() vs Symbol()

> 这两种写法，都会生成新的 Symbol。它们的区别是，前者会被登记在全局环境中供搜索，后者不会

```JavaScript
    Symbol.for("bar") === Symbol.for("bar") // true

    Symbol("bar") === Symbol("bar") // false
```

## Symbol.keyFor()

> Symbol.keyFor() 方法返回一个已登记的 Symbol 类型值的 key

```JavaScript
    let s1 = Symbol.for("foo");
    Symbol.keyFor(s1) // "foo"

    let s2 = Symbol("foo");
    Symbol.keyFor(s2) // undefined
```
