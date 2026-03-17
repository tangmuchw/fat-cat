# React.memo() 和 React.useMemo() 的区别

- memo 是一个高阶组件，默认情况下会对 props 进行浅比较，如果相等不会重新渲染。多数情况下我们比较的都是引用类型，浅比较就会失效，所以我们可以传入第二个参数手动控制。
- useMemo 返回的是一个缓存值，只有依赖发生变化时才会去重新执行作为第一个参数的函数，需要记住的是，useMemo 是在 render 阶段执行的，所以不要在这个函数内部执行与渲染无关的操作，诸如副作用这类的操作属于 useEffect 的适用范畴。

---

- **React.memo**：**缓存组件**，防止组件不必要重渲染
- **useMemo**：**缓存计算结果**，防止重复计算

一个管**组件**，一个管**值/计算**。

---

## 1. React.memo（高阶组件）

### 作用

**缓存整个函数组件**，只有 props 变了才重新渲染。

### 用法

```jsx
import { memo } from "react";

const Child = memo(function Child({ data }) {
    console.log("Child 渲染了");
    return <div>{data}</div>;
});
```

### 原理

- 对组件的 **props 做浅比较**
- props 没变 → 复用上次渲染结果，**不重新执行组件函数**

### 什么时候用

- 组件渲染贵
- 父组件频繁更新，但传给子组件的 props 不变

---

## 2. useMemo（Hook）

### 作用

**缓存一个“计算结果”**，避免每次渲染都重新计算。

### 用法

```jsx
import { useMemo } from 'react';

const expensiveValue = useMemo(() => {
  // 昂贵计算
  return bigList.filter(...).map(...);
}, [dep1, dep2]);
```

### 原理

- 依赖不变 → **直接返回上一次缓存的值**
- 依赖变了 → 重新执行函数，返回新值

### 什么时候用

- 计算非常耗时（过滤、排序、大数据处理）
- 要把这个值传给 memo 组件做 props

---

## 3. 最关键区别（面试必背）

| 特性     | React.memo        | useMemo                       |
| -------- | ----------------- | ----------------------------- |
| 包装对象 | 组件              | 一个值/一段计算               |
| 目的     | 防止组件重复渲染  | 防止重复计算                  |
| 原理     | 浅比较 props      | 比较依赖数组                  |
| 返回     | 缓存后的组件      | 缓存后的值                    |
| 写法     | `memo(Component)` | `useMemo(() => result, deps)` |

---

## 4. 经典配合用法（超级常用）

```jsx
const Child = memo(({ list }) => { ... });

const Parent = () => {
  // 用 useMemo 缓存 list，否则每次都是新引用 → Child 必重渲染
  const list = useMemo(() => data.filter(...), [data]);

  return <Child list={list} />;
};
```

**memo + useMemo 一起用才真正有效**。

---

## 5. 极简总结

- **React.memo**：让组件“记住自己”，props 不变就不跑
- **useMemo**：让计算“记住结果”，依赖不变就不算
- 一个**防组件重渲染**，一个**防重复计算**
