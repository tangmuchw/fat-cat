#概念：

## 入口(entry)
>>指示webpack应该使用哪个模块，来作为构建其内部依赖图的开始。


## 出口(output)
>>告诉webpack在哪里输出它所创建的bundles， 默认**./dist**


## loader
>>让webpack能够去处理那些非JavaScript文件(webpack自身只理解JavaScript)

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
>>用于执行番位更广的任务
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
>> 通过选择<code>development</code>或<code>production</code>之中的一个，来设置<code>mode</code>参数


## 依赖图(dependency graph)
>>任何时候，一个文件依赖与另一个文件，webpack就把此视为文件之间有**依赖关系**。
- 这使得webpack可以接受非代码资源(non-code asset)（例如图像后web字体，并且可以把它们作为__依赖__提供给你的应用程序）


## Runtime
>>runtime， 以及伴随的manifest数据，主要是指：在浏览器运行时，webpack用来连接模块化的应用程序的所有代码。

- runtime包含：在模块交互时，链接模块所需的加载和解析逻辑。包括浏览器中的已加载模块的连接，以及懒加载模块的执行逻辑。


## Manifest
>>管理所有模块之间的交互。
- 当编译器(complier)开始**执行、解析和映射**应用程序时，他会保留所有模块的详细要点。这个数据集合称为**Manifest**
- 当完成打包并发送到浏览器时，会在运行时通过Manifest来解析和加载模块，无论你选择哪种模块语法，那些<code>import</code>或<code>require</code>语句现在都已经转换成<code>__webpack_require__</code>方法