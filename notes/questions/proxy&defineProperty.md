# 实现双向绑定Proxy比defineProperty优劣如何

>>实现一个完整的双向绑定需要以下几个要点:
- 利用<code>Proxy</code>或<code>Object.defineProperty</code>生成的Observer针对对象/对象的属性进行“劫持”，在属性发生变化后通知订阅者

- 解析器Compile解析模版中的Directive（指令），收集指令所依赖的方法和数据，等待数据变化后进行渲染

- Watcher属于Observer和Compile桥梁，他将接收到的Observer产生的数据变化，并根据COmpile提供的指令进行视图渲染，使得数据变化促使视图变化


## defineProperty
### 特点：
- 无法监听数组变化 （但可以通过监听数组的操作方法，来监听数组变化）
- 只能劫持对象的属性，需要多次用遍历方法遍历对象的属性
- 修改属性时，是直接对对象属性直接修改


## proxy
### 特点：
- 可以直接监听对象而非属性
- 可以直接监听数组的变化
- Proxy有多达13种拦截方法, 不限于apply、ownKeys、deleteProperty、has等等是Object.defineProperty不具备的
- Proxy返回的是一个新对象, 可以只操作新的对象达到目的
- 缺点：兼容性问题