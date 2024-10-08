# state 如同一张快照

> 设置 state 会触发渲染
> 渲染会及时生成一张快照

-   **设置 state 只会为下一次渲染变更 state 的值**（在点击事件里多次改变 state 的值）
-   **一个 state 变量的值永远不会在一次渲染的内部发生变化**

## React 会对 state 更新进行批处理

> React **会等到事件处理函数中的** 所有 **代码都运行完毕再处理你的 state 更新**

> 在你的事件处理函数及其中任何代码执行完成 **之后**，UI 才会更新。这种特性也就是 批处理

在严格模式下，React 会执行每个更新函数两次（但是丢弃第二个结果）以便帮助你发现错误。

## 自动批处理 Automatic Batching

-   在 React 18 之前，React 只会在事件回调中使用批处理，而在 Promise、setTimeout、原生事件等场景下，是不能使用批处理的（react17 里 setState enqueue TaskQueue 之后，直接 flushSyncCallbackQueue 掉，不再在 port.postMessage 后 flush 了。这也就是为什么 18 之前的版本多次 render 的原因 ；react18 在 <code>scheduleUpdateOnFiber</code>里相当于屏蔽了 ensureRootIsScheduled()后 flushSyncCallbackQueue 的执行来处理批量更新，相当于多了并发模式的判断后再去 flush）。

-   而在 React 18 中，所有的状态更新，都会自动使用批处理，不关心场景
-   如果你在某种场景下不想使用批处理，你可以通过 ReactDOM.flushSync 来强制同步执行（比如：你需要在状态更新后，立刻读取新 DOM 上的数据等
