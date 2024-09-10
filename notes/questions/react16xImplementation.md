# 简单说一下 react 16.x 执行过程

-   jsx 经过 babel 转变成 render 函数
-   create update
-   enqueueUpdate
-   scheduleWork 更新 expirationTime
-   requestWork
-   workLoop 大循环：循环处理每个 fiber 节点
-   Effect List
-   commit

**待扩展对应细节...**

## useEffect 的执行流程

-   commit 阶段的 before-mutation 阶段之前通过 scheduleCallback 进行调度 flushPassiveEffects
-   因为 flushPassiveEffects 函数会遍历 effect，所以 layout 阶段之后，会将 effectList 放入一个全局变量
-   适当的时机，useEffect 会在页面渲染后，即 layout 阶段后执行
-   flushPassiveEffects 的功能是：获取 effectList，遍历执行 effect 的 useEffect 销毁函数，然后再遍历执行 effect 的 useEffect 执行函数，将 destroy 存放在每个 fiber.destroy 上

## React 15.x

> 这个版本及以前对 DOM 的遍历采用的是递归的形式进行，递归的好处就是代码简单，容易理解。可也有致命的缺陷：**难以中断和恢复**，因此，在 Mount、 render 巨大节点的时候，总是那么卡

## Fiber 架构

> 使用 Fiber 架构，React 的性能可以达到前所未有的高度

> 要做到这一点，解决的办法是：

-   使用性能优化神器：requestIdleCallback，将每一帧中浪费的 CPU 时间，利用起来
-   重新实现 React 的树构成栈、更新栈，抛弃递归的方式，**采用循环 ( while )、出栈入栈的形式对树进行遍历**
-   每个、每种虚拟 DOM 节点都提到了升级，添加了 Alternate、child、sibling 和 return 的属性，这些个属性为的就是在更新阶段，能够停止、恢复以达到将 diff 和 patch 全部拆分成每个小任务，整个树，以链表的形式组织
