# Javascript之Event Loop(事件循环)
>> 根据规范，事件循环时通过**任务队列**的机制来进行协调的。
 - 一个Event Loop => 一个或者多个任务队列（task queue）
 - 一个任务队列 => 一系列有序任务（task）的集合
 - 每个任务 => 一个任务源（task source）

 ## 特点
 - JS引擎是单线程的
 - Event Loop是javascript的执行机制
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
  - JS分为**同步任务**和**异步任务**
  - 同步任务都在主线程上执行，形成一个**执行栈**
  - 主线程之外，事件触发线程管理着一个**任务队列**，只要异步任务有了运行结果，就在任务队列之中放置一个事件
  - 一旦执行栈中的所有同步任务执行完毕（此时**JS引擎空闲**），系统就会读取任务队列，将可运行的异步任务添加到可执行栈中，开始执行


### 主菜-宏任务
 - 概念：每次执行栈执行的代码就是一个宏任务（macro task）
 - 与DOM任务交互流程： 会在一个macro task执行结束后，在下一个macro task执行开始前，对页面进行渲染, 即macro task => 渲染 => macro task
 - 场景：
    + script（整体代码）
    + setTimeout
    + setInterval
    + I/O
    + UI交互事件
    + postMessage
    + MessageChannel: 允许我们创建一个新的消息通道，并通过它的两个MessagePort 属性发送数据。
    + setImmediate(Node.js)

### 主菜-微任务
 - 概念：在当前task执行结束后立即执行的任务（micro task）
 - 场景：
    + Promise.then
    + MutationObserver: 提供了监视对DOM树所做更改的能力
    + process.nextTick(Node.js)

### 甜品-运行机制
   ```
                                  --- N --> 浏览器渲染 -> 下一个宏任务
                                  |
   宏任务 -> 执行结束 ->  有微任务？ --
                                  |
                                  --- Y --> 执行所有微任务 -> 浏览器渲染 -> 下一个宏任务
   ```

### 甜品-Promise和async
 - Promise中的异步体现在then和catch中，所以**写在Promise中的代码是被当做同步任务立即执行的**
 - async/await，再出现await出现之前，其中的代码也是立即执行的

### 甜品-await
 - 实际上await是**一个让出线程的标志**，await后面的表达式会先执行一遍，将await后面的代码加入到micro task中，然后就会跳出async函数来执行后面的代码

