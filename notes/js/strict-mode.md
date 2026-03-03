# 严格模式

JavaScript 的严格模式（strict mode）是 ES5 引入的一种限制性更强的语言变体。它在代码执行时采用更严格的解析和错误处理规则，旨在消除代码中的一些不安全或容易出错的地方，提升代码质量和性能，并为未来的 JavaScript 版本做好铺垫。

## 如何启用严格模式

- 在脚本文件或 `<script>` 标签的第一行添加 `"use strict";`（字符串字面量），整个文件都会进入严格模式。
- 在函数内部第一行添加 `"use strict";`，只对该函数作用域启用严格模式。
- 模块（ES6 Module）和类（Class）内部默认就是严格模式，无需显式声明。

## 严格模式的主要变化

### 1. 变量必须声明后再赋值

禁止意外创建全局变量。在非严格模式下，给一个未声明的变量赋值会自动创建一个全局变量；严格模式下会抛出 `ReferenceError`。

```javascript
"use strict";
x = 3.14; // 抛出 ReferenceError: x is not defined
```

### 2. 静默失败转为异常

对一些原本静默失败的操作（如对只读属性赋值、删除不可删除的属性等），严格模式下会抛出错误。

```javascript
"use strict";
var obj = {};
Object.defineProperty(obj, "x", { value: 42, writable: false });
obj.x = 9; // 抛出 TypeError: Cannot assign to read only property 'x'

delete Object.prototype; // 抛出 TypeError: Cannot delete property 'prototype' of function Object() { ... }
```

### 3. 禁止删除变量、函数和函数参数

`delete` 操作符不能用于删除变量、函数声明或函数参数（只能删除对象属性）。

```javascript
"use strict";
var x = 3;
delete x; // 语法错误或抛出 SyntaxError

function f() {}
delete f; // 语法错误
```

### 4. 禁止八进制字面量

八进制字面量（如 `0123`）在非严格模式下被允许（但可能引起混淆），严格模式下不支持，会抛出语法错误。ES6 之后可以用 `0o123` 代替。

```javascript
"use strict";
var num = 0123; // SyntaxError: Octal literals are not allowed in strict mode.
```

### 5. 禁止使用 `with` 语句

`with` 语句会改变作用域链，导致代码难以优化和理解，严格模式下完全禁止。

```javascript
"use strict";
with (Math) {
    // SyntaxError: Strict mode code may not include a with statement
    x = cos(2);
}
```

### 6. 函数参数名称必须唯一

在非严格模式下，函数可以有重复的参数名（如 `function f(a, a, b) {}`），后面的参数会覆盖前面的。严格模式下，重复的参数名会导致语法错误。

```javascript
"use strict";
function f(a, a, b) {
    // SyntaxError: Duplicate parameter name not allowed in this context
    return a + b;
}
```

### 7. 禁止在函数内部遍历调用栈

`arguments.callee` 和 `arguments.caller` 被禁用，访问它们会抛出错误。这是出于优化和安全考虑。

```javascript
"use strict";
function f() {
    arguments.callee; // TypeError: 'caller', 'callee', and 'arguments' properties may not be accessed on strict mode functions
}
```

### 8. 让 `eval` 拥有独立的作用域

在严格模式下，`eval` 执行的代码不会在包含它的作用域中创建新的变量或函数。它只在自己的作用域内生效，并且 `eval` 本身会被保留为关键字。

```javascript
"use strict";
eval("var x = 2;");
console.log(x); // ReferenceError: x is not defined
```

### 9. 禁止使用 `arguments` 和函数参数之间的绑定

在非严格模式下，修改 `arguments` 对象中的值会同步到对应的命名参数，反之亦然。严格模式下，`arguments` 对象是参数的静态副本，修改它不会影响命名参数。

```javascript
"use strict";
function f(a) {
    a = 42;
    console.log(arguments[0]); // undefined（如果调用时没传参）或传入的原始值，不会变成 42
}
f(); // 输出 undefined
```

### 10. 全局作用域中的 `this` 不再指向全局对象

在非严格模式下，函数中如果 `this` 是 `undefined` 或 `null`，会自动替换为全局对象。严格模式下，`this` 保持原样，不会自动包装。

```javascript
"use strict";
function f() {
    console.log(this); // undefined
}
f();
```

### 11. 禁止使用未来保留的关键字作为变量名

严格模式下，一些可能在未来版本中使用的关键字（如 `implements`, `interface`, `let`, `package`, `private`, `protected`, `public`, `static`, `yield` 等）不能用作变量名或函数名，以防止未来兼容性问题。

```javascript
"use strict";
var private = 123; // SyntaxError: Unexpected strict mode reserved word
```

### 12. 限制对 `caller` 和 `arguments` 的访问

函数的 `caller` 属性（指向调用当前函数的函数）和 `arguments` 属性被禁用，访问它们会抛出错误。

```javascript
"use strict";
function f() {
    console.log(f.caller); // TypeError: 'caller' access on strict mode function
}
```

## 总结

严格模式通过以上变更，帮助开发者编写更安全、更健壮的代码，避免一些常见的 JavaScript 陷阱，同时也让 JavaScript 引擎能更好地进行优化。在实际开发中，建议始终在代码中使用严格模式（特别是在模块化和类中已经默认启用），以提升代码质量。
