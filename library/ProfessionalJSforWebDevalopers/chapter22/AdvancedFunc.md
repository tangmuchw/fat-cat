[toc]

# 高级函数

## 安全的类型检测

> Object.prototype.toString.call([]) // '[object Array]'

## 惰性载入函数

> 如果 id 语句 不必每次执行，name 代码可以运行地更快一些，解决方案就是**惰性载入**，即表示函数执行的分支仅会发生一次。实现方式如下：

- 在函数被调用时再处理函数，即根据条件，重写对应函数的逻辑
- 在声明函数时就指定适当的函数

## 函数式编程

> 在函数式编程中，函数就是一个管道（pipe）。这头进去一个值，那头就会出来一个新的值，没有其他作用

- 函数式编程有两个最基本的运算：合成和柯里化

### 函数柯里化

> "柯里化"，就是把一个多参数的函数，转化为单参数函数。

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

```JavaScript
// 柯里化之前
function add(x, y) {
  return x + y;
}

add(1, 2) // 3

// 柯里化之后
function addX(y) {
  return function (x) {
    return x + y;
  };
}

addX(2)(1) // 3

// 合成
const compose = function (f, g) {
  return function (x) {
    return f(g(x));
  };
}
```

### 合成

```JavaScript
// 合成
const compose = function (f, g) {
  return function (x) {
    return f(g(x));
  };
}
```

> 如果一个值要经过多个函数，才能变成另外一个值，就可以把所有中间步骤合并成一个函数，这叫做"函数的合成"（compose）
