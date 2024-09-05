# CJS, AMD, UMD 和 ESM

## CJS

> cjs 是 common js 的缩写，CommonJS 是 Node.js 采用的模块化规范，主要用于服务端的 JavaScript 环境

-   供后端使用
-   cjs 在浏览器环境中是无效的，它必须要经过编译和打包后才能在浏览器环境中执行
-   require 是运行时加载

### 特性：

-   **同步加载**：模块在代码运行时同步加载，适用于服务端，但不适用于浏览器环境，因为浏览器环境中同步加载会阻塞渲染进程。
-   **缓存机制**：同一个模块在多次加载时会被缓存，除非明确清除缓存。
-   **简单易用**：通过 require 和 module.exports 实现模块的导入和导出，简单直观。

### 局限性：

-   **同步加载的限制**：CommonJS 模块是同步加载的，这意味着在模块加载完成之前，代码的执行会被阻塞。**在前端浏览器环境中，网络延迟可能导致较长的加载时间，进而阻塞页面渲染并降低用户体验**
-   **循环依赖问题**：CommonJS 规范中，模块被加载时执行（运行时加载），如果两个模块互相引用（循环依赖），这可能会导致未定义的行为或部分代码无法执行。
-   **缺乏静态分析能力**：由于 CommonJS 使用动态 require() 语句来引入模块，这使得工具很难在编译时进行静态分析。
-   **跨平台兼容性**：CommonJS 规范设计之初是为了满足服务端 JavaScript（Node.js）环境的需求，它不适合直接在浏览器环境中使用。

```JavaScript
// importing
const doSomething = require('./doSomething.js')

// exporting
module.exports = function doSomething(n) {
    // do something
}
```

## AMD 异步模块定义

> AMD 是 asynchronous module definition 的缩写，是一个在浏览器环境中使用的模块化规范。它解决了 CommonJS 在浏览器中同步加载的问题，使用异步加载方式来加载模块。

-   供前端使用

### 特性：

-   **异步加载**：通过异步方式加载模块，适合在浏览器环境下使用，避免了浏览器渲染的阻塞问题。
-   **依赖前置**：在定义模块时需要声明所有的依赖模块，这些模块会在代码运行前加载完成。
-   **较复杂的定义方式**：需要使用 define() 函数来定义模块，并声明依赖。

### 局限性：

-   **模块定义复杂性增加**：AMD 使用 define() 函数来定义模块，并且需要提前声明所有的依赖模块。
-   **加载速度较慢**：尽管 AMD 通过异步方式加载模块来避免阻塞浏览器渲染进程，但由于模块依赖的前置加载特性，所有依赖模块需要在主模块执行之前全部加载完毕。
-   **过度依赖回调函数**：AMD 模块化规范依赖于回调函数，这会导致代码结构的嵌套层级增加，出现俗称的“回调地狱”现象，使得代码的调试和维护变得更加困难。
-   **生态系统和工具支持限制**：相比于 ES6 Module 等更现代的模块化标准，AMD 的生态系统支持较为有限。

```JavaScript

define(['dep1', 'dep2'], function (dep1, dep2) {
    // define the module value by returning a value.
  return function () {};
})

// or simplified CommonJS wrapping
define(function (require) {
    var dep1 = require('dep1'),
      dep2 = require('dep2');
  return function () {};
})

// math.js
define([], function() {
  const add = (a, b) => a + b;
  const subtract = (a, b) => a - b;

  return {
    add,
    subtract
  };
});

// main.js
require(['./math'], function(math) {
  console.log(math.add(1, 2)); // 输出: 3
  console.log(math.subtract(5, 3)); // 输出: 2
});

```

## UMD

> UMD 是 Universal Module Definition 的缩写

-   UMD 更像是一种模式，去适配多种模块系统
-   当用像 rollup/webpack 这样的打包器的时候，UMD 通常用作一个回调模块

```JavaScript
(function (root, factory) {
    if (typeof define === 'function' && define.amd) {
    define(['jquery', 'underscore'], factory);
  } else if (typeof exports === 'objects') {
    module.exports = factory(require('jquery'), require('underscore'));
  } else {
    root.Requester = factory(root.$, root._);
  }
})(this, function ($, _) {
  // this is where I defined my module implementation
    var Requester = {// ... };
      return Requester;
 })

```

## ESM

> ESM 是 ES6 Module 的缩写。是 JavaScript 语言级别的模块系统，支持静态分析，能够在编译时确定模块的依赖关系。

### 特性：

-   **静态依赖分析**：ES6 Module 在编译时就可以确定模块的依赖关系，从而实现静态分析和树摇（Tree Shaking）优化。
-   **严格模式（Strict Mode）**：ES6 Module 自动采用 JavaScript 严格模式。这意味着模块中不能使用某些不安全的语法（如 with 语句），提高了代码的安全性和性能。
-   **独立的模块作用域**： 每个模块都有独立的作用域，模块内部的变量、函数不会污染全局作用域，避免了变量命名冲突问题。
-   **导入和导出语句（Import 和 Export）**：ES6 Module 使用 import 和 export 关键字来导入和导出模块成员。导出可以是命名导出（Named Export）或默认导出（Default Export）。
-   **异步加载支持**：ES6 Module 可以异步加载模块，避免了阻塞浏览器的渲染进程，从而提升了页面加载性能。
-   **浏览器原生支持**：现代浏览器原生支持 ES6 Module，无需额外的加载器（如 RequireJS）或打包工具（如 Webpack）即可直接使用。

### 局限性：

-   **浏览器兼容性**：早期版本的浏览器不支持 ES6 Module，不过随着浏览器的更新，这个问题正逐渐消失。
-   **服务端使用限制**：在服务端（如 Node.js）环境中，使用 ES6 Module 可能需要一些配置和额外的工具支持（如 Babel、Webpack）。
-   **性能影响**：在非常大量模块导入的场景下，可能会有性能瓶颈。

```JavaScript
import React from 'react';

export default function() {
    // your function
}

export const function1() {}
export const function2() {}
```
