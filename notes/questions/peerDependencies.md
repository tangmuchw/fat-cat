# peerDependencies

> 同等依赖。用于指定当前包（也就是你写的包）兼容的宿主版本

- 目的是提示宿主环境去安装满足插件 peerDependencies 所指定依赖的包，然后在插件 import 或者 require 所依赖的包的时候，永远都是引用宿主环境统一安装的 npm 包，最终解决插件与所依赖包不一致的问题
- 简单来说有一个 version check 的功能
