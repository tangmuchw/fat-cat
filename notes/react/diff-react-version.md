# React 15、16、17、18 各版本的区别（特点）

> 参考[React 各版本性能优化方案原理分析](https://www.jianshu.com/p/25e0c17d43e9)
> 总结：
> react16：提出 fiber，hooks
> react17：提出 lanes、 更改事件处理(把事件添加到 React 渲染树的根 Dom 容器中)
> react18：提出 concurrentMode 并发渲染机制，全自动批处理、startTransition 过度任务

## React15.x

### 组成部分

-   Reconciler：负责调用 render 生成虚拟 Dom 进行 diff，找出变化后的虚拟 Dom
-   Renderer：负责接到 Reconciler 通知，将变化的组件渲染在当前宿主环境，比如浏览器，不同的宿主环境会有不同的 Renderer

### 优化点

因为 setState 是同步的，当同时触发多次 setState 时浏览器会一直被 JS 线程阻塞，那么那么浏览器就会掉帧，导致页面卡顿，所以 React 才引入了批处理的机制，为了将同一上下文中触发的更新合并为一个更新

### 缺陷

主要是因为 react 15 在 mount 或 diff 过程中，并没有考虑到组件树过于庞大的问题，由于这两个过程是从父到子的递归渲染，且浏览器的单线程限制 ui 渲染线程和 js 线程互斥，在运行 JS 的时候，无法渲染 DOM，所以导致在组件树太庞大的情况下，会造成用户卡顿，也无法对页面进行任何操作 => fiber 方案提出

## React16.x

> 在 CPU 上，主要问题是，在 JS 执行超过 16.6 ms 时，页面就会产生卡顿，那么 React 的解决思路：就是

-   **在浏览器每一帧的时间中预留一些时间给 JS 线程，React 利用这部分时间更新组件**。
-   **当预留的时间不够用时，React 将线程控制权交还给浏览器让他有时间渲染 UI，React 则等待下一帧再继续被中断的工作**。

> 浏览器帧的概念：
> 某任务执行时间过长 超过 16ms 渲染就会推迟 造成页面卡顿
> 浏览器大概一帧有 10 毫秒的空闲时间 我们可以在这个空闲做一些事情

### Fiber 大体思路

-   fiber 是一个执行单元
    ，每执行完一个单元，浏览器就会检查剩余多少时间，没有时间就将控制权让出

-   通过 fiber 架构，让协调过程变得不可中断，实时让出 cpu 执行权，提高响应速度

### requestIdleCallback

-   requestIdleCallback 使开发者在主事件循环上执行后台和低优先级工作 不会影响延迟关键事件：动画和输入响应
-   正常帧执行完任务后没超过 16ms 说明有时间空余 就会执行 requestIdleCallback 里面的注册任务
-   requestAnimationFrame 回调会在每一帧确定执行 属于高优先级任务 requestIdleCallback 不一定 它属于低优先级任务

> 由于兼容性和刷新帧率的问题，React 并没有直接使用 requestIdleCallback ， 而是使用了 MessageChannel 模拟实现

#### 核心原理

-   Scheduler：时间切片，调度高优任务进入 Reconciler，可中断渲染
-   Reconciler：双缓存，fiber 构建，diff
-   Renderer：commitRoot

Reconciler 的工作就是使用 Diff 算法对比生成 workInProgress Fiber ，这个阶段是可中断的
Renderer 的工作是把 workInProgress Fiber 转换成真正的 DOM 节点

##### 调度器 Scheduler

调度任务的优先级，高优任务优先进入 Reconciler 利用时间切片，就可以根据当前的宿主环境性能，为每个工作单元分配一个可运行时间，从而实现异步可中断的更新

时间切片的本质，也就是模拟实现 requestIdleCallback 这个函数 看下源码

```Javascript
// 接收 MessageChannel 消息
const performWorkUntilDeadline = () => {
  if (scheduledHostCallback !== null) {
    const currentTime = getCurrentTime(); // 1. 获取当前时间
    deadline = currentTime + yieldInterval; // 2. 设置deadline
    const hasTimeRemaining = true;
    try {
      // 3. 执行回调, 返回是否有还有剩余任务
      const hasMoreWork = scheduledHostCallback(hasTimeRemaining, currentTime);
      if (!hasMoreWork) {
        // 没有剩余任务, 退出
        isMessageLoopRunning = false;
        scheduledHostCallback = null;
      } else {
        port.postMessage(null); // 有剩余任务, 发起新的调度
      }
    } catch (error) {
      port.postMessage(null); // 如有异常, 重新发起调度
      throw error;
    }
  } else {
    isMessageLoopRunning = false;
  }
  needsPaint = false; // 重置开关
};

const channel = new MessageChannel();
const port = channel.port2;
channel.port1.onmessage = performWorkUntilDeadline;

// 请求回调
requestHostCallback = function(callback) {
  // 1. 保存callback
  scheduledHostCallback = callback;
  if (!isMessageLoopRunning) {
    isMessageLoopRunning = true;
    // 2. 通过 MessageChannel 发送消息
    port.postMessage(null);
  }
};
// 取消回调
cancelHostCallback = function() {
  scheduledHostCallback = null;
};
```

时间切片(time slicing)相关：执行时间分割, 让出主线程 把控制权归还浏览器, 浏览器可以处理用户输入, UI 绘制等紧急任务

```Javascript
const localPerformance = performance;
// 获取当前时间
getCurrentTime = () => localPerformance.now();

// 时间切片周期, 默认是5ms(如果一个task运行超过该周期, 下一个task执行之前, 会把控制权归还浏览器)
let yieldInterval = 5;

let deadline = 0;
const maxYieldInterval = 300;
let needsPaint = false;
const scheduling = navigator.scheduling;
// 是否让出主线程
shouldYieldToHost = function() {
  const currentTime = getCurrentTime();
  if (currentTime >= deadline) {
    if (needsPaint || scheduling.isInputPending()) {
      // There is either a pending paint or a pending input.
      return true;
    }
    // There's no pending input. Only yield if we've reached the max
    // yield interval.
    return currentTime >= maxYieldInterval; // 在持续运行的react应用中, currentTime肯定大于300ms, 这个判断只在初始化过程中才有可能返回false
  } else {
    // There's still time left in the frame.
    return false;
  }
};

// 请求绘制
requestPaint = function() {
  needsPaint = true;
};

// 设置时间切片的周期
forceFrameRate = function(fps) {
  if (fps < 0 || fps > 125) {
    // Using console['error'] to evade Babel and ESLint
    console['error'](
      'forceFrameRate takes a positive int between 0 and 125, ' +
        'forcing frame rates higher than 125 fps is not supported',
    );
    return;
  }
  if (fps > 0) {
    yieldInterval = Math.floor(1000 / fps);
  } else {
    // reset the framerate
    yieldInterval = 5;
  }
};
```

##### 任务队列管理

在 Scheduler.js 维护了一个 taskQueue 任务队列管理就是围绕这个 taskQueue 展开
在 unstable_scheduleCallback 函数中

###### 1.创建任务

```Javascript
// 省略部分无关代码
function unstable_scheduleCallback(priorityLevel, callback, options) {
  // 1. 获取当前时间
  var currentTime = getCurrentTime();
  var startTime;
  if (typeof options === 'object' && options !== null) {
    // 从函数调用关系来看, 在v17.0.2中,所有调用 unstable_scheduleCallback 都未传入options
    // 所以省略延时任务相关的代码
  } else {
    startTime = currentTime;
  }
  // 2. 根据传入的优先级, 设置任务的过期时间 expirationTime
  var timeout;
  switch (priorityLevel) {
    case ImmediatePriority:
      timeout = IMMEDIATE_PRIORITY_TIMEOUT;
      break;
    case UserBlockingPriority:
      timeout = USER_BLOCKING_PRIORITY_TIMEOUT;
      break;
    case IdlePriority:
      timeout = IDLE_PRIORITY_TIMEOUT;
      break;
    case LowPriority:
      timeout = LOW_PRIORITY_TIMEOUT;
      break;
    case NormalPriority:
    default:
      timeout = NORMAL_PRIORITY_TIMEOUT;
      break;
  }
  var expirationTime = startTime + timeout;
  // 3. 创建新任务
  var newTask = {
    id: taskIdCounter++,
    callback, // callback: 传入的回调函数
    priorityLevel, // priorityLevel: 优先级等级
    startTime,
    expirationTime, // expirationTime: task的过期时间, 优先级越高 expirationTime = startTime + timeout 越小
    sortIndex: -1,
  };
  if (startTime > currentTime) {
    // 省略无关代码 v17.0.2中不会使用
  } else {
    newTask.sortIndex = expirationTime;
    // 4. 加入任务队列
    push(taskQueue, newTask);
    // 5. 请求调度
    if (!isHostCallbackScheduled && !isPerformingWork) {
      isHostCallbackScheduled = true;
      requestHostCallback(flushWork);
    }
  }
  return newTask;
}
```

维护的队列就是一个小顶堆数组 用 O(1)的复杂度就能找到优先级更高的任务

-   生命周期方法：是最高优先级、同步执行的。
-   受控用户输入：比如输入框内输入文字，同步执行。
-   交互事件：比如动画 requestAnimationFrame，高优先级执行。
-   其他数据请求、使用了 suspense、transition 这样的更新，是低优先级执行的。

###### 2.消费任务

> 创建任务之后, 最后请求调度 requestHostCallback(flushWork)(创建任务源码中的第 5 步), flushWork 函数作为参数被传入调度中心内核等待回调. requestHostCallback 函数在上文调度内核中已经介绍过了, 在调度中心中, 只需下一个事件循环就会执行回调, 最终执行 flushWork

```Javascript
// 省略无关代码
function flushWork(hasTimeRemaining, initialTime) {
  // 1. 做好全局标记, 表示现在已经进入调度阶段
  isHostCallbackScheduled = false;
  isPerformingWork = true;
  const previousPriorityLevel = currentPriorityLevel;
  try {
    // 2. 循环消费队列
    return workLoop(hasTimeRemaining, initialTime);
  } finally {
    // 3. 还原全局标记
    currentTask = null;
    currentPriorityLevel = previousPriorityLevel;
    isPerformingWork = false;
  }
}
```

flushWork 中调用了 workLoop. 队列消费的主要逻辑是在 workLoop 函数中, 这就是 React 工作循环一文中提到的任务调度循环

```Javascript
// 省略部分无关代码
function workLoop(hasTimeRemaining, initialTime) {
  let currentTime = initialTime; // 保存当前时间, 用于判断任务是否过期
  currentTask = peek(taskQueue); // 获取队列中的第一个任务
  while (currentTask !== null) {
    if (
      currentTask.expirationTime > currentTime &&
      (!hasTimeRemaining || shouldYieldToHost())
    ) {
      // 虽然currentTask没有过期, 但是执行时间超过了限制(毕竟只有5ms, shouldYieldToHost()返回true). 停止继续执行, 让出主线程
      break;
    }
    const callback = currentTask.callback;
    if (typeof callback === 'function') {
      currentTask.callback = null;
      currentPriorityLevel = currentTask.priorityLevel;
      const didUserCallbackTimeout = currentTask.expirationTime <= currentTime;
      // 执行回调
      const continuationCallback = callback(didUserCallbackTimeout);
      currentTime = getCurrentTime();
      // 回调完成, 判断是否还有连续(派生)回调
      if (typeof continuationCallback === 'function') {
        // 产生了连续回调(如fiber树太大, 出现了中断渲染), 保留currentTask
        currentTask.callback = continuationCallback;
      } else {
        // 把currentTask移出队列
        if (currentTask === peek(taskQueue)) {
          pop(taskQueue);
        }
      }
    } else {
      // 如果任务被取消(这时currentTask.callback = null), 将其移出队列
      pop(taskQueue);
    }
    // 更新currentTask
    currentTask = peek(taskQueue);
  }
  if (currentTask !== null) {
    return true; // 如果task队列没有清空, 返回ture. 等待调度中心下一次回调
  } else {
    return false; // task队列已经清空, 返回false.
  }
}
```

> 可中断渲染原理：
> 每一次 while 循环的退出就是一个时间切片, 深入分析 while 循环的退出条件: 1.队列被完全清空: 这种情况就是很正常的情况, 没有遇到任何阻碍。 2.执行超时: 在消费 taskQueue 时, 在执行 task.callback 之前, 都会检测是否超时。如果某个 task.callback 执行时间太长(如: fiber 树很大, 或逻辑很重)也会造成超时

在时间切片的基础之上, 如果单个 task.callback 执行时间就很长(假设 200ms). 就需要 task.callback 自己能够检测是否超时, 所以在 fiber 树构造过程中, 每构造完成一个单元, 都会检测一次超时(源码链接), 如遇超时就退出 fiber 树构造循环, 并返回一个新的回调函数(就是此处的 continuationCallback)并等待下一次回调继续未完成的 fiber 树构造.

```Javascript
function workLoopConcurrent() {
  // Perform work until Scheduler asks us to yield
  while (workInProgress !== null && !shouldYield()) {
    performUnitOfWork(workInProgress);
  }
}
```

#### 双缓存

canvas 开发动画时候发现 绘制动画时候需要调用 ctx.clearRect 清除上一帧动画 如果当前帧动画计算量比较大 导致清除上一帧画面到绘制当前帧画面会有很长时间 页面会白屏。

> 什么是双缓存：这种在内存中构建并直接替换的技术
> React 使用“双缓存”来完成 Fiber 树的构建与替换——对应着 DOM 树的创建与更新。
> 在 React 中最多会同时存在两棵 Fiber 树。当前屏幕上显示内容对应的 Fiber 树称为 current Fiber 树，正在内存中构建的 Fiber 树称为 workInProgress Fiber 树。

-   在首次渲染的时候，会创建 fiberRoot 和 rootFiber,fiberRoot 是整个应用的根节点，rootFiber 是组件的根节点
-   接下来进入 render 阶段，根据组件返回的 JSX 在内存中依次创建 Fiber 节点并连接在一起构建 Fiber 树，被称为 workInProgress Fiber 树。
-   在构建 workInProgress Fiber 树时会尝试复用 current Fiber 树中已有的 Fiber 节点内的属性，在首屏渲染时只有 rootFiber 存在对应的 current fiber（即 rootFiber.alternate）
-   渲染完成之后，workInProgress 树会赋值给 current 树

#### 生命周期的改变

在新的 React 架构中，一个组件的渲染被分为两个阶段：

-   第一个阶段也就是 fiber 构建的阶段是可以被 React 打断的，一旦被打断，这阶段所做的所有事情都被废弃，当 React 处理完紧急的事情回来会重新渲染这个组件，这时候第一阶段的工作会重做一遍
-   第二个阶段叫做 commit 阶段，一旦开始就不能中断，也就是说第二个阶段的工作会直接做到这个组件的渲染结束

> 两个阶段的分界点，就是 render 函数。**render 函数之前的所有生命周期函数（包括 render)都属于第一阶段，之后的都属于第二阶段**。开启 Concurrent Mode 之后， render 之前的所有生命周期都有可能会被打断，或者重复调用 比如如下生命周期：componentWillMount componentWillReceiveProps componentWillUpdate

