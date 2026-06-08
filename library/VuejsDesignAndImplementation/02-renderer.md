# 02 - 渲染器（Renderer）

> 源码：`packages/runtime-core/src/renderer.ts`、`packages/runtime-dom/src/nodeOps.ts`

---

## 一、渲染器的本质

渲染器的核心职责：**把虚拟 DOM（vnode）变成真实 DOM，并处理更新**。

它的关键设计是**平台无关**：所有 DOM 操作都抽象到 `nodeOps`，同一个渲染器在 Node.js 里是 SSR，在浏览器里是 DOM：

```
vnode → renderer
          ↓
    ┌─────────────┐
    │ nodeOps     │  ← 只换这一个模块，就换了一个平台
    │ createElement│
    │ appendChild │
    │ remove      │
    │ setElementText│
    └─────────────┘
```

---

## 二、核心数据结构

```javascript
// renderer.ts 核心是三个函数的创建：
const renderer = createRenderer(nodeOps)

function createRenderer(options) {
  const {
    createElement,      // 创建 DOM 元素
    appendChild,       // 插入 DOM
    remove,            // 删除 DOM
    patchProps,        // 更新属性/事件
    ...                // 更多平台操作
  } = options

  // 三个核心函数
  const mount = (vnode, container) => { /* ... */ }
  const patch = (prev, next) => { /* ... */ }
  const unmount = (vnode) => { /* ... */ }

  return { render, hydrate }
}
```

---

## 三、挂载（mount）

### 3.1 mountElement

```javascript
function mountElement(vnode, container) {
    const el = createElement(vnode.type); // 创建真实 DOM

    // 处理 children
    if (typeof vnode.children === "string") {
        setElementText(el, vnode.children); // 文本子节点
    } else if (Array.isArray(vnode.children)) {
        vnode.children.forEach((child) => {
            patch(null, child, el); // 递归挂载子节点
        });
    }

    // 处理 props（attrs + events）
    if (vnode.props) {
        for (const key in vnode.props) {
            patchProps(el, key, null, vnode.props[key]);
        }
    }

    appendChild(container, el); // 插入容器
    return el;
}
```

### 3.2 vnode 结构

```javascript
// 组件 vnode
{ type: 'div', props: { class: 'container' }, children: [...] }
{ type: Component, props: { msg: 'hello' }, children: [...] }

// HTML vnode
{ type: 'div', class: 'container', children: 'text' }
```

---

## 四、更新（patch）

patch 是渲染器最复杂的部分——**决定是复用已有 DOM 还是重建**。

### 4.1 patch 流程

```javascript
function patch(prev, next, container) {
    // 1. 类型不同 → 卸载旧的，挂载新的
    if (prev.type !== next.type) {
        unmount(prev);
        prev = null;
    }

    const { type } = next;

    // 2. 组件 patch
    if (typeof type === "object") {
        patchComponent(prev, next, container);
    }
    // 3. 文本节点
    else if (type === Text) {
        patchText(prev, next);
    }
    // 4. Fragment
    else if (type === Fragment) {
        patchChildren(prev, next, container);
    }
    // 5. 普通 HTML/SVG 元素
    else if (isString(type)) {
        patchElement(prev, next, container);
    }
}
```

### 4.2 patchElement（最常见）

```javascript
function patchElement(prev, next, container) {
    const el = prev.el; // 复用已有 DOM

    // 1. 更新 props
    patchProps(el, prev.props, next.props);

    // 2. 更新 children
    patchChildren(prev.children, next.children, el);
}

function patchChildren(prevChildren, nextChildren, el) {
    // 三种情况：string / array / null
    // 调用对应的 diff 算法（见 04-diff.md）
    // 最简单的情况：全是文本，直接 setElementText
}
```

---

## 五、卸载（unmount）

```javascript
function unmount(vnode) {
    const { type, props, children } = vnode;

    if (typeof type === "object") {
        // 组件：调用组件的 unmounted 钩子
        unmountComponent(vnode.component);
    } else if (type === Fragment) {
        // Fragment：递归卸载子节点
        vnode.children.forEach((child) => unmount(child));
    } else {
        // 普通元素
        remove(vnode.el);
    }

    // 触发 DOM removal 观察者（Transition/KeepAlive 用）
    vnode.props?.onVnodeMounted?.(vnode);
}
```

