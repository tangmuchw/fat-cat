# 简单对比 webpack、rollup、esbuild 和 vite

## webpack

> 基于 JavaScript 开发 的前端打包构建框架，通过依赖手机，模块解析，生成 chunk，最终输出生成的打包产物，是一个 BundleBased 的框架，优点是**大而全**，缺点是**配置繁琐**

## rollup

> rollup 是专门针对类库进行打包，其优点是小巧而专注，比如 Vue、React 和 three.js 都是用其打包

## esbulid

> 一个基于 Go 编写的高性能构建工具，和其他构建工具相比，速度快到 10-100x，其内置了一些 loader 能解析编译常见的 js(x),ts(x) 等文件，同时支持通过插件的形式处理其他类型的文件

## vite

> vite 是基于 \_ESMBased_devServer 在开发环境实现了快速启动、按序编译、即时模块热更新等能力，同时针对同一份代码，在生产环境通过 rollup 进行打包，生成线上产物
