
# tree shaking
>> tree shaking，通常用于描述溢出JavaScript上下文中的未引用代码。它依赖于ES2015模块系统中的<code>静态机构特性</code>，例如<code>import</code>和<code>export</code>


- 新的 webpack 4 正式版本，扩展了这个检测能力，通过 package.json 的<code>sideEffects</code>属性作为标记，向 compiler 提供提示，表明项目中的哪些文件是 "pure(纯的 ES2015 模块)"，由此可以安全地删除文件中未使用的部

>> 简单来说，就是做打包优化的，检测bundle后的代码中，没被用到js代码，并根据配置决定是否删除掉