[toc]

> 摘自[畅谈 this 的四种绑定方式](https://juejin.cn/post/7018413160168177700)

# this 绑定方式（四种）

## 默认绑定

> 默认绑定时，使用严格模式，不能将全局对象用于默认绑定，<code>this</code> 会绑定到<code>undefined</code>

```JavaScript
function say(){
    console.log(this)
}

say() // window
```

```JavaScript
function say(){
    'use strict'
    console.log(this)
}

say() // undefined
```

## 隐式绑定

> 当函数引用有上下文对象时，隐式绑定会把函数调用中的 this 绑定到这个上下文对象

-   **本质上**，判断隐式绑定时，必须是一个对象内部包含一个指向函数的属性，通过这个属性间接的引用函数，从而把 this 间接（隐式）绑定到这个对象中

```JavaScript
function say(){
    console.log(this.name)
}

const person = {
    name: 'tmchw',
    say,
}

function createBoy() {
    return person
}

const boy = createBoy()

boy.say() // tmchw
person.say() // tmchw
```

### 隐式丢失

-   引用赋值隐式丢失

```JavaScript
function say(){
    console.log(this.name)
}

const person = {
    name: 'tmchw',
    say,
}

const talk = person.say
talk() // undefined

// talk 实际上引用的 say 函数本身，所以应用了默认绑定，这是的 this 指向 window
```

-   参数传递隐式丢失

```JavaScript
function say(){
    console.log(this.name)
}

function talk(fn){
  fn()
}

const person = {
    name: 'tmchw',
    say,
}

talk(person.say) // undefined

// 参数传递，其实也是一种隐式赋值，逻辑和「引用赋值隐式丢失」一样
```

## 显示绑定

> 调用函数时，强制响函数绑定到<code>this</code>，可以通过<code>call</code>、<code>apply</code>、<code>bind</code> 方法实现

-   硬绑定：等同于 bind
-   new 绑定

## 绑定优先级

> new 绑定 > 显示绑定 > 隐式绑定 > 默认绑定
