# Recursion 递归

```JavaScript

function factorial(num){
    if(num <= 1) return 1

    return num * factorial(num - 1)
}

var anotherFactorial = factorial
factorial = null
alert(anotherFactorial(4)) // 出错


// fix: 上述错误
function factorialCallee(num){
    if(num <= 1) return 1

    return num * argument.callee(num - 1)
}


// 在严格模式下，不能通过脚本访问 argument.callee
// 改进如下
var factorialAdvance = (function f(num){
    if(num <= 1) return 1

    return num * f(num - 1)
})


```