### React16.x 缺陷

在 expirationTime 最开始被设计的时候，React 体系中还没有 Suspense 异步渲染 的概念。假如现在有这样的场景: 有 3 个任务, 其优先级 A > B > C，正常来讲只需要按照优先级顺序执行就可以。
但是现在有这样的情况：A 和 C 任务是 CPU 密集型，而 B 是 IO 密集型 （Suspense 会调用远程 api, 算是 IO 任务）， 即 A(cpu) > B(IO) > C(cpu)，在这种情况下呢，高优先级 IO 任务会中断低优先级 CPU 任务，这显然，是不合理的

## React17.x

### 多版本共存

17 版本之前的 react 如果存在多版本嵌套 如果页面上有多个 React 版本，他们都将在顶层注册事件处理器。这会破坏 e.stopPropagation()：如果嵌套树结构中阻止了事件冒泡，但外部树依然能接收到它。这会使不同版本 React 嵌套变得困难重重

react 实现了自己的一套事件机制并绑定到 **document** 上 也就是自己的合成事件 当我们触发一个事件的时候 这样可以抹平各个浏览器的兼容性问题

### React 17 React 会把事件 attach 到 React 渲染树的根 DOM 容器中

> 绑定在根 DOM 容器上 这样就有效将嵌套的 React 版本隔离开来 事件不会相互影响

