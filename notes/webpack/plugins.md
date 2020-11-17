# 插件

## 剖析

> > webpack 插件是一个具有**apply**属性的 JavaScript 对象。apply 属性会被**webpack compiler**调用，并且 compiler 对象可在整个编辑生命周期访问

```JavaScript
//ConsoleLogOnBuildWebpackPlugin.js

const pluginName = 'ConsoleLogOnBuildWebpackPlugin'

class ConsoleLogOnBuildWebpackPlugin {

    apply(complier){
        complier.hooks.run.tap(pluginName, compilation => {
            console.log('webpack 构建过程开始')
        })
    }
}
```

## 用法

- 由于插件可以携带参数/选项，必须在 webpack 配置中，向<code>plugins</code>属性传入<code>new</code>实例
