# 发布订阅者模式

> 发布订阅模式，它定义对象间的一种一对多的依赖关系，当一个对象状态改变的时候，所有依赖于它对象都将得到通知.

```JavaScript
// 发布者
 const publisher = {
     queue: new Map(),
     listen: function(key, fn) {
         const _map = this.queue
         _map.set(key, fn)
     },
     trigger: function(key) {
        const _map = this.queue
        const hasKey = _map.has(key)

        if(!hasKey) return

        const fn = _map.get(key)

        const args = Array.prototype.slice.call(arguments, 1)
        console.log(args)
        typeof fn === 'function' && fn.apply(this, args)
     },
     remove: function(key) {
        const _map = this.queue
        const hasKey = _map.has(key)

        if(!hasKey) return

        _map.delete(key)
     }
 }

// 订阅者
 const initSubscriber = () => {
     return publisher
 }

 const subscriber = initSubscriber()

 subscriber.listen('click', (whom) => { console.log('change click =>', whom) }) // 动态维护订阅者

// 观察者列表
 function handlerWhom(whom) {
     console.log('change click =>', whom)
 }

subscriber.listen('click', handlerWhom)

 publisher.trigger('click', 'dom')

```

## 发布订阅模式与观察者模式的区别是什么

- 在观察者模式中，被观察者通常会维护一个观察者列表。当被观察者的状态发生改变时，就会通知观察者。
- 在发布订阅模式中，具体发布者会动态维护一个订阅者的列表，可在运行时根据程序需要开始或停止发布给对应订阅者的时间通知

> 区别在于发布者本身并不维护订阅列表（它不会像观察者一样主动维护一个列表），它会将工作委派给具体发布者（相当于秘书，任何人想知道我的事情，直接问我的秘书就可以了）；订阅者在接收到发布者的消息后，会委派具体的订阅者来进行相关的处理