### 新的优先级算法 lanes

但是现在有这样的情况：A 和 C 任务是 CPU 密集型，而 B 是 IO 密集型 （Suspense 会调用远程 api, 算是 IO 任务）， 即 A(cpu) > B(IO) > C(cpu)，在这种情况下呢，高优先级 IO 任务会中断低优先级 CPU 任务

那么使用 expirationTime ，它是以某一优先级作为整棵树的优先级更新标准，而并不是某一个具体的组件，这时我们的需求是需要把 任务 B 从 一批任务 中分离出来，先处理 cpu 任务 A 和 C ，如果通过 expirationTime 很难表示批的概念，也很难从一批任务里抽离单个任务，这时呢，我们就需要一种更细粒度的优先级。

> lanes 具体细节可见[lane (车道模型)类型任务的位掩码优先级体系](./17x/lanes.md)

## React18.x

### Concurrent Rendering 并发渲染机制

在 React 18 版本中，ReactDOM.createRoot() 替代了通常作为程序入口的 ReactDOM.render() 方法。这个方法主要是防止 React 18 的不兼容更新导致你的应用程序崩溃

### 批处理的优化

全自动批处理：
v18 实现「自动批处理」的关键在于两点：

-   1.增加调度的流程
-   2.不以全局变量 executionContext 为批处理依据，而是以更新的优先级为依据

