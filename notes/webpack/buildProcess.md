# Webpack 5.x 大致构建过程

> 参考[跟着源码了解 Webpack 编译流程-前端巅峰](https://mp.weixin.qq.com/s/Oes6yI2XCKXKLQSijNNjGQ?st=25D6B8745162BBA43B557AA00DB08E1B72D2699A6D5228E6E1360E83D39E37466280B76D343C9BDF30CEE5B43AE327429C464C33763883385BC1E21AA55957CAFAB34ED65BF7D59CC1552833D08D230EA8158B810BE96DFBD7BD96508491AF044168484699391D687385AD2A8DB10029AF6E266A4FFA9B24AAD9742C865456B9837F9680B9A994D1D7CCA9D61F3161782BEEF57F1A26335FBCB6DECD8F88117F4E00642FEFC2958E574261EB44C8BEAB6D914850A627DFAB2A3B71631A9AB3AB&vid=1688853527239128&cst=DEA82C7FE4BBD00DDE1A1F0CB6F5D3EEF7E7B0FC39C600A898DCE0A2CCC4971BC554F9191CB500E8240D4B9277397708&deviceid=935d7942-b09f-4038-b6eb-c5f25ce0db0a&version=3.1.18.90318&platform=mac)

## 初始化

- 初始化 options 参数
- 实例化 complier 对象
- 初始化默认的和配置的插件
- 开始调用 complier 的 run 方法开始编译

## 编译

- 调用 complier.run，正式进入到编译阶段
- 执行关键的 make 钩子，即开始执行真正的编译，这里会调用 loader 对代码解析，递归模块的依赖解析等
- make 结束后，进入 compilation 的 seal 阶段，这个阶段会创建 chunk，并且有许多用于处理优化的 hook

## run

- 先经过 beforeRun、run 的钩子，进入 compile 方法
- 在 compile 中经过 beforeCompile、compile 钩子后，**实例化 compilation**，来到真正执行编译的钩子 make
- **make 阶段**，执行一些内置的 plugin， 如 TestChildCompilationFailurePlugin、EntryPlugin 等，可检索 hooks.make.tapAsync 来查看

  - EntryPlugin： 在插件的 apply 方法中，将入口信息、上下文环境等作为参数，调用 addEntry 方法，从入口开始编译；在 addEntry 中，调用了 addModuleChain 将整个 Module 链中的所有模块都处理完成
  - NormalModule.doBuild 主要使用 runLoaders，执行配置的 Loader 来解析 Module
  - 经过 Loader 的解析后，得到可被 js 继续解析的 source，此时将其交给 Parser，解析为 AST，并遍历 AST，查找 Import、require 等语句，即当前模块的依赖项，往复递归，直到解析完所有依赖

- make 阶段结束后，将会在其回调中调用 **compilation.seal** 进入 seal 阶段，根据编译好的 Module 创建 Chunk，其主要逻辑是：
  - 根据 entry 生成 Chunk 图
  - 生成构建 hash
  - 生成 Chunk 对应的资源，保存在 compilation.assets 中

## 输出

- 输出部分，主要是在上一步 seal 阶段的回调中，进到 **complier.emitAssets** 方法，将 seal 过程中处理好的资源生成具体的文件
