# 概念

## 入口(entry)

> 指示 webpack 应该使用哪个模块，来作为构建其内部依赖图的开始。

## 出口(output)

> 告诉 webpack 在哪里输出它所创建的 bundles， 默认**./dist**

## loader

> 让 webpack 能够去处理那些非 JavaScript 文件(webpack 自身只理解 JavaScript)

```JavaScript
// webpack.config.js

const path = require('path')

const config = {
    output: {
        filename: 'my-first-webpack.bundle.js'
    },
    module: {
        rules: [
            {
                test: /\.txt$/,
                use: 'raw-loader'
            }
        ]
    }
}

module.exports = config
```

## 插件(plugins)

> 用于执行功能更广的任务

- 插件的范围包括，从打包优化和压缩，一直到重新定义环境中的变量

```JavaScript
// webpack.config.js
const HtmlWebpackPlugin = require('html-webpack-plugin')
const webpack = require('webpack') // 用于访问内置插件

const config = {
    module: {
        rules: [
            {
                test: /\.txt$/,
                use: 'raw-loader'
            }
        ]
    }，
    plugins: [
        new HtmlWebpackPlugin({
            template: './src/index.html'
        })
    ]
}

module.exports = config
```

## 模式(mode)

> 通过选择<code>development</code>或<code>production</code>之中的一个，来设置<code>mode</code>参数

## 依赖图(dependency graph)

> 任何时候，一个文件依赖与另一个文件，webpack 就把此视为文件之间有**依赖关系**。

- 这使得 webpack 可以接受非代码资源(non-code asset)（例如图像后 web 字体，并且可以把它们作为**依赖**提供给你的应用程序）

## Runtime

> runtime， 以及伴随的 manifest 数据，主要是指：在浏览器运行时，webpack 用来连接模块化的应用程序的所有代码。

- runtime 包含：在模块交互时，链接模块所需的加载和解析逻辑。包括浏览器中的已加载模块的连接，以及懒加载模块的执行逻辑。

## Manifest

> 管理所有模块之间的交互。

- 当编译器(complier)开始**执行、解析和映射**应用程序时，他会保留所有模块的详细要点。这个数据集合称为**Manifest**
- 当完成打包并发送到浏览器时，会在运行时通过 Manifest 来解析和加载模块，无论你选择哪种模块语法，那些<code>import</code>或<code>require</code>语句现在都已经转换成<code>**webpack_require**</code>方法

## 整体构建流程

> 详见[构建过程](./buildProcess.md)

- **初始化**：启动构建；读取与合并配置参数；加载 Plugin；实例化 Complier
- **编译**：从 Entry 出发，针对每个 Module 调用对应的 Loader 翻译文件，再找到该 Module 依赖的 Module，递归进行编译处理，对编译后的 Module 组合成 Chunk 及对应资源 Assets
- **输出**：把编译过程得到的 Assets 输出到文件系统中

## Webpack 5 的核心特性（当前最新稳定版）

Webpack 5 相比 4 有大量优化，核心亮点：

- 持久化缓存：内置缓存机制，大幅提升二次构建速度；
- 模块联邦（Module Federation）：支持跨应用共享模块（微前端核心能力）；
- 更好的 Tree Shaking：优化了无用代码剔除，减小打包体积；
- Node.js 模块 Polyfill 移除：默认不再自动注入 Node.js 核心模块（如 path/fs），需手动配置，减小打包体积；
- 性能优化：编译速度、内存占用均有显著提升。
