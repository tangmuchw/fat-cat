# 发布订阅者模式

> 发布订阅模式称观察者模式，它定义对象间的一种一对多的依赖关系，当一个对象状态改变的时候，所有依赖于它对象都将得到通知.

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
     remove: function(key){
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

 subscriber.listen('click', (whom) => { console.log('change click =>', whom)})

 publisher.trigger('click', 'dom')

```
