# Vue.js 3 核心原理精要

> 基于《Vue.js设计与实现》霍春阳 著，精简自 18 章完整笔记

---

## 目录

1. [框架设计哲学](#1-框架设计哲学)
2. [响应系统](#2-响应系统)
3. [非原始值的响应式方案](#3-非原始值的响应式方案)
4. [原始值与 ref](#4-原始值与-ref)
5. [渲染器](#5-渲染器)
6. [Diff 算法](#6-diff-算法)
7. [组件机制](#7-组件机制)
8. [内建组件](#8-内建组件)
9. [编译器](#9-编译器)
10. [同构渲染](#10-同构渲染)

---

## 1. 框架设计哲学

### 1.1 命令式 vs 声明式

| | 命令式 | 声明式 |
|---|---|---|
| 特点 | 关注**过程**，逐行写 DOM 操作 | 关注**结果**，描述最终状态 |
| 性能 | 最优（精准修改） | 额外 B（找差异）+ A（直接修改） |
| 可维护性 | 低（维护整个过程） | 高（只看结果） |
| 代表 | jQuery | Vue.js |

**结论**：声明式代码性能 = B + A，框架设计者的任务是在保持可维护性的同时，让 B 尽可能小（虚拟 DOM 的核心价值）。

### 1.2 框架设计的核心要素

- **开发体验**：友好的警告信息（`warn`）、自定义 formatter、详细的错误栈
- **代码体积**：通过 `__DEV__` 常量在构建时区分开发/生产环境，开发警告不进入生产包
- **Tree-Shaking**：使用 `__DEV__` + 纯净 API（无副作用），让打包工具消除未使用的代码
- **构建产物**：IIFE（`<script>`直接用）、ESM（按需导入）、CJS（Node.js）
- **特性开关**：编译时根据用户配置关闭不需要的特性，进一步减小体积
- **TypeScript 支持**：良好的类型推导，减少运行时错误

### 1.3 运行时 vs 编译时

Vue.js 3 采用**运行 + 编译时混合**方案：
- 模板 → 编译优化 → 生成带动态节点标记的代码（编译时减少运行时 Diff 开销）
- 虚拟 DOM 渲染函数 → 运行时跨平台

---

## 2. 响应系统

### 2.1 核心概念

**副作用函数**：执行时会间接影响其他函数执行的函数（如修改全局变量、设置 DOM 内容）

**响应式数据**：当数据变化时，相关副作用函数自动重新执行

### 2.2 基本实现原理

```
读取 obj.text  → 把 effect 存入"桶"  →  设置 obj.text  →  从"桶"取出 effect 执行
     (get)                                    (set)
```

核心用 Proxy 拦截 get/set：

```javascript
const bucket = new Set()
const data = { text: 'hello' }
const obj = new Proxy(data, {
  get(target, key) {
    bucket.add(effect)   // 读取时收集依赖
    return target[key]
  },
  set(target, key, newVal) {
    target[key] = newVal
    bucket.forEach(fn => fn())  // 写入时触发更新
    return true
  }
})
```

### 2.3 完善响应系统

真实 Vue.js 3 响应系统比上述示例复杂得多：

**分支切换与 cleanup**：条件渲染中，不满足条件的分支不应建立响应联系，需要在重新执行前清除旧联系

```javascript
let temp
const obj = { ok: true, text: 'hello' }
effect(() => {
  // 每次重新执行前先清除
  cleanup()
  if (obj.ok) {
    temp = obj.text  // 读取 obj.text
  }
})
```

**嵌套 effect**：effect 可以嵌套，内层 effect 执行时，外层 effect 应该暂停

```javascript
effect(() => {
  effect(() => { /* 嵌套 */ })  // 内层先执行完，外层再继续
})
```

**避免无限递归**：在 trigger 中检测是否等同于当前执行的 effect，避免自己触发自己时无限递归

**调度执行**：通过 `effect(options.scheduler)` 让用户控制副作用函数的执行时机（如微任务、宏任务）

### 2.4 计算属性与 watch

**计算属性** `computed`：
- 惰性求值（lazy）：只有真正读取时才计算
- 缓存机制（dirty flag）：依赖不变时返回缓存值，不重新计算
- 嵌套在 effect 中时自动收集依赖

**watch**：
- 本质是对计算属性的深度监听
- 支持 `immediate`（立即执行一次）
- 支持 `flush` 控制时机（pre/post/sync）
- 过期的副作用用 `onInvalidate` 处理竞态问题

---

## 3. 非原始值的响应式方案

### 3.1 Proxy + Reflect

Vue.js 3 用 **Proxy** 代理整个对象，**Reflect** 提供默认行为：

```javascript
const obj = new Proxy(data, {
  get(target, key, receiver) {
    track(target, key)       // 收集依赖
    return Reflect.get(target, key, receiver)
  },
  set(target, key, newVal, receiver) {
    const res = Reflect.set(target, key, newVal, receiver)
    trigger(target, key)     // 触发更新
    return res
  }
})
```

### 3.2 代理 Object

**get**：返回属性值时，如果是对象则递归代理（深响应）；如果是数组，访问 `length` 时也要追踪

**set**：严格区分新增属性 vs 已有属性（通过 `hasOwnProperty` 判断），触发不同的 `trigger` 类型

### 3.3 浅响应 vs 深响应

- `reactive` / `ref(inner)`：深响应（递归代理嵌套对象）
- `shallowReactive` / `ref(inner)`：浅响应（只代理第一层）
- `readonly`：只读代理，任何写入操作报警告

### 3.4 代理数组的特殊处理

- **索引与 length**：修改索引可能触发 `length` 追踪；设置 `length` 小于索引会触发删除
- **for...in 遍历**：`enumerateIndexedDeps` 追踪索引依赖
- **隐式修改长度的方法**（`push`/`pop`/`splice`）：Vue.js 对这些方法做了特殊处理，避免由 length 变化引发的重复触发
- **查找方法**（`includes`/`indexOf`/`lastIndexOf`）：在代理中返回的值与原始值不同，需要在方法实现中用原始值查找

### 3.5 代理 Set 和 Map

Set/Map 不能像普通对象那样代理，需要逐个实现：

- `get(target, key)` 拦截：`get` 返回 Set/Map 的方法本身或迭代器
- `size` 属性：通过 `Reflect.get(target, key, receiver)` 获取，但需要让 `size` 可追踪
- 污染问题：Set 的 `add`/`delete` 方法返回 Set 本身，不能直接返回 `Reflect` 的结果
- `forEach`：需要建立与所有 value 的依赖联系
- 迭代器方法（`entries`/`keys`/`values`/`[Symbol.iterator]`）：需要特殊处理

---

## 4. 原始值与 ref

### 4.1 ref 的本质

原始值（string/number/boolean）不能像对象一样被 Proxy 代理，需要用**引用**包装：

```javascript
function ref(initialValue) {
  return {
    get value() {
      trackRefValue()
      return initialValue
    },
    set value(newVal) {
      initialValue = newVal
      triggerRefValue()
    }
  }
}
```

### 4.2 响应丢失问题

`ref` 返回对象，解构后失去响应性。解决：使用 `toRef` / `toRefs` 保持解构后的响应联系

### 4.3 自动脱 ref

模板中 `{{ count }}` 自动访问 `.value` 而不需要写 `.value`，通过 `proxyRefs` 拦截 `get`，在读取 `ref` 类型的属性时自动解包

---

## 5. 渲染器

### 5.1 渲染器的基本概念

渲染器的核心职责：**将虚拟 DOM 渲染为真实 DOM**

```javascript
function renderer(vnode, container) {
  const el = document.createElement(vnode.type)
  el.innerText = vnode.children
  container.appendChild(el)
}
```

Vue.js 3 渲染器的特点：**跨平台能力**（同一套逻辑，替换不同平台的 DOM API 即可运行在小程序、SSR 等环境）

### 5.2 渲染器的核心操作

| 操作 | 说明 |
|---|---|
| `mountElement` | 创建 DOM 并挂载到容器 |
| `patch` | 对比新旧 vnode，决定如何更新 |
| `unmount` | 卸载 vnode，清除副作用 |
| `patchChildren` | 对比并更新子节点列表 |

### 5.3 渲染器与响应系统的结合

```javascript
const count = ref(1)
effect(() => {
  renderer(`<h1>count.value</h1>`, container)
})
count.value++  // 自动触发重新渲染
```

### 5.4 渲染器设计要点

- **HTML Attributes vs DOM Properties**：优先设置 DOM Properties，特殊情况处理（布尔属性 `disabled`、枚举属性 `contentEditable`）
- **class 处理**：支持字符串、对象、数组等多种形式，转换为字符串后设置
- **事件处理**：用 `el.addEventListener(eventName, handler)` 绑定，缓存事件处理函数以支持事件更新
- **更新时机**：微任务队列中批量执行，避免同步更新时的重复渲染
- **Fragment**：组件返回多个根节点时，用 Fragment 包装

---

## 6. Diff 算法

### 6.1 简单 Diff

**核心思想**：遍历新旧 children 中较短的那一组，逐个 patch；然后处理多出的部分（新增挂载或旧节点卸载）

**问题**：没考虑节点顺序变化，会产生大量不必要的移动操作

### 6.2 双端 Diff

**核心思想**：新旧 children 各有两个指针（头尾），同时从两端向中间比较

比较四次：
1. 新头 vs 旧头
2. 新尾 vs 旧尾
3. 新头 vs 旧尾（头变尾）
4. 新尾 vs 旧头（尾变头）

找到可复用节点后，调用 `patch` 打补丁，然后移动到正确位置

**局限**：非理想状况（中间节点乱序）时需要退化处理

### 6.3 快速 Diff（Vue.js 3 采用）

**核心思想**：先处理**相同的前置节点**和**相同的后置节点**，中间区域用**最长递增子序列**（LIS）算法确定最小移动

步骤：
1. 跳过相同的前置元素
2. 跳过相同的后置元素
3. 处理剩余节点：
   - 新 key → 旧无 key → 新增
   - 新 key → 旧有 key → 可复用 patch，复位到正确位置
   - 旧 key → 新无 key → 卸载
4. 根据 **LIS** 移动现有节点到正确顺序

**优势**：充分利用编译器生成的 key 信息，最小化 DOM 移动

---

## 7. 组件机制

### 7.1 组件的本质

组件是**返回虚拟 DOM 的函数**（或包含 `render` 方法的对象），Vue.js 3 用 `defineComponent` 包装：

```javascript
const MyComponent = {
  render() {
    return h('div', { class: 'container' }, this.message)
  },
  data() {
    return { message: 'Hello' }
  }
}
```

### 7.2 组件实例

每个组件在渲染时会创建一个**组件实例**，包含：
- 组件自身的状态（`data()`）
- 生命周期状态
- 插槽内容
- 渲染结果（`subTree`）

实例与 vnode 一一对应，vnode 的 `component` 属性指向实例。

### 7.3 组件更新

组件被动更新（父组件重新渲染 → 触发子组件更新）：
- **props 更新**：子组件的 props 是响应式的，变化时触发更新
- **setup**：在 `setup` 中可以返回函数（render）或对象（暴露给模板）
- **emit**：子组件通过 `emit` 触发事件，父组件用 `@event` 监听

### 7.4 生命周期

| 钩子 | 时机 |
|---|---|
| `beforeCreate` | 实例初始化之后，数据响应式之前 |
| `created` | 数据响应式完成后 |
| `beforeMount` | 挂载前 |
| `mounted` | 挂载后 |
| `beforeUpdate` | 更新前 |
| `updated` | 更新后 |
| `beforeUnmount` | 卸载前 |
| `unmounted` | 卸载后 |

### 7.5 插槽

- **编译时**：`:slot` 属性 → `setupContext.slots`
- **运行时**：`vnode.children` 作为插槽内容传递给子组件
- **默认插槽**：直接作为子组件的子节点
- **具名插槽**：通过名称分发到对应的 `<slot>`

---

## 8. 内建组件

### 8.1 KeepAlive

**核心**：缓存已渲染的组件实例，再次进入时直接激活而非重新创建

```html
<KeepAlive>
  <Component v-if="show" />
</KeepAlive>
```

实现要点：
- **激活**（activate）：从缓存取出，复用 DOM 节点，触发 `onActivated`
- **失活**（deactivate）：放入缓存，复用 DOM 节点，触发 `onDeactivated`
- **缓存策略**：`max` 控制最大缓存数量（LRU）
- **include/exclude**：按组件名过滤是否缓存

### 8.2 Teleport

将组件的 DOM 传送到任意指定节点：

```html
<Teleport to="body">
  <Modal />
</Teleport>
```

实现：将 Teleport 的子节点**直接挂载到目标容器**（`document.body`），而非父组件的容器

### 8.3 Transition

为 DOM 元素的进入/离开提供 CSS 过渡效果：

- **原生 DOM**：在 `mounted`/`unmounted` 时添加/移除 CSS 类名
- **vnode 类型**：`ANIMATION`（动画）、`TRANSITION`（过渡）
- CSS 类名规则：`v-enter` → `v-enter-to` 进入；`v-leave` → `v-leave-to` 离开

---

## 9. 编译器

### 9.1 编译器工作流

```
模板字符串
    ↓ parser（解析）
抽象语法树（AST）
    ↓ transform（转换）
模板 AST（优化）
    ↓ generate（生成）
渲染函数代码 / 服务端渲染代码
```

### 9.2 解析器（Parser）

**状态机驱动**：根据当前解析状态（文本、标签开始、标签结束、属性等）决定如何处理下一个字符

核心节点类型：
- `Element`：标签节点（`div`、`span` 等）
- `Text`：文本节点
- `Interpolation`：插值（`{{ count }}`）
- `Directive`：指令（`v-if`、`v-for` 等）

递归下降算法：从上到下解析标签，递归处理子节点

HTML 实体解码：
- 命名字符引用（`&nbsp;` → ` `）：用Trie树查找
- 数字字符引用（`&#60;` → `<`）：解析为十/十六进制数字

### 9.3 AST 转换

遍历 AST 节点，通过**插件链**（transform plugins）逐个处理：
- `v-if` 转换：`IF` 节点 + `Branch` 节点（处理 `v-else-if`/`v-else`）
- `v-for` 转换：提取 `source`/`iterator`/`key` 等信息
- `v-once` 标记：标记为静态节点，跳过后续 Diff

### 9.4 代码生成

从模板 AST 生成 JavaScript 代码：
- `genElement`：生成 `h(tag, props, children)` 调用
- `genInterpolation`：生成对响应式数据的访问
- `genDirective`：生成对应指令的运行时处理

### 9.5 编译优化（SSR/客户端共用）

**Block 与 PatchFlags**：编译器在模板中标记出哪些是动态节点（文本/属性/事件等），运行时只对这些节点进行 Diff

**静态提升**：
```javascript
// 编译前
<div><span>static</span>{{ dynamic }}</div>
// 编译后：static 部分提升到渲染函数外，只创建一次
const static = h('span', 'static')
render() { return h('div', [static, dynamic]) }
```

**预字符串化**：静态元素超过 20 个时，序列化为字符串直接 innerHTML

**事件缓存**：内联事件处理函数（如 `@click="count++"`）缓存函数引用，避免每次渲染都创建新函数

---

## 10. 同构渲染

### 10.1 CSR vs SSR vs 同构

| 方案 | 首屏速度 | SEO | 交互性 | TTID |
|---|---|---|---|---|
| CSR | 慢（需等 JS） | 差 | 好 | 慢 |
| SSR | 快（直出 HTML） | 好 | 差（需水合） | 快 |
| 同构（SSR + 客户端激活） | 快 | 好 | 好 | 快 |

### 10.2 SSR 工作流程

```
组件渲染函数
    ↓
虚拟 DOM → 渲染为 HTML 字符串
    ↓
返回完整 HTML（含 hydration 标记）
    ↓
客户端下载 JS，激活 hydration（水合）
```

### 10.3 客户端激活（Hydration）

将服务器返回的 HTML "附着"上 Vue.js 的响应式能力：
1. Vue.js 遍历服务器返回的 HTML
2. 根据 vnode 结构找到对应 DOM 节点
3. 为 DOM 节点绑定事件、响应式状态
4. 之后由 Vue.js 接管 DOM 更新

### 10.4 同构代码编写原则

- **生命周期**：`beforeMount`/`mounted` 在 SSR 时不执行；`onServerPrefetch` 仅服务端执行
- **跨平台 API**：`window`/`document` 在 Node.js 中不存在，需要用 `isServer` 判断
- **模块引入**：仅客户端使用的模块（`document.body.scroll`）用 `import.meta.env.CLIENT` 包裹
- **状态污染**：多个请求共享模块级变量会导致状态污染，需要用 `requestContext` 或每次请求独立的作用域
- **`<ClientOnly>`**：仅在客户端渲染（SSR 时跳过），用于避免 SSR 不支持的特性（如浏览器 API 调用）

---

## 附录：模块关系图

```
用户模板
    ↓
┌─────────────────────────────────────┐
│           编译器（编译时）             │
│  parser → AST → transform → generate │
└──────────┬──────────────────────────┘
           ↓ 生成渲染函数 + 优化标记
┌─────────────────────────────────────┐
│           运行时（运行时）             │
│  createApp → 组件实例 → render()     │
│                    ↓                 │
│               虚拟 DOM (vnode)       │
│                    ↓                 │
│               渲染器 renderer          │
│      ┌───────────┴──────────┐        │
│   挂载                    更新        │
│   (mount)    Diff 算法    (patch)   │
│                        ↓             │
│               真实 DOM 更新           │
└─────────────────────────────────────┘

响应系统（reactivity）
  └─ 被渲染器引用：effect(() => render())
  └─ 被组件引用：data() / computed / watch
```
