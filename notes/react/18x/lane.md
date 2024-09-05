# lane (车道模型)类型任务的位掩码优先级体系

> 从值的角度来看，位掩码就是一个二进制数。所谓的「lane」就是只有一位为 1，其他位都是 0 的二进制数；而「lanes」就是有多个位为 1，其他位都是 0 的二进制数(31 位)。

-   能够表示一种类型任务的位掩码称之为「lane」；
-   能够表示一批任务（由不同类型任务所组成）的位掩码称之为「lanes」；

## 用十进制值表示任务优先级存在两个不足点

-   数值既用来表示一个优先级也用来表示一批优先级。单个优先级跟批量优先级的概念耦合在一块了

-   无法满足 react 中高频的优先级运算场景对优先级运算高效性和便利性方面的要求；
    一条 lane 就可以表示多个具有相同优先级的任务。而在 expirationTime 模型中，这需要多个十进制值来表示。这无疑会占用更多的内存。

## lane 的生命周期可以分为几个阶段：

-   **产生**：lane 是从无到有来生产出来；
-   **分发**：产生的 lane 最终是被分发到 update 对象，普通的 fiber 节点和 fiber root node 上面去；
-   **消费**：lane 最终是参与到末端消费，即用于某种用途。

## react 在每一次创建 update 对象之前都会做一个动作：请求一条 lane - requestUpdateLane()

```Javascript
// react@18.2.0/packages/react-reconciler/src/ReactFiberWorkLoop.old.js
function requestUpdateLane(fiber) {
  // Special cases
  const mode = fiber.mode;

  if ((mode & ConcurrentMode) === NoMode) {
    return SyncLane;
  } else if (
    (executionContext & RenderContext) !== NoContext &&
    workInProgressRootRenderLanes !== NoLanes
  ) {
    // This is a render phase update. These are not officially supported. The
    // old behavior is to give this the same "thread" (lanes) as
    // whatever is currently rendering. So if you call `setState` on a component
    // that happens later in the same render, it will flush. Ideally, we want to
    // remove the special case and treat them as if they came from an
    // interleaved event. Regardless, this pattern is not officially supported.
    // This behavior is only a fallback. The flag only exists until we can roll
    // out the setState warning, since existing code might accidentally rely on
    // the current behavior.
    return pickArbitraryLane(workInProgressRootRenderLanes);
  }

  const isTransition = requestCurrentTransition() !== NoTransition;

  if (isTransition) {
    // updates at the same priority within the same event. To do this, the
    // inputs to the algorithm must be the same.
    //
    // The trick we use is to cache the first of each of these inputs within an
    // event. Then reset the cached values once we can be sure the event is
    // over. Our heuristic for that is whenever we enter a concurrent work loop.

    if (currentEventTransitionLane === NoLane) {
      // All transitions within the same event are assigned the same lane.
      currentEventTransitionLane = claimNextTransitionLane();
    }

    return currentEventTransitionLane;
  } // Updates originating inside certain React methods, like flushSync, have
  // their priority set by tracking it with a context variable.
  //
  // The opaque type returned by the host config is internally a lane, so we can
  // use that directly.
  // TODO: Move this type conversion to the event priority module.

  const updateLane = getCurrentUpdatePriority();

  if (updateLane !== NoLane) {
    return updateLane;
  } // This update originated outside React. Ask the host environment for an
  // appropriate priority, based on the type of event.
  //
  // The opaque type returned by the host config is internally a lane, so we can
  // use that directly.
  // TODO: Move this type conversion to the event priority module.

  const eventLane = getCurrentEventPriority();
  return eventLane;
}


```

## react 是这样生产 lane 的：

-   如果当前是同步渲染模式，返回 SyncLane；
-   如果是在 render 阶段触发了更新请求，不会生产一个新 lane；
-   如果当前的更新请求是 transition 类型的更新请求，则从 16 条 transition lane 中选择一条返回；
-   如果当前是在离散型事件触发了更新请求，返回 SyncLane;
-   如果当前是在连续型事件触发了更新请求，返回 InputContinuousLane;
-   如果当前是在其他 DOM 事件（排除「离散型事件」和「连续型事件」）中触发了更新请求，返回 DefaultLane;
-   如果当前是在 react 外部方法中触发了更新请求，返回 DefaultLane;

鉴于 react 对这些「常量 lane 的赋值」和「**lane 的值越小，则代表优先级越高**」的定性，那么从优先级比较的角度出发，我们可以得到这样的结论：

```HTML
离散型事件中触发的更新请求的优先级 >
连续型事件中触发的更新请求的优先级 >
其他 DOM 事件中触发的更新请求的优先级 =
react 外部方法中触发的更新请求的优先级 >
startTransition 中触发的更新请求的优先级
```

## React 按照事件的紧急程度，把它们划分成三个等级：

-   离散事件（DiscreteEvent）：click、keydown、focusin 等，这些事件的触发不是连续的，优先级为 0。
-   用户阻塞事件（UserBlockingEvent）：drag、scroll、mouseover 等，特点是连续触发，阻塞渲染，优先级为 1。
-   连续事件（ContinuousEvent）：canplay、error、audio 标签的 timeupdate 和 canplay，优先级最高，为 2。
