# 简单对比 Webpack、Rollup、ESbuild、Parcel、Snowpack 和 Vite

## Webpack

> 基于 JavaScript 开发 的前端打包构建框架，通过依赖手机，模块解析，生成 chunk，最终输出生成的打包产物，是一个 BundleBased 的框架，优点是**大而全**，缺点是**配置繁琐**。两大最核心的特点：**一切皆模块**和**按需加载**

## Rollup

> Rollup 是专门针对类库进行打包，是一款 ES Modules 打包器，其优点是小巧而专注，比如 Vue、React 和 three.js 都是用其打包。[rollup.js 中文文档](https://www.rollupjs.com/)

### 优点：

-   代码效率更简洁、效率更高
-   默认支持 tree-shaking

### 缺点：

-   加载其他类型的资源文件或者支持导入 CommonJS 模块，或是编辑 ES 新特性，这些额外的需求需要单独使用插件去完成

## ESbulid

> 一个基于 Go 编写的高性能构建工具，和其他构建工具相比，速度快到 10-100x，其内置了一些 loader 能解析编译常见的 js(x),ts(x) 等文件，同时支持通过插件的形式处理其他类型的文件

## vite

> vite 是一种新型前端构建工具，能够显著提升前端开发体验。是基于 \_ESMBased_devServer 在开发环境实现了快速启动、按序编译、即时模块热更新等能力，同时针对同一份代码，在生产环境通过 rollup 进行打包，生成线上产物

主要由两部分组成：

-   一个开发服务器，它基于 原生 ES 模块 提供了丰富的内建功能，如速度快到惊人的模块热更新 HMR
-   一套构建指令，它使用 Rollup 打包你的代码，并且它是预配置的，可以输出用于生产环境的优化过的静态资源

Vite 会**直接启动开发服务器，不需要进行打包操作，也就意味着不需要分析模块的依赖、不需要编译**，因此启动速度非常快

利用现代浏览器支持 ES Module 的特性，当浏览器请求某个模块的时候，再根据需要对模块的内容进行编译，这种方式大大缩短了编译时间

在热模块 HMR 方面，当修改一个模块的时候，仅需让浏览器重新请求该模块即可，无须像 webpack 那样需要把该模块的相关依赖模块全部编译一次，效率更高

## Parcel

> Parcel 是一款完全零配置的前端打包器，它提供了 “傻瓜式” 的使用体验，只需了解简单的命令，就能构建前端应用程序。
> Parcel 跟 Webpack 一样都支持以任意类型文件作为打包入口，但建议使用 HTML 文件作为入口，该 HTML 文件像平时一样正常编写代码、引用资源

-   支持模块热替换
-   支持自动安装依赖
-   零配置加载其他类型的资源文件
-   打包过程是多进程同时工作，构建速度回避 Webpack 块，输出文件也会被压缩，并且样式代码也会被单独提取到单个文件中

## Snowpack

> [Snowpack](https://www.snowpack.cn/concepts/how-snowpack-works) 是一个用在现代 Web 应用上的，快如闪电的前端构建工具。 在你的开发工作流程中，它可以替代更重、更复杂的打包工具，如 webpack 或 Parcel。 Snowpack 利用了 JavaScript 的本地模块系统(ESM)以避免不必要的工作，无论你的项目膨胀地多大，它都能保持快速。

### 免打包式开发

免打包式开发是指在开发过程中向浏览器发送单个文件的设计。文件仍然可以用你最喜欢的工具（如 Babel、TypeScript、Sass）来构建，然后在浏览器中单独加载，由于 ESMimport 和 export 语法的存在，这些文件具有依赖性。不管什么时候 Snowpack 都只重建发生变化的文件

**每个文件都是单独构建的，并且被无限期地缓存。**开发环境不会对一个文件进行多次构建，浏览器也不会对一个文件进行两次下载（直到它改变）。这就是免打包式开发的真正力量。

### NPM 依赖处理

Snowpack 采取了一种不同的方法： Snowpack 没有因为这个打包整个应用程序，而是单独处理 npm 依赖

-   Snowpack 扫描网站/应用程序引入的所有 npm 包。
-   Snowpack 从 node_modules 目录中读取这些已安装的依赖包。
-   Snowpack 将所有 npm 依赖分别打包到单个 JavaScript 文件中。例如：react 和 react-dom 分别转换为 react.js 和 react-dom.js
-   每个转换来的文件在经过 ESM 的 import 语句导入后，都可以直接在浏览器中运行。
-   因为 npm 依赖很少改变，Snowpack 很少需要重建它们。

```HTML
node_modules/react/**/*     -> http://localhost:3000/web_modules/react.js
node_modules/react-dom/**/* -> http://localhost:3000/web_modules/react-dom.js
```
