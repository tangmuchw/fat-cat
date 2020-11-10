# Memory Management 管理内存

> 一旦有数据不再有用，通过将其值设置为 null 来释放其引用--这个做法叫做「解除引用」（dereferencing）.

- 解除一个值的引用并不意味着自动回收该值所占用的内存
- 解除引用的真正作用是让值脱离执行环境，以便垃圾收集器下次运行时将其回收

```JavaScript
function createPerson(name){
    var localPerson = {
        name
    }

    return localPerson
}

var globalPerson = createPerson('fatCat')
globalPerson = null
```
