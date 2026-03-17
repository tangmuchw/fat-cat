[toc]

# hooks

## hooks 优点

- 简洁：React Hooks 解决了 HOC 和 Render Props 的嵌套问题,更加简洁
- 解耦: React Hooks 可以更方便地把 UI 和状态分离,做到更彻底的解耦
- 组合: Hooks 中可以引用另外的 Hooks 形成新的 Hooks,组合变化万千
- 函数友好: React Hooks 为函数组件而生，从而解决了类组件的几大问题

## hooks 缺点

- 额外的学习成本
- 写法上有限制（不能出现在条件、循环中），并且写法限制增加了重构成本
- 破坏了 PureComponent、React.memo 浅比较的性能优化效果（为了取最新的 props 和 state，每次 render()都要重新创建事件处函数）
- 在闭包场景可能会引用到旧的 state、props 值
- React.memo 并不能完全替代 shouldComponentUpdate（因为拿不到 state change，只针对 props change）

### useCallback

> useCallback 是一个允许你在多次渲染中缓存函数的 React Hook

- 跳过组件的重新渲染
- 从记忆化回调中更新 state
- 防止频繁触发 Effect
- 优化自定义 Hook

### useContext

> useContext 是一个 React Hook，可以让你读取和订阅组件中的 context（上下文）

- 向组件树深层传递数据
- 通过 context 更新传递的数据
- 指定后备方案默认值
- 覆盖组件树一部分的 context
- 在传递对象和函数时优化重新渲染

### useDeferredValue

> useDeferredValue 是一个 React Hook，可以让你延迟更新 UI 的某些部分

- 在新内容加载期间显示旧内容。
- 表明内容已过时
- 延迟渲染 UI 的某些部分

### useEffect

> useEffect 是一个 React Hook，它允许你 将组件与外部系统同步

- 连接到外部系统
- 在自定义 Hook 中封装 Effect
- 控制非 React 小部件
- 使用 Effect 请求数据
- 指定响应式依赖项
- 在 Effect 中根据先前 state 更新 state
- 删除不必要的对象依赖项
- 删除不必要的函数依赖项
- 从 Effect 读取最新的 props 和 state
- 在服务器和客户端上显示不同的内容

### useImperativeHandle

> useImperativeHandle 是 React 中的一个 Hook，它能让你自定义由 ref 暴露出来的句柄

- 向父组件暴露一个自定义的 ref 句柄
- 暴露你自己的命令式方法

```Javascript
useImperativeHandle(ref, createHandle, dependencies?)
```

### useMemo

> useMemo 是一个 React Hook，它在每次重新渲染的时候能够缓存计算的结果

- 跳过代价昂贵的重新计算
- 跳过组件的重新渲染
- 记忆另一个 Hook 的依赖
- 记忆一个函数

### useReducer

> useReducer 是一个 React Hook，它允许你向组件里面添加一个 reducer。

- 向组件添加 reducer
- 实现 reducer 函数
- 避免重新创建初始值

### useRef

> useRef 是一个 React Hook，它能帮助引用一个不需要渲染的值

- 使用用 ref 引用一个值
- 通过 ref 操作 DOM
- 避免重复创建 ref 的内容

### useState

> useState 是一个 React Hook，它允许你向组件添加一个 状态变量

- 为组件添加状态
- 根据先前的 state 更新 state
- 更新状态中的对象和数组
- 避免重复创建初始状态
- 使用 key 重置状态
- 存储前一次渲染的信息

### useTransition

> useTransition 是一个帮助你在不阻塞 UI 的情况下更新状态的 React Hook

### React Hooks 原理深度解析（通俗易懂版）

React Hooks（如 `useState`、`useEffect`）的核心原理，本质是**React 利用函数组件的 Fiber 节点，通过链表结构存储 Hook 状态，严格按调用顺序匹配，实现状态的持久化与复用**。

我会用**极简原理 + 核心机制 + 伪代码实现**帮你彻底吃透，不绕弯子。

---

## 一、先搞懂核心前提

1. **函数组件本身无状态**：普通函数执行完就销毁，变量会被回收，无法保存状态；
2. **Hooks 把状态存在「组件外部」**：状态不放在函数里，而是存在 React 管理的 **Fiber 节点**（组件在 React 内部的真实对象）上；
3. **必须按顺序调用**：Hooks 不能写在 `if/for/函数嵌套` 里，因为 React 靠**调用顺序**匹配状态。

