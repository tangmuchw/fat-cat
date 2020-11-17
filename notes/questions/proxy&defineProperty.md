# 实现双向绑定 Proxy 比 defineProperty 优劣如何

> 实现一个完整的双向绑定需要以下几个要点:

- 利用<code>Proxy</code>或<code>Object.defineProperty</code>生成的 Observer 针对对象/对象的属性进行“劫持”，在属性发生变化后通知订阅者

- 解析器 Compile 解析模版中的 Directive（指令），收集指令所依赖的方法和数据，等待数据变化后进行渲染

- Watcher 属于 Observer 和 Compile 桥梁，他将接收到的 Observer 产生的数据变化，并根据 Compile 提供的指令进行视图渲染，使得数据变化促使视图变化

## defineProperty

### 特点：

- 无法监听数组变化 （但可以通过监听数组的操作方法，来监听数组变化）
- 只能劫持对象的属性，需要多次用遍历方法遍历对象的属性
- 修改属性时，是直接对对象属性直接修改

### defineProperty-语法

> Object.defineProperty(obj, prop, descriptor)
> 注意： **value、writable 不能和 set、 get 同时出现**

```JavaScript
 let obj = {}

 Object.defineProperty(obj, 'property1', {
     value: 44,
     writable: false,
 })


 Object.defineProperty(obj, 'property2', {
    set: (v) => {
        this.value = v
    },
    get: () => {
        return this.value
    }
 })

 // 定义多个属性
 Object.defineProperties(obj, {
     _year: {
         value: 3,
     },
     property4: {
         value: 4,
     },
     year: {
         get: function(){
             return this._year
         }
     }
 })
```

## proxy

### 特点：

- 可以直接监听对象而非属性
- 可以直接监听数组的变化
- Proxy 有多达 13 种拦截方法, 不限于 apply、ownKeys、deleteProperty、has 等等是 Object.defineProperty 不具备的
- Proxy 返回的是一个新对象, 可以只操作新的对象达到目的
- 缺点：兼容性问题

```JavaScript
 const p = new Proxy({}, {
     get: (obj, prop) => {
         return prop in obj ? obj[prop] : undefined
     },
     set: (obj, prop, val) => {
        // TODO: 可以在赋值前做一些数据校验的处理

        obj[prop] = val

        // 表示成功，也可以忽略不用这一行代码
        return true

     }
 })

 p.age = 20
 console.log(p.age) // 20
```
