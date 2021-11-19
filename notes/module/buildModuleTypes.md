# CJS, AMD, UMD 和 ESM

## CJS

> cjs 是 common js 的缩写

- 供后端使用
- cjs 在浏览器环境中是无效的，它必须要经过编译和打包后才能在浏览器环境中执行
- require 是运行时加载

```JavaScript
// importing
const doSomething = require('./doSomething.js')

// exporting
module.exports = function doSomething(n) {
    // do something
}
```

## AMD

> AMD 是 asynchronous module definition 的缩写

- 供前端使用

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

```

## UMD

> UMD 是 Universal Module Definition 的缩写

- UMD 更像是一种模式，去适配多种模块系统
- 当用像 rollup/webpack 这样的打包器的时候，UMD 通常用作一个回调模块

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

> ESM 是 ES 模块的缩写。是 JS 语言为了标准化模块系统的一种方案

- 具有 tree-shakable 的特性，这是由于 ES6 的静态模块结构

```JavaScript
import React from 'react';

export default function() {
    // your function
}

export const function1() {}
export const function2() {}
```