调度流程部分源码：

```Javascript
//调度流程
function ensureRootIsScheduled(root, currentTime) {

  // 获取当前所有优先级中最高的优先级
  var nextLanes = getNextLanes(root, root === workInProgressRoot ? workInProgressRootRenderLanes : NoLanes);
  // 本次要调度的优先级
  var newCallbackPriority = getHighestPriorityLane(nextLanes);
  // 已经存在的调度的优先级
  var existingCallbackPriority = root.callbackPriority;
  if (existingCallbackPriority === newCallbackPriority) {
    return;
  }
  // 调度更新流程
  newCallbackNode = scheduleCallback(schedulerPriorityLevel, performConcurrentWorkOnRoot.bind(null, root));

  root.callbackPriority = newCallbackPriority;
  root.callbackNode = newCallbackNode;
}
```

> 节选后的调度流程大体是： 1.获取当前所有优先级中最高的优先级 2.将步骤 1 的优先级作为本次调度的优先级 3.看是否已经存在一个调度 4.如果已经存在调度，且和当前要调度的优先级一致，则 return 5.不一致的话就进入调度流程
> 可以看到，调度的最终目的是在一定时间后执行 performConcurrentWorkOnRoot，正式进入更新流程。

第一次调用 this.setState，进入「调度流程」后，不存在 existingCallbackPriority 所以会执行调度：