---

## 六、Props 处理（patchProps）

### 6.1 三种属性处理

```javascript
// packages/runtime-dom/src/modules/attrs.ts

function patchAttr(el, key, prev, next) {
  if (next == null) {
    removeAttribute(el, key)   // 删除属性
  } else {
    setAttribute(el, key, next) // 设置属性
  }
}

// packages/runtime-dom/src/modules/events.ts

function patchEvent(el, key, prev, next) {
  // 1. 获取缓存的事件处理函数
  const invoker = el._vei || (el._vei = {})
  let handler = invoker[key]

  if (next) {
    if (!handler) {
      // 首次绑定：创建 invoker 并缓存
      handler = invoker[key] = (e) => handler(e)
      el.addEventListener(key.slice(2).toLowerCase(), handler)
    } else {
      // 更新：替换 invoker 中的函数引用
      invoker[key] = handler = (e) => handler(e)
    }
  } else {
    // 移除
    el.removeEventListener(..., handler)
    invoker[key] = null
  }
}

// packages/runtime-dom/src/modules/style.ts

function patchStyle(prev, next) {
  if (next == null) {
    removeAttribute(el, 'style')
  } else {
    for (const key in next) {
      el.style[key] = next[key]      // 赋新值
    }
    for (const key in prev) {
      if (next[key] == null) {
        el.style[key] = ''            // 删除旧值
      }
    }
  }
}
```

### 6.2 class 处理（支持多种写法）

```javascript
// 字符串：class="container"
// 对象：class={{ active: true, 'text-sm': false }}
// 数组：class={['a', { b: true }]}
// 全部规范化为字符串后设置

function patchClass(el, prev, next) {
    if (next == null || next === "") {
        el.removeAttribute("class");
        return;
    }
    el.className = normalizeClass(next);
}
```

### 6.3 事件处理缓存

```javascript
// el._vei = { click: invokerFn, input: invokerFn }
// 缓存 invoker 是为了：事件更新时不用 add/remove，而是直接替换 invoker 中的函数
// 节省 addEventListener 调用，且能精确控制"移除的是哪个函数"
```

---

## 七、运行时平台抽象

```javascript
// packages/runtime-dom/src/nodeOps.ts

export const nodeOps = {
    createElement(tag) {
        return document.createElement(tag);
    },
    createElementNS(ns, tag) {
        return document.createElementNS(ns, tag);
    },
    createText(text) {
        return document.createTextNode(text);
    },
    appendChild(child, parent) {
        parent.appendChild(child);
    },
    remove(child) {
        child.parentNode.removeChild(child);
    },
    insertBefore(child, ref, parent) {
        parent.insertBefore(child, ref);
    },
    setElementText(el, text) {
        el.textContent = text;
    },
    parentNode(node) {
        return node.parentNode;
    },
    nextSibling(node) {
        return node.nextSibling;
    },
    tagName(elm) {
        return elm.tagName;
    },
};
```

换平台（如 Wechat Mini Program）只需替换 `nodeOps`。

---

## 八、渲染器的批量更新

响应式数据变化 → trigger → effect → render → patch → DOM 更新

**不需要同步执行所有更新**，Vue 3 用队列批量处理：

```javascript
// scheduler 调度
scheduler: () => {
    queueJob(renderEffect);
};

// 队列去重：同一个 effect 在队列中只出现一次
// 微任务执行：所有同步更新完成后，在微任务中批量执行队列中的 job
```

---

## 九、跨平台扩展

```
createRenderer(nodeOps)

nodeOps = 浏览器    → DOM 渲染器
nodeOps = JSDOM     → 服务端渲染（读取 DOM 结构）
nodeOps = WXML      → 微信小程序
nodeOps = UNIAPP    → App 跨端
```

关键：渲染器本身不包含任何 DOM 逻辑，只包含**对 nodeOps 的调用**。
