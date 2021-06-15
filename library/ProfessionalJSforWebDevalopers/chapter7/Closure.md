# Closure 闭包

> 闭包是指**有权访问另一个函数作用域中的变量的函数**

- 创建闭包的常见方式，就是在一个函数内部创建另一个函数。
  - 返回函数
  - 函数当作参数传递
- 闭包只能取得包含函数中任何变量的最后一个值，所保存的是整个变量对象，而不是某个特殊的变量
- 闭包的应用场景：柯里化， 模块

```JavaScript
function createComparisonFunction(propertyName){

    return function(obj1, obj2){
        var val1 = obj1[propertyName] // 加粗
        var val2 = obj2[propertyName] // 加粗

        if(val1 < val2) return -1

        if(val1 > val2) return 1

        return 0
    }
}

// 回收闭包
var compareNames = createComparisonFunction('name')
var result = compareNames({ name: 'Tom'}, { name: 'Jon' })
compareNames = null

```

## 如何创建作用域链以及作用域链有什么作用

- 当某个函数第一次被调用时，会创建一个执行环境(execution context)及相应的作用域链
- 并把作用域链赋值给一个特殊的内部属性(即[[Scope]]])
- 然后，使用 this、arguments 和其他命名参数的值来初始化函数的活动对象(activation object)
- 注意在作用域链中，外部函数的活动对象始终处于第二位，外部函数的外部函数的活动对象处于第三位，......直至作为作用域链终点的全局执行环境
- 在函数执行过程中，为读取和写入变量的值，就需要在作用域链中查找变量

## 闭包与变量

```JavaScript
function createFunction(){
    var result = []

    for(var i = 0; i < 10; i++){
        result[i] = function(){
            return i
        }
    }

    return result
}

createFunction() // 即位置 0 到 9 的函数都返回 10

```

```JavaScript
function createFunction(){
    var result = []

    for(var i = 0; i < 10; i++){
        result[i] = (function(num){
            return function(){
                return num
            }
        })(i)
    }

    return result
}

createFunction() // 即位置 0 到 9 的函数都返回对应下标

```

## 关于 this 对象

> 匿名函数的执行环境具有全局性，指向 window

```JavaScript
var name = 'This Window'

var obj = {
    name: 'My Obj',

    getNameFunc: function(){
        return function(){
            return this.name
        }
    }
}


console.log(obj.getNameFunc()()) // This Window

```

## 块级作用域

> 只要没有指向匿名函数的引用，只要函数执行完毕，就可以立即销毁其作用域链

```JavaScript
(function(){
    // 这里是块级作用域
})()

```
