# Concurrent Mode（React >= 18.x）

> Concurrent Mode（以下简称 CM）翻译叫并发模式。CM 本身并不是一个功能，而是一个底层设计，它使 **React 能够同时准备多个版本的 UI**
> 在 CM 模式下，React 在执行过程中，每执行一个 Fiber，都会看看有没有更高优先级的更新，如果有，则当前低优先级的的更新会被暂停，待高优先级任务执行完之后，再继续执行或重新执行。

## React 的渲染流程

-   React 是通过 JSX 描述页面的，将**JSX 编译成 render function**（也就是 React.createElement 等），**执行之后产生 vdom**。
-   之后这个 **vdom 会转换为 fiber 结构**（vdom 是通过 children 关联子节点，而 fiber 通过 child、sibling、return 关联了父节点、子节点、兄弟节点）
    -   从 **vdom 转 fiber 的过程叫做 reconcile（调和）**，这个过程还会创建用到的 dom 节点，并且打上增删改的标记。这个 reconcile 的过程叫做 render 阶段
-   之后 commit 阶段会根据标记来增删改 dom。commit 阶段也分为了 3 个小阶段，before mutation、mutation、layout

    -   before mutation 是在 dom 操作之前，mutation 阶段会增删改 dom，layout 是在 dom 操作之后

> 综上：React 整体的渲染流程就是 render（reconcile 的过程） + commit（执行增删改 dom 和 effect、生命周期函数的执行、ref 的更新等）

-   多次 setState 会引起多个渲染流程，这之间可能有重要程度的不同，也就是优先级的不同。

    -   为了让高优先级的更新能先渲染，react 实现了并发模式。

    -   **同步模式是循环处理 fiber 节点，并发模式多了个 shouldYield 的判断，每 5ms 打断一次，也就是时间分片**。并且之后会重新调度渲染。通过这种打断和恢复的方式实现了并发。

    -   然后 Scheduler 可以根据优先级来对任务排序，这样就可以实现高优先级的更新先执行。

-   react 里有 Lane 的优先级机制，基于二进制设计的。它和事件的优先级机制、Scheduler 的优先级机制能够对应上。调度任务的时候先把 Lane 转事件优先级，然后转 Scheduler 的优先级。

-   react18 的 useTransition、useDeferredValue 都是基于并发特性实现的，useTransition 是把回调函数里的更新设置为连续事件的优先级，比离散事件的优先级低。useDeferredValue 则是延后更新 state 的值。
-   这些并发特性的 api 都是通过设置 Lane 实现的，react 检测到对应的 Lane 就会开启带有时间分片的 workLoopConcurrent 循环

```Javascript
// workLoop 同步执行
function renderRootSync(root, lanes) {
    do{
        try {
            workLoopSync();
            break;
        } catch (thrownValue) {
            handleError(root, thrownValue);
        }
    } while (true)
}

function workLoopSync) {
    while (workInProgress !== null) {
        performUnitOfWork(workInProgress);
    }
}

//
function renderRootConcurrent(root, lanes) {
    do{
        try {
            workLoopConcurrent();
            break;
        } catch (thrownValue) {
            handleError(root, thrownValue);
        }
    } while (true)
}

function workLoopConcurrent() {
    // Perform work until Scheduler asks us to yield
    while (workInProgress !== null && shouldYield()) {
        performUnitOfWork(workInProgress);
    }
}

```
