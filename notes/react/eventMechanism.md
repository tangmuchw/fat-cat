# React 事件机制

> 参考[「react 进阶」一文吃透 react 事件系统原理](https://juejin.cn/post/6955636911214067720#heading-4)

// 待补充完整

## React 16.x

-   在 jsx 中绑定的事件,根本就没有注册到真实的 dom 上。是绑定在 document 上统一管理的。

-   真实的 dom 上的 click 事件被单独处理，已经被 react 底层替换成空函数。

-   在 react 绑定的事件，比如 onChange，在 document 上，可能有多个事件与之对应。

-   react 并不是一开始，把所有的事件都绑定在 document 上，而是采取了一种按需绑定，比如发现了 onClick 事件,再去绑定 document click 事件。

### 事件池

```JavaScript
 handlerClick = (e) => {
    console.log(e.target) // button
    setTimeout(()=>{
        console.log(e.target) // null
    }, 0)
}
```

-   对于一次点击事件的处理函数，在正常的函数执行上下文中打印 e.target 就指向了 dom 元素，但是在 setTimeout 中打印却是 null，如果这不是 React 事件系统，两次打印的应该是一样的，但是为什么两次打印不一样呢？** 因为在 React 采取了一个事件池的概念，每次我们用的事件源对象，在事件函数执行之后，可以通过 <code>releaseTopLevelCallbackBookKeeping</code> 等方法将事件源对象释放到事件池中，这样的好处每次我们不必再创建事件源对象，可以从事件池中取出一个事件源对象进行复用，在事件处理函数执行完毕后，会释放事件源到事件池中，清空属性，这就是 setTimeout 中打印为什么是 null 的原因了。**

## React 17.x

-   事件统一绑定 container 上，ReactDOM.render(app， container)；而不是 document 上，这样好处是有利于微前端的，微前端一个前端系统中可能有多个应用，如果继续采取全部绑定在 document 上，那么可能多应用下会出现问题
-   React 17 中终于支持了原生捕获事件的支持， 对齐了浏览器原生标准。同时 onScroll 事件不再进行事件冒泡。onFocus 和 onBlur 使用原生 focusin， focusout 合成。
-   取消事件池 React 17 取消事件池复用，也就解决了上述在 setTimeout 打印，找不到 e.target 的问题。
