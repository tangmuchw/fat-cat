# 08 - 进阶话题

> 涵盖：Suspense / 错误边界 / nextTick / VNode 核心机制 / 扩展点

---

## 一、Suspense（异步组件边界）

### 1.1 问题

异步组件加载是**非阻塞**的：在 async setup 期间，组件树需要显示 loading 态，resolve 后切换回来。

### 1.2 实现原理

```javascript
// packages/runtime-core/src/components/Suspense.ts

const Suspense = {
  name: 'Suspense',
  props: ['timeout'],
  setup(props, { slots }) {
    // pendingVNodes：异步加载中的子 vnode
    // fallbackVNode：loading 态的 vnode
    const state = reactive({
      pending: new Map(),    // vnode → Promise
      fallback: slots.fallback?.(),
      default: slots.default?.()
    })

    let sync = true

    function resolve() {
      // 异步加载完成，切换到 default
      state.default = slots.default?.()
    }

    return () => {
      // 渲染 default slot（可能包含异步组件）
      if (state.default) {
        return state.default
      }
      // 未 resolve 前渲染 fallback
      return state.fallback
    }
  }
}
```

### 1.3 onResolve 钩子

```javascript
// 异步组件 resolve 后触发
onResolve(() => {
  // 可以做性能统计等
})
```

---

## 二、错误边界（ErrorBoundary）

### 2.1 组件渲染错误处理

```javascript
// packages/runtime-core/src/components/ErrorBoundary.ts

const ErrorBoundary = {
  name: 'ErrorBoundary',
  props: ['onError'],
  setup(props, { slots }) {
    let error = null

    return () => {
      if (error) {
        // 有错误 → 渲染 error slot
        return slots.error?.({ error })
      }
      // 无错误 → 正常渲染
      return slots.default?.()
    }
  },

  errorCaptured(err, instance, info) {
    error = err
    props.onError?.(err, instance, info)
  }
}
```

### 2.2 全局错误处理

```javascript
// app.config.errorHandler
const app = createApp(App)
app.config.errorHandler = (err, instance, info) => {
  console.error('全局错误:', err, info)
  // 上报错误
}
```

---

## 三、nextTick

### 3.1 为什么需要 nextTick

Vue 的响应式更新是**异步批量**的。修改数据后，DOM 不是立即更新：

```javascript
msg = 'new'
console.log(el.textContent)  // 还是旧值！

nextTick(() => {
  console.log(el.textContent)  // 已更新
})
```

### 3.2 实现

```javascript
// packages/runtime-core/src/scheduler.ts

let isFlushing = false
let flushPromise

function nextTick(fn) {
  return fn
    ? flushPromise.then(fn)  // 返回 Promise，支持 await
    : flushPromise
}

function queueJob(job) {
  if (!queue.includes(job)) {
    queue.push(job)
    if (!isFlushing) {
      isFlushing = true
      flushPromise = Promise.resolve().then(flushJobs)
    }
  }
}

function flushJobs() {
  let job
  while ((job = queue.shift())) {
    job()  // 执行 effect 的 scheduler
  }
  isFlushing = false
}
```

---

## 四、VNode 核心机制

### 4.1 VNode 结构

```javascript
// packages/runtime-core/src/vnode.ts

function createVNode(type, props, children, ...) {
  return {
    type,
    props,
    children,
    el: null,           // 指向真实 DOM，挂载后填充
    key: props?.key,
    ref: props?.ref,
    shapeFlag,         // 位掩码：ELEMENT | COMPONENT | TEXT | etc.
    patchFlag,
    dynamicProps,
    dirs,              // 指令
    targetArch,       // KeepAlive 标记
    // ...
  }
}

// shapeFlag 位运算
const ShapeFlags = {
  ELEMENT: 1,         // 普通 HTML/SVG 元素
  COMPONENT: 1 << 1,  // 组件
  TEXT: 1 << 2,       // 文本节点
  FRAGMENT: 1 << 3,   // Fragment
  TELEPORT: 1 << 4,
  SUSPENSE: 1 << 5,
  // ...
}
```

### 4.2 h() 助手

```javascript
// h('div', 'text')              → 文本子节点
// h('div', {}, ['child'])        → 多个子节点
// h('div', { class: 'a' }, h('span'))  → 带 props 和子 vnode
// h(Component, { msg: 'hi' })     → 组件 vnode
```

---

## 五、扩展点

### 5.1 自定义指令（vCustom）

```javascript
const vFocus = {
  mounted(el) { el.focus() }
}

// vnode.dirs = [{ dir: vFocus, value: undefined }]
// 渲染器在 mount 时调用 dir.mounted(el, vnode)
```

### 5.2 renderTracked / renderTriggered

```javascript
export default {
  renderTracked({ key, target, type }) {
    console.log('读取:', key, target, type)
  },
  renderTriggered({ key, target, type }) {
    console.log('修改:', key, target, type)
  }
}
```

### 5.3 自定义渲染器

```javascript
// 替换运行时 DOM API，换成 Canvas / PDF / etc.
const customRenderer = createRenderer({
  createElement(type) {
    if (type === 'canvas') return document.createElement('canvas')
  },
  patchProp(el, key, prev, next) {
    if (key === 'width') el.width = next
  }
})

// 使用自定义渲染器
customRenderer.render(h('canvas', { width: 100 }), container)
```

---

## 六、响应式系统的局限性

| 场景 | 局限 | 解决方案 |
|---|---|---|
| **解构丢失响应式** | `const { a } = reactive(obj)` | 用 `toRef` / `toRefs` |
| **新增属性** | `obj.newKey = 'val'` 不会响应 | `reactive(obj.newKey = 'val')` 或用 `ref` |
| **替换整个对象** | `obj = newObj` 失去联系 | `Object.assign(target, newObj)` |
| **Set/Map** | 不能被 Proxy 代理 | 用 `reactive(new Set())` 但有限制 |
| **普通值** | 原始值无法被代理 | 用 `ref` 包装 |
