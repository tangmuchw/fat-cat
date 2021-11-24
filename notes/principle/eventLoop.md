# Javascript 之 Event Loop(事件循环)

> 根据规范，事件循环时通过**任务队列**的机制来进行协调的。

- 一个 Event Loop => 一个或者多个任务队列（task queue）
- 一个任务队列 => 一系列有序任务（task）的集合
- 每个任务 => 一个任务源（task source）

## 特点

- JS 引擎是单线程的
- Event Loop 是 javascript 的执行机制
- 微任务优于宏任务

```Javascript
    //请写出输出内容
    async function async1() {
        console.log('async1 start');
        await async2();
        console.log('async1 end');
    }
    async function async2() {
      console.log('async2');
    }

    console.log('script start');

    setTimeout(function() {
        console.log('setTimeout');
    }, 0)

    async1();

    new Promise(function(resolve) {
        console.log('promise1');
        resolve();
    }).then(function() {
        console.log('promise2');
    });
    console.log('script end');

    /*
      script start
      async1 start
      async2
      promise1
      script end
      async1 end
      promise2
      setTimeout
    */

   // Learn from: https://github.com/Advanced-Frontend/Daily-Interview-Question/issues/7
```

### 前菜-任务队列

- JS 分为**同步任务**和**异步任务**
- 同步任务都在主线程上执行，形成一个**执行栈**
- 主线程之外，事件触发线程管理着一个**任务队列**，只要异步任务有了运行结果，就在任务队列之中放置一个事件
- 一旦执行栈中的所有同步任务执行完毕（此时**JS 引擎空闲**），系统就会读取任务队列，将可运行的异步任务添加到可执行栈中，开始执行

### 主菜-宏任务

- 概念：每次执行栈执行的代码就是一个宏任务（macro task）
- 与 DOM 任务交互流程： 会在一个 macro task 执行结束后，在下一个 macro task 执行开始前，对页面进行渲染, 即 macro task => 渲染 => macro task
- 场景：
  - script（整体代码）
  - setTimeout
  - setInterval
  - I/O
  - UI 交互事件
  - postMessage
  - MessageChannel: 允许我们创建一个新的消息通道，并通过它的两个 MessagePort 属性发送数据。
  - setImmediate(Node.js)

### 主菜-微任务

- 概念：在当前 task 执行结束后立即执行的任务（micro task）
- 场景：
  - Promise.then
  - MutationObserver: 提供了监视对 DOM 树所做更改的能力
  - process.nextTick(Node.js)

### 甜品-运行机制

```
                               --- N --> 浏览器渲染 -> 下一个宏任务
                               |
宏任务 -> 执行结束 ->  有微任务？ --
                               |
                               --- Y --> 执行所有微任务 -> 浏览器渲染 -> 下一个宏任务
```

### 甜品-Promise 和 async

- Promise 中的异步体现在 then 和 catch 中，所以**写在 Promise 中的代码是被当做同步任务立即执行的**
- async/await，再出现 await 出现之前，其中的代码也是立即执行的

### 甜品-await

- 实际上 await 是**一个让出线程的标志**，await 后面的表达式会先执行一遍，将 await 后面的代码加入到 micro task 中，然后就会跳出 async 函数来执行后面的代码

## Promise.then 的执行顺序

- 当前一个 then 中的代码都是同步执行的，执行结束后第二个 then 即可注册进入微任务队列
- 当前一个 then 中有 return 关键字，需要 return 的内容完全执行结束,第二个 then 才会注册进入微任务队列

```JavaScript
new Promise((resolve, reject) => {
    console.log(1)
    reject(2)
    console.log(2)
})
    .then(() => console.log(3))
    .catch(() => console.log(4))
    .then(() => {
        console.log(5)
        Promise.reject().catch(() => console.log('5-1'))
    })
    .catch(() => console.log(6))
    .then(() => {
        console.log(7)
        new Promise((resolve, reject) => {
            console.log(8)
            resolve()
        })
            .then(() => console.log(9))
            .then(() => console.log(10))


        Promise.resolve().then(() => console.log('promise.resolve'))

        // 有没有 return 结果是一样的
        return new Promise((resolve, reject) => {
            console.log(11)
            reject()
        })
            .then(() => console.log(12))
            .catch(() => console.log(13))
            .then(() => console.log(15))
    })
    .catch(() => console.log(16))
    .then(() => console.log(17))

// 1
// 2
// 4
// 5
// 5-1
// 7
// 8
// 11
// 9
// promise.resolve
// 10
// 13
// 15
// 17

```