第二次调用 this.setState，进入「调度流程」后，已经存在 existingCallbackPriority，即第一次调用产生的。

此时比较两者优先级：由于两个更新都是在 onClick 中触发，拥有同样优先级，所以 return。
按这个逻辑，即使多次调用 this.setState，如：

```Javascript
onClick() {
  this.setState({ b: 1 });
  this.setState({ b: 2 });
  this.setState({ b: 3 });
}
```

只有第一次调用会执行调度，后面几次执行由于优先级和第一次一致会 return。
当一定时间过后，第一次调度的回调函数 performConcurrentWorkOnRoot 会执行，进入更新流程。
由于每次执行 this.setState 都会创建 update 并挂载在 fiber 上 所以即使只执行一次更新流程，还是能将状态更新到最新

### startTransition 属性

什么是过度任务？

-   第一类紧急更新任务。比如一些用户交互行为，按键，点击，输入等。
-   第二类就是过渡更新任务。比如 UI 从一个视图过渡到另外一个视图。

举一个很常见的场景：就是有一个 input 表单。并且有一个大量数据的列表，通过表单输入内容，对列表数据进行搜索，过滤。那么在这种情况下，就存在了多个并发的更新任务

我们希望输入框状态改变更新优先级要大于列表的更新的优先级。 这个时候我们的主角就登场了。用 startTransition 把两种更新区别开。

> 为什么不用 setTimeout？
> startTransition 的处理逻辑和 setTimeout 有一个很重要的区别，setTimeout 是异步延时执行，而 startTransition 的回调函数是同步执行的。在 startTransition 之中任何更新，都会标记上 transition，React 将在更新的时候，判断这个标记来决定是否完成此次更新 所以 Transition 可以理解成比 setTimeout 更早的更新
> 对于渲染并发的场景下，setTimeout 仍然会使页面卡顿。因为超时后，还会执行 setTimeout 的任务，它们与用户交互同样属于宏任务，所以仍然会阻止页面的交互。那么 transition 就不同了，在 conCurrent mode 下，startTransition 是可以中断渲染的 ，所以它不会让页面卡顿，React 让这些任务，在浏览器空闲时间执行，所以上述输入 input 内容时，startTransition 会优先处理 input 值的更新，之后才是列表的渲染
