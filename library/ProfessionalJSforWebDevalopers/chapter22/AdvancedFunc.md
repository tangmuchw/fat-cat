[toc]

# 高级函数

## 安全的类型检测

> Object.prototype.toString.call([]) // '[object Array]'

## 惰性载入函数

> 如果 id 语句 不必每次执行，name 代码可以运行地更快一些，解决方案就是**惰性载入**，即表示函数执行的分支仅会发生一次。实现方式如下：

- 在函数被调用时再处理函数，即根据条件，重写对应函数的逻辑
- 在声明函数时就指定适当的函数

## 函数柯里化

```JavaScript
function curry(fn) {
    var args = Array.prototype.slice.call(arguments, 1)

    return function(){
        var innerArgs = Array.prototype.slice.call(arguments)
        var finalArgs = args.cat(innerArgs)
        return fn.apply(null, finalArgs)
    }
}

function add(num1, num2){
    return num1 + num2
}

var curriedAdd = curry(add, 5)

console.log(curriedAdd(3)) // 8

```
