# JSX → React 解析全流程 + Fiber 结构（彻底讲透）

## 一、整体流程（4 步）

你写的 `.jsx` 文件 → React 会按这个流水线处理：

1. **JSX 编译成 `React.createElement()`**（babel 做的）
2. **生成 `Virtual DOM`（虚拟 DOM 对象）**
3. **`Reconciler`（协调器）转成 `Fiber` 树**
4. **Renderer（渲染器）把 Fiber 渲染成真实 DOM**

---

## 二、第一步：JSX 是如何被解析的？

### 你写的 JSX

```jsx
function App() {
    return (
        <div id="root">
            <h1>Hello</h1>
            <p>React</p>
        </div>
    );
}
```

### Babel 会把它编译成：

```js
function App() {
    return React.createElement(
        "div",
        { id: "root" },
        React.createElement("h1", null, "Hello"),
        React.createElement("p", null, "React"),
    );
}
```

#### 关键点：

- **JSX 只是语法糖**
- **真正执行的是 `React.createElement(type, props, ...children)`**
- 这一步和 Fiber 无关，只是生成**虚拟 DOM**

---

## 三、第二步：createElement 做了什么？

它返回一个**JS 对象**，就是 **Virtual DOM（虚拟 DOM）**

结构长这样：

```js
{
  type: 'div',
  props: {
    id: 'root',
    children: [
      { type: 'h1', props: { children: 'Hello' } },
      { type: 'p', props: { children: 'React' } }
    ]
  }
}
```

特点：

- 轻量对象
- 描述界面结构
- **还不是 Fiber**

---

## 四、第三步：虚拟 DOM → Fiber 树（核心！）

## 什么是 Fiber？

Fiber 是：

#### **React 16 重写的核心算法架构**

它的作用：

- **把虚拟 DOM 转成可中断、可恢复、可优先级调度的结构**
- 让渲染不卡主线程（时间切片）

### Fiber 本质：一个 JS 对象

它比 VDOM 多了**链表结构**，用来实现：

- parent（父）
- child（子）
- sibling（兄弟）

### 一个 Fiber 节点包含什么？

```js
{
  // 节点类型
  type: 'div',
  key: null,

  // 指向树结构 ★核心
  return: 父Fiber,
  child: 第一个子Fiber,
  sibling: 下一个兄弟Fiber,

  // 状态与副作用
  memoizedState: hooks链表,
  memoizedProps: {},
  effectTag: 插入/更新/删除,

  // 其他...
}
```

---

## 五、Fiber 树结构（图解）

你写的 JSX：

```jsx
<div>
    <h1></h1>
    <p></p>
</div>
```

### 最终生成的 Fiber 链表结构：

```
div (return: null)
 ↓ child
h1 (return: div, sibling: p)
 ↓ sibling
p (return: div)
```

### 不是普通树！是**链表树**

- 用 **child** 找第一个子节点
- 用 **sibling** 找兄弟节点
- 用 **return** 找父节点

这种结构最大优势：

#### **遍历可以暂停、恢复、插队**

这就是 React “异步渲染”的基础。

---

## 六、第四步：Fiber 如何变成真实 DOM？

### 双缓存机制：

React 有两棵 Fiber 树：

1. **current Fiber 树**（屏幕上正在显示的）
2. **workInProgress 树**（正在内存中构建的）

### 流程：

1. 构建 workInProgress
2. 遍历、更新、标记副作用
3. **commit 阶段一次性更新到 DOM**
4. 替换指针，成为新 current 树

这就是 React 的 **Reconciliation（协调/差分）** 过程。

---

## 七、最精简总结

## JSX 解析流程

1. JSX → babel 编译 → `React.createElement`
2. `createElement` → 返回 **虚拟 DOM 对象**
3. React Reconciler → 把 VDOM 转成 **Fiber 链表树**
4. Commit 阶段 → Fiber 变成 **真实 DOM**

## Fiber 结构特点

- 不是普通树，是**链表**
- 三个核心指针：
    - `child`（子）
    - `sibling`（兄弟）
    - `return`（父）
- 支持**中断、恢复、优先级调度**
- 每个函数组件的 Fiber 上存着 `memoizedState`（Hooks 链表）

---

# 终极一句话总结

### **JSX 是语法糖 → 编译成虚拟 DOM → 转成 Fiber 链表树 → 最终渲染真实 DOM**

---

### 总结

1. **JSX 不直接运行**，会被编译成 `React.createElement`
2. **虚拟 DOM = 描述结构的普通对象**
3. **Fiber = 带链表结构、可中断渲染的进阶版虚拟 DOM**
4. Fiber 靠 **child / sibling / return** 实现遍历
5. Fiber 上的 `memoizedState` 就是 **Hooks 的存储位置**
