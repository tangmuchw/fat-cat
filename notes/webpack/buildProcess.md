# Webpack 5.x 大致构建过程

> 参考[跟着源码了解 Webpack 编译流程-前端巅峰](https://mp.weixin.qq.com/s/Oes6yI2XCKXKLQSijNNjGQ?st=25D6B8745162BBA43B557AA00DB08E1B72D2699A6D5228E6E1360E83D39E37466280B76D343C9BDF30CEE5B43AE327429C464C33763883385BC1E21AA55957CAFAB34ED65BF7D59CC1552833D08D230EA8158B810BE96DFBD7BD96508491AF044168484699391D687385AD2A8DB10029AF6E266A4FFA9B24AAD9742C865456B9837F9680B9A994D1D7CCA9D61F3161782BEEF57F1A26335FBCB6DECD8F88117F4E00642FEFC2958E574261EB44C8BEAB6D914850A627DFAB2A3B71631A9AB3AB&vid=1688853527239128&cst=DEA82C7FE4BBD00DDE1A1F0CB6F5D3EEF7E7B0FC39C600A898DCE0A2CCC4971BC554F9191CB500E8240D4B9277397708&deviceid=935d7942-b09f-4038-b6eb-c5f25ce0db0a&version=3.1.18.90318&platform=mac)

## 初始化

-   初始化 options 参数
-   实例化 compiler 对象
-   初始化默认的和配置的插件
-   开始调用 compiler 的 run 方法开始编译

## 编译

-   调用 compiler.run，正式进入到编译阶段
-   执行关键的 make 钩子(compiler.hooks.make)，即开始执行真正的编译，这里会调用 loader 对代码解析，递归模块的依赖解析等
-   make 结束后，进入 compilation 的 seal （封存）阶段，这个阶段会创建 chunk，并且有许多用于处理优化的 hook

## run

-   先经过 beforeRun、run 的钩子，进入 compile 方法
-   在 compile 中经过 beforeCompile、compile 钩子后，**实例化 compilation**，来到真正执行编译的钩子 make
-   **make 阶段**，执行一些内置的 plugin， 如 TestChildCompilationFailurePlugin、EntryPlugin 等，可检索 hooks.make.tapAsync 来查看

    -   EntryPlugin： 在插件的 apply 方法中，将入口信息、上下文环境等作为参数，调用 addEntry 方法，从入口开始编译；在 addEntry 中，调用了 addModuleChain 将整个 Module 链中的所有模块都处理完成
    -   NormalModule.doBuild 主要使用 runLoaders，执行配置的 Loader 来解析 Module
    -   经过 Loader 的解析后，得到可被 js 继续解析的 source，此时将其交给 Parser，解析为 AST，并遍历 AST，查找 Import、require 等语句，即当前模块的依赖项，往复递归，直到解析完所有依赖

-   make 阶段结束后，将会在其回调中调用 **compilation.seal** 进入 seal 阶段，根据编译好的 Module 创建 Chunk，其主要逻辑是：
    -   根据 entry 生成 Chunk 图
    -   生成构建 hash
    -   生成 Chunk 对应的资源，保存在 compilation.assets 中

## 输出

-   输出部分，主要是在上一步 seal 阶段的回调中，进到 **compiler.emitAssets** 方法，将 seal 过程中处理好的资源生成具体的文件

## Compilation

> Compilation 对象**代表了一次资源版本构建**。每次构建过程都会产生一次 Compilation，比如我们启动 watch 功能的时候，每当检测到一个文件变化，就会重新创建一个新的 Compilation，从而生成一组新的编译资源 一个 Compilation 对象表现了当前的模块资源、编译生成资源、变化的文件、以及被跟踪依赖的状态信息

-   Compilation 对象也提供了插件需要自定义功能的回调，以供插件做自定义处理时选择使用拓展。简单来说，**Compilation 的职责就是构建模块和 Chunk，并利用插件优化构建过程**。

## Compiler

> Compiler 用来创建新的编译（或新的构建）。compilation 实例能够访问所有的模块和它们的依赖（大部分是循环依赖）。它会对应用程序的依赖图中所有模块进行字面上的编译(literal compilation)。在编译阶段，模块会被加载(loaded)、封存(sealed)、优化(optimized)、分块(chunked)、哈希(hashed)和重新创建(restored)