---

## 二、Hooks 核心原理（3 大关键点）

### 1. 状态存储：用「链表」存所有 Hook

React 为每个函数组件创建一个 **Fiber 节点**，节点上有个专门属性：`memoizedState`。
这个属性是一个**单向链表**，每个节点对应一个 Hook：

```js
// 伪代码：组件的 Fiber 节点结构
fiberNode = {
    memoizedState: {
        hook: {
            state: 0, // 第一个 Hook：useState(0) 的值
            next: {
                hook: {
                    state: false, // 第二个 Hook：useState(false) 的值
                    next: null, // 链表结尾
                },
            },
        },
    },
};
```

- 每调用一个 Hook，就往链表追加一个节点；
- 组件更新时，React 遍历这个链表，还原所有状态。

### 2. 状态匹配：严格依赖「调用顺序」

这是 Hooks 最重要的规则：**不能在条件/循环中使用 Hooks**。
因为 React 不看 Hook 名称，只看**调用顺序**：

```js
// 正确：顺序固定
function App() {
    const [num, setNum] = useState(0); // 顺序 1
    const [flag, setFlag] = useState(false); // 顺序 2
}

// 错误：顺序会变，React 匹配失败
function App() {
    if (flag) {
        const [num, setNum] = useState(0); // 有时执行，有时不执行
    }
    const [flag, setFlag] = useState(false);
}
```

### 3. 状态更新：替换链表节点 + 触发重渲染

- 调用 `setState` 时，React 找到对应链表节点，**直接修改 state 值**；
- 状态修改后，触发组件**重新渲染**；
- 重渲染时，按**相同顺序**重新执行 Hooks，从链表中取出最新状态。

---

## 三、极简伪代码：手写一个 useState（看懂就懂原理）

这是 React 官方 `useState` 的**核心简化版**，10 行代码看懂本质：

```js
// 全局变量：记录当前组件、当前 Hook 位置
let currentComponentFiber;
let hookIndex;

function useState(initialState) {
    // 1. 拿到当前组件的 Hook 链表
    const hooks = currentComponentFiber.memoizedState;
    // 2. 按 调用顺序 取对应 Hook
    const currentHook = hooks[hookIndex];

    // 3. 首次渲染：初始化 Hook，存入状态
    if (!currentHook) {
        hooks[hookIndex] = {
            state: initialState, // 存初始值
        };
    }

    // 4. 定义更新函数：修改状态 + 触发重渲染
    const setState = (newState) => {
        hooks[hookIndex].state = newState; // 更新链表中的状态
        renderComponent(); // 触发组件重新渲染
    };

    // 5. 索引+1，匹配下一个 Hook，返回当前状态
    hookIndex++;
    return [hooks[hookIndex - 1].state, setState];
}

// 组件渲染时：重置索引，按顺序执行 Hooks
function renderComponent() {
    hookIndex = 0; // 关键！每次渲染都从 0 开始
    componentFunction(); // 执行函数组件，调用所有 Hooks
}
```

### 伪代码总结

1. **首次渲染**：创建 Hook 链表，存储所有状态；
2. **更新渲染**：重置索引，按顺序读取链表中的状态；
3. **修改状态**：直接改链表值，触发重渲染，重新读取。

---

## 四、其他 Hooks 原理（通用）

所有 Hooks 底层逻辑完全一致，只是功能不同：

- `useEffect`：存储「依赖数组 + 回调函数」，对比依赖是否变化，决定是否执行；
- `useRef`：存储一个 `{ current: xxx }` 对象，永久不变；
- `useMemo`：存储「计算结果 + 依赖」，依赖不变则直接返回缓存结果；
- `useCallback`：缓存函数，本质和 `useMemo` 一样。

---

## 五、一句话终极总结

**React Hooks 就是：用 Fiber 节点的链表存储状态，靠固定调用顺序匹配 Hook，重渲染时按顺序读取状态，实现函数组件的状态持久化与副作用管理。**

---

### 总结

1. **状态位置**：Hooks 状态存在**组件 Fiber 节点**，不在函数内部；
2. **存储结构**：**单向链表**，一个 Hook 对应一个节点；
3. **核心规则**：**调用顺序绝对固定**（不能用在条件/循环里）；
4. **更新机制**：修改链表状态 → 触发重渲染 → 按顺序读取最新状态。
