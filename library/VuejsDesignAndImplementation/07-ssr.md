# 07 - 同构渲染（SSR + Hydration）

> 源码：`packages/server/`、`packages/runtime-core/src/hydration.ts`

---

## 一、三种渲染模式对比

| | CSR | SSR | 同构（SSR + Hydration） |
|---|---|---|---|
| 首屏速度 | 慢（等 JS 下载 + 执行） | 快（直出 HTML） | 快 |
| SEO | 差 | 好 | 好 |
| 交互性 | 好 | 差（无响应式） | 好 |
| TTID | 慢 | 快 | 快 |

---

## 二、SSR 工作流程

```
组件定义
    ↓
renderComponentTree()  → vnode 树
    ↓
┌─────────────────────────────┐
│    SSR 渲染器（字符串拼接）     │
│  vnode → HTML 字符串          │
│  (packages/server/renderer.ts)│
└────────────┬────────────────┘
             ↓
┌─────────────────────────────┐
│       HTML + 水合标记         │
│  <div data-v-app>...HTML...</div>
│  + hydration markers        │
└────────────┬────────────────┘
             ↓
浏览器收到 HTML，直出内容（用户可见）
             ↓
             ↓
┌─────────────────────────────┐
│    客户端 Hydration（水合）    │
│  遍历 DOM，建立 vnode 映射    │
│  绑定事件，激活响应式          │
└────────────┬────────────────┘
             ↓
             ↓
     Vue 3 接管，后续更新走 CSR
```

---

## 三、SSR 渲染器

SSR 和 DOM 渲染器使用同一个 vnode 结构，只是**渲染方式不同**：

```javascript
// packages/server/renderer.ts

const serverRenderer = {
  renderComponentTree(vnode, context) {
    // 递归处理 vnode，返回 HTML 字符串
    switch (vnode.type) {
      case 'Element':
        return renderElement(vnode)      // <tag>children</tag>
      case 'Text':
        return vnode.content            // 纯文本
      case 'Interpolation':
        return resolveString(vnode)     // {{ msg }} → 数据
      case Fragment:
        return vnode.children.map(renderComponentTree).join('')
      default:
        // 组件：执行组件 render
        const result = vnode.type.render(vnode)
        return renderComponentTree(result, context)
    }
  }
}
```

### 3.1 字符串拼接 vs vnode

```javascript
// CSR：创建 vnode
const vnode = h('div', { class: 'container' }, 'hello')
patch(prev, vnode)  // 创建 DOM

// SSR：直接生成 HTML 字符串
const html = `<div class="container">hello</div>`
```

### 3.2 服务端数据获取（onServerPrefetch）

```javascript
// 用户代码
export default {
  async serverPrefetch() {
    this.data = await fetch('/api/data')
  },
  data() { return { data: null } },
  render() { return h('div', this.data) }
}

// SSR 时：在 render 之前等待 serverPrefetch 完成
async function renderComponent(vnode) {
  const instance = createComponentInstance(vnode)
  if (instance.type.serverPrefetch) {
    await instance.type.serverPrefetch.call(instance.proxy)
  }
  return renderComponentTree(instance)
}
```

---

## 四、客户端 Hydration（水合）

### 4.1 核心问题

服务器返回的 HTML 是**纯静态字符串**，没有响应式、没有事件绑定。Hydration 就是"把 Vue 3 的响应式能力嫁接到已有 DOM 上"。

### 4.2 流程

```javascript
// packages/runtime-core/src/hydration.ts

function hydrate(node, vnode) {
  const { type, props, children } = vnode

  // 1. 建立 DOM → vnode 映射（通过 hydration marker）
  // 服务器在 HTML 中插入了 data-v-hydrate 标记

  // 2. 绑定事件
  if (props.onClick) {
    node.addEventListener('click', props.onClick)
  }

  // 3. 递归水合子节点
  if (Array.isArray(children)) {
    hydrateChildren(node.childNodes, children)
  }

  // 4. 激活组件的响应式
  if (typeof type === 'object') {
    hydrateComponent(node, vnode)
  }
}

function mountApp(rootComponent) {
  const container = document.querySelector('#app')
  const vnode = createVNode(rootComponent)

  // SSR 场景：hydrate
  if (container.hasAttribute('data-v-hydrate')) {
    hydrate(vnode, container)
  }
  // CSR 场景：正常 mount
  else {
    render(vnode, container)
  }
}
```

### 4.3 Hydration Marker

服务器在 HTML 中插入标记，客户端用来对齐 vnode：

```html
<!-- 服务端输出的 HTML -->
<div data-v-abc123>
  <span data-v-abc123>hello</span>
</div>

<!-- 客户端知道 span 对应哪个 vnode -->
```

### 4.4 SSR 与 CSR 的差异处理

```javascript
// 客户端可能和服务端渲染结果不同（如时间戳）
// Hydration 会"修复"这些差异

// 组件的 updated 钩子会触发：
// 1. 服务端 render 的时间戳是旧的
// 2. 客户端 hydration 时，effect 重新执行
// 3. 时间戳更新为新的客户端时间
```

---

## 五、async component（异步组件）

### 5.1 问题

大型应用不希望首屏加载所有组件，需要**按需加载**。

### 5.2 实现

```javascript
// 用户代码
const AsyncComp = defineAsyncComponent(() => import('./Foo.vue'))

// 编译后生成一个包装组件
const AsyncComp = {
  setup() {
    const resolved = ref(null)
    const error = ref(null)
    const loading = ref(false)

    // 异步加载
    import('./Foo.vue')
      .then(m => { resolved.value = m.default })
      .catch(e => { error.value = e })

    return () => {
      if (loading.value) return h('div', 'loading...')
      if (error.value) return h('div', 'error')
      if (resolved.value) return h(resolved.value)
      return null
    }
  }
}
```

### 5.3 async 组件边界（Suspense）

```html
<Suspense>
  <template #default>
    <AsyncChild />  <!-- 异步加载 -->
  </template>
  <template #fallback>
    加载中...
  </template>
</Suspense>
```

```javascript
// Suspense 内部：
// 1. 渲染 default：遇到 async 组件 → 等待 Promise
// 2. Promise pending → 渲染 fallback
// 3. Promise resolve → 切换到 default
// 4. Promise reject → 渲染 error boundary
```

---

## 六、编写同构代码的原则

### 6.1 生命周期差异

```javascript
export default {
  created() { /* SSR + CSR 都执行 */ },
  mounted() { /* 仅 CSR */ },
  beforeUnmount() { /* 仅 CSR */ },
  serverPrefetch() { /* 仅 SSR */ }
}
```

### 6.2 跨平台 API 判断

```javascript
import { isServer } from 'vue'

if (isServer) {
  // Node.js 端
  const data = await fetchData()
} else {
  // 浏览器端
  document.title = 'loaded'
}

// 或用环境变量
import.meta.env.CLIENT  // true = 浏览器
```

### 6.3 状态污染问题

```javascript
// ❌ 模块级变量在多个请求间共享（SSR 大忌）
let cache = []

// ✅ 每个请求独立作用域
function handleRequest(req) {
  const cache = []  // 请求内私有
}
```

### 6.4 ClientOnly 组件

```html
<ClientOnly>
  <HeavyChart />  <!-- SSR 时跳过，只在 CSR 渲染 -->
</ClientOnly>
```
