# hooks

## hooks 优点

-   简洁：React Hooks 解决了 HOC 和 Render Props 的嵌套问题,更加简洁
-   解耦: React Hooks 可以更方便地把 UI 和状态分离,做到更彻底的解耦
-   组合: Hooks 中可以引用另外的 Hooks 形成新的 Hooks,组合变化万千
-   函数友好: React Hooks 为函数组件而生，从而解决了类组件的几大问题

## hooks 缺点

-   额外的学习成本
-   写法上有限制（不能出现在条件、循环中），并且写法限制增加了重构成本
-   破坏了 PureComponent、React.memo 浅比较的性能优化效果（为了取最新的 props 和 state，每次 render()都要重新创建事件处函数）
-   在闭包场景可能会引用到旧的 state、props 值
-   React.memo 并不能完全替代 shouldComponentUpdate（因为拿不到 state change，只针对 props change）

### useCallback

> useCallback 是一个允许你在多次渲染中缓存函数的 React Hook

-   跳过组件的重新渲染
-   从记忆化回调中更新 state
-   防止频繁触发 Effect
-   优化自定义 Hook

### useContext

> useContext 是一个 React Hook，可以让你读取和订阅组件中的 context（上下文）

-   向组件树深层传递数据
-   通过 context 更新传递的数据
-   指定后备方案默认值
-   覆盖组件树一部分的 context
-   在传递对象和函数时优化重新渲染

### useDeferredValue

> useDeferredValue 是一个 React Hook，可以让你延迟更新 UI 的某些部分

-   在新内容加载期间显示旧内容。
-   表明内容已过时
-   延迟渲染 UI 的某些部分

### useEffect

> useEffect 是一个 React Hook，它允许你 将组件与外部系统同步

-   连接到外部系统
-   在自定义 Hook 中封装 Effect
-   控制非 React 小部件
-   使用 Effect 请求数据
-   指定响应式依赖项
-   在 Effect 中根据先前 state 更新 state
-   删除不必要的对象依赖项
-   删除不必要的函数依赖项
-   从 Effect 读取最新的 props 和 state
-   在服务器和客户端上显示不同的内容

### useImperativeHandle

> useImperativeHandle 是 React 中的一个 Hook，它能让你自定义由 ref 暴露出来的句柄

-   向父组件暴露一个自定义的 ref 句柄
-   暴露你自己的命令式方法

```Javascript
useImperativeHandle(ref, createHandle, dependencies?)
```

### useMemo

> useMemo 是一个 React Hook，它在每次重新渲染的时候能够缓存计算的结果

-   跳过代价昂贵的重新计算
-   跳过组件的重新渲染
-   记忆另一个 Hook 的依赖
-   记忆一个函数

### useReducer

> useReducer 是一个 React Hook，它允许你向组件里面添加一个 reducer。

-   向组件添加 reducer
-   实现 reducer 函数
-   避免重新创建初始值

### useRef

> useRef 是一个 React Hook，它能帮助引用一个不需要渲染的值

-   使用用 ref 引用一个值
-   通过 ref 操作 DOM
-   避免重复创建 ref 的内容

### useState

> useState 是一个 React Hook，它允许你向组件添加一个 状态变量

-   为组件添加状态
-   根据先前的 state 更新 state
-   更新状态中的对象和数组
-   避免重复创建初始状态
-   使用 key 重置状态
-   存储前一次渲染的信息

### useTransition

> useTransition 是一个帮助你在不阻塞 UI 的情况下更新状态的 React Hook
