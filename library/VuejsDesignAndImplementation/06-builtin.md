# 06 - 内建组件

> 源码：`packages/runtime-core/src/components/`

---

## 一、KeepAlive

### 1.1 核心问题

组件切换时默认会**卸载（unmount）再挂载（mount）**，DOM 销毁再重建，状态丢失：

```
<A /> → <B />
  ↓
A unmounted（DOM 销毁）
B mounted（DOM 重建）
```

KeepAlive 的目标是：**切换时缓存组件实例，不销毁 DOM，再次进入时直接激活**。

### 1.2 实现原理

```javascript
// packages/runtime-core/src/components/KeepAlive.ts

const KeepAlive = {
  name: 'KeepAlive',
  __isKeepAlive: true,  // 标记（渲染器识别用）

  props: {
    include: [String, RegExp, Array],
    exclude: [String, RegExp, Array],
    max: [Number]
  },

  setup(props, { slots }) {
    const cache = new Map()     // key → vnode（缓存的组件实例）
    const keys = new Set()      // 记录缓存顺序（用于 max 限制）

    let current = null          // 当前激活的 vnode

    return () => {
      // slots.default() 返回的是组件 vnode
      const vnode = slots.default()

      if (!isObject(vnode.type)) return vnode  // 非组件跳过

      const key = vnode.key || vnode.type
      const { include, exclude, max } = props

      // 1. 匹配 include/exclude
      if (include && !matchName(vnode.type, include)) return vnode
      if (exclude && matchName(vnode.type, exclude)) return vnode

      // 2. 已在缓存中 → 激活（复用 DOM，不重新创建）
      if (cache.has(key)) {
        const cachedVnode = cache.get(key)
        cachedVnode.component.targetArch = 'keep-alive'
        keys.delete(key)
        keys.add(key)
        return cachedVnode
      }

      // 3. 不在缓存 → 挂载
      const subTree = renderComponent(vnode)

      // 4. 缓存新组件
      if (max && keys.size >= max) {
        // LRU：删除最老的
        const oldest = keys.values().next().value
        cache.delete(oldest)
        keys.delete(oldest)
      }
      cache.set(key, subTree)
      keys.add(key)

      return subTree
    }
  }
}
```

### 1.3 激活与失活（activate / deactivate）

真正切换时，组件不是 unmount，而是"失活"：

```javascript
// 在渲染器的 unmount 中，检测到 __isKeepAlive 时调用 deactivate
function unmount(vnode) {
  if (vnode.type.__isKeepAlive) {
    // 不销毁 DOM，只是失活
    const instance = vnode.component
    instance.targetArch = 'keep-alive'
    // 触发 onDeactivated 钩子
    instance.deactivated?.()
  } else {
    // 普通组件走正常 unmount
    doUnmount(vnode)
  }
}
```

激活时**复用已有 DOM 节点**：

```javascript
// 在 patch 中检测到来自 KeepAlive 缓存的组件时：
function patchComponent(prev, next) {
  if (next.targetArch === 'keep-alive') {
    // 复用 prev 的 DOM
    next.el = prev.el
    next.component = prev.component
    // 触发 onActivated 钩子
    next.component.activated?.()
  } else {
    // 正常 patch
    doPatchComponent(prev, next)
  }
}
```

### 1.4 LRU 缓存策略

```javascript
// max 属性限制最大缓存数量
// 每次激活（cache.get）时，把 key 移到 keys 末尾（最新）
// 超过 max 时，删除 keys 的第一个元素（最老）
if (max && keys.size >= max) {
  const oldest = keys.values().next().value
  cache.delete(oldest)
  keys.delete(oldest)
}
```

---

## 二、Teleport

### 2.1 核心问题

组件的 DOM 默认挂载在父组件容器下，但有时需要**挂载到任意 DOM 节点**：

```html
<Portal to="#modal-root">
  <Modal />
</Portal>
```

Modal 的 DOM 应该直接出现在 `document.body#modal-root`，而非父组件的容器里。

### 2.2 实现

```javascript
// packages/runtime-core/src/components/Teleport.ts

const Teleport = {
  name: 'Teleport',
  process(prev, next, container, ...) {
    const target = document.querySelector(next.props.to)  // 目标容器
    if (!target) return

    if (prev) {
      // 移动已有子节点到目标
      moveChildren(prev.children, target)
    } else {
      // 挂载新子节点到目标
      mountChildren(next.children, target)
    }

    // 记录挂载目标（用于后续更新）
    next.target = target
  },

  patch(prev, next, container) {
    // .children 整体移动到新的 to 目标
    const newTarget = document.querySelector(next.props.to)
    if (prev.props.to !== next.props.to) {
      moveChildren(prev.children, newTarget)
    }
    // patch 子节点
    patchChildren(prev.children, next.children, newTarget)
  }
}
```

### 2.3 关键点

Teleport 的 children **不受父容器约束**，直接挂载到 `to` 指定的目标节点。

SSR 时需要特殊处理：Teleport 的子节点要拼到 HTML 字符串的对应位置。

---

## 三、Transition

### 3.1 原理

DOM 节点的进入/离开通过**动态添加/移除 CSS 类名**实现过渡效果：

```css
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s }
.fade-enter-from, .fade-leave-to { opacity: 0 }
.fade-enter-to, .fade-leave-from { opacity: 1 }
```

### 3.2 实现

```javascript
// packages/runtime-core/src/components/Transition.ts

const Transition = {
  name: 'Transition',
  __isTeleport: true,

  setup(props, { slots }) {
    return () => {
      const vnode = slots.default()

      // 为子节点 vnode 附加 Transition hooks
      if (vnode.component) {
        vnode.component.transition = {
          beforeEnter(el) {
            el.classList.add(`${prefix}-enter-from`)
            el.classList.remove(`${prefix}-enter-to`)
          },
          enter(el) {
            requestAnimationFrame(() => {
              el.classList.add(`${prefix}-enter-active`)
              el.classList.remove(`${prefix}-enter-from`)
              // 下一帧去除 enter-to（触发 CSS transition）
              requestAnimationFrame(() => {
                el.classList.add(`${prefix}-enter-to`)
              })
            })
          },
          leave(el) {
            el.classList.add(`${prefix}-leave-from`)
            requestAnimationFrame(() => {
              el.classList.add(`${prefix}-leave-active`)
              el.classList.remove(`${prefix}-leave-from`)
              requestAnimationFrame(() => {
                el.classList.add(`${prefix}-leave-to`)
              })
            })
          }
        }
      }

      return vnode
    }
  }
}
```

### 3.3 钩子触发时机

```javascript
// 渲染器在 mount/unmount 时检测 transition hooks
function mountElement(vnode, container) {
  const el = vnode.el
  vnode.component?.transition?.beforeEnter?.(el)
  // ...
  vnode.component?.transition?.enter?.(el)
}

function unmount(vnode) {
  const el = vnode.el
  vnode.component?.transition?.leave?.(el, () => {
    // 离开动画完成后，真正移除 DOM
    remove(el)
  })
}
```

---

## 四、Fragment

### 4.1 问题

组件返回多个根节点时，单个 vnode 无法表达：

```javascript
// 组件返回两个根节点
return [h('td'), h('td')]  // 不合法
```

### 4.2 解决方案

```javascript
// Fragment vnode：type = Fragment
{ type: Fragment, children: [h('td'), h('td')] }
```

渲染器识别 Fragment：

```javascript
function patch(prev, next, container) {
  if (next.type === Fragment) {
    // Fragment 的 children 直接挂载到 container
    next.children.forEach(child => patch(null, child, container))
    return
  }
}
```
