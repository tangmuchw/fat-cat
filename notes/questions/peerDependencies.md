
# peerDependencies
>> 同等依赖。用于指定当前包（也就是你写的包）兼容的宿主版本

- 目的是提示宿主环境去安装满足插件peerDependencies所指定依赖的包，然后在插件import或者require所依赖的包的时候，永远都是引用宿主环境统一安装的npm包，最终解决插件与所依赖包不一致的问题
- 简单来说有一个version check的功能