# Vue.js 设计与实现 — 源码笔记

基于 Vue 3 源码（`packages/` 目录）分析，聚焦**完整实现逻辑与核心算法**，以模块主线贯穿，不堆砌 PDF 原文。

---

## 文件结构

```
VuejsDesignAndImplementation/
├── README.md              ← 本文件，架构总览
├── 01-reactivity.md       ← 响应系统（effect / computed / ref / watch）
├── 02-renderer.md         ← 渲染器（mount / patch / unmount / nodeOps）
├── 03-component.md        ← 组件机制（实例 / setup / 生命周期 / provideinject / slots）
├── 04-diff.md             ← Diff 算法（简单 Diff / 双端 Diff / 快速 Diff + LIS）
├── 05-compiler.md         ← 编译器（parser 状态机 / transform 插件链 / codegen / SSR 编译）
├── 06-builtin.md          ← 内建组件（KeepAlive LRU / Teleport / Transition / Fragment）
├── 07-ssr.md              ← 同构渲染（SSR → HTML / Hydration 水合 / async component）
└── 08-advance.md          ← 进阶话题（Suspense / ErrorBoundary / nextTick / VNode / 自定义渲染器）
```

---

## 核心模块关系

```
templates / JSX / h()
            ↓
    ┌──────────────────┐
    │    编译器          │  packages/compiler-core + compiler-dom
    │  parser→AST→gen   │
    └────────┬─────────┘
             ↓
    ┌──────────────────┐
    │  运行时核心        │  packages/runtime-core
    │  组件实例 / render │  组件生命周期 / slots / provideinject
    └────────┬─────────┘
             ↓ render() 返回 vnode
    ┌──────────────────┐
    │   渲染器           │  packages/runtime-core/src/renderer.ts
    │  mount/patch      │  跨平台：runtime-dom / 小程序 / etc.
    └────────┬─────────┘
             ↓
    ┌──────────────────┐
    │   响应系统         │  packages/reactivity
    │  effect+track+trigger│  被 render 函数引用，驱动自动更新
    └──────────────────┘

    ┌──────────────────┐
    │   服务端渲染       │  packages/server
    │  renderToString   │  SSR → HTML 字符串
    └────────┬─────────┘
             ↓
         Hydration
             ↓
    ┌──────────────────┐
    │   客户端激活       │  packages/runtime-core/hydration.ts
    │  DOM + 响应式      │
    └──────────────────┘
```

---

## 阅读顺序建议

1. **先读 reactivity** — 理解 Vue 3 的"数据变化自动更新"核心机制
2. **再读 renderer** — 看 vnode 怎么变成真实 DOM
3. **读 component** — 组件实例、setup、render 的关联
4. **读 diff** — 对比新旧 vnode 树，找出最小 DOM 操作
5. **读 compiler** — 模板怎么变成 render 函数
6. **读 builtin** — KeepAlive / Teleport / Transition 三大特殊组件
7. **读 ssr** — 服务端渲染与客户端水合
8. **读 advance** — Suspense / nextTick / 自定义渲染器
