# 04 - Diff 算法

> 源码：`packages/runtime-core/src/renderer.ts`（patchKeyedChildren / patchUnkeyedChildren）

---

## 一、Diff 的问题背景

对比两个 vnode 树，找出最小 DOM 操作次数的更新方案。

声明式更新性能 = **找差异的成本（B）+ 应用差异的成本（A）**。Diff 算法就是在最小化 B。

---

## 二、简单 Diff（简单对比）

### 2.1 实现思路

```javascript
// 遍历新旧 children 中较短的那个，逐个 patch
function simpleDiff(prevChildren, nextChildren, container) {
  const minLen = Math.min(prevChildren.length, nextChildren.length)

  // 1. 逐个 patch 前 minLen 个
  for (let i = 0; i < minLen; i++) {
    patch(prevChildren[i], nextChildren[i], container)
  }

  // 2. 新 children 更长 → 剩余是新增的，挂载
  if (nextChildren.length > minLen) {
    for (let i = minLen; i < nextChildren.length; i++) {
      mountElement(nextChildren[i], container)
    }
  }

  // 3. 旧 children 更长 → 剩余是删除的，卸载
  if (prevChildren.length > minLen) {
    for (let i = minLen; i < prevChildren.length; i++) {
      unmount(prevChildren[i])
    }
  }
}
```

**问题**：完全没考虑节点**顺序变化**，顺序一变就全部卸载重建。

---

## 三、双端 Diff（Vue 2 采用）

### 3.1 四指针比较

新旧 children 各两个指针（头部 `oldStartIdx/oldEndIdx`，尾部 `newStartIdx/newEndIdx`），同时从两端向中间推进。

```javascript
function doubleEndedDiff(prevChildren, nextChildren) {
  let oldStartIdx = 0, oldEndIdx = prevChildren.length - 1
  let newStartIdx = 0, newEndIdx = nextChildren.length - 1

  while (oldStartIdx <= oldEndIdx && newStartIdx <= newEndIdx) {
    // 四次尝试配对：
    // 1. 新头 vs 旧头
    // 2. 新尾 vs 旧尾
    // 3. 新头 vs 旧尾（节点从尾变到头）
    // 4. 新尾 vs 旧头（节点从头变到尾）

    if (isSameVnode(prev[oldStartIdx], next[newStartIdx])) {
      patch(prev[oldStartIdx], next[newStartIdx])
      oldStartIdx++; newStartIdx++
    } else if (isSameVnode(prev[oldEndIdx], next[newEndIdx])) {
      patch(prev[oldEndIdx], next[newEndIdx])
      oldEndIdx--; newEndIdx--
    } else if (isSameVnode(prev[oldStartIdx], next[newEndIdx])) {
      // 节点从旧头移动到新尾
      move(prev[oldStartIdx], newEndIdx)
      oldStartIdx++; newEndIdx--
    } else if (isSameVnode(prev[oldEndIdx], next[newStartIdx])) {
      // 节点从旧尾移动到新头
      move(prev[oldEndIdx], newStartIdx)
      oldEndIdx--; newStartIdx++
    } else {
      // 四次都没配上 → 退化：遍历旧的找可复用节点
    }
  }
}
```

### 3.2 退化处理

四次比较都失败时，退化为**遍历旧 children 查找可复用节点**：

```javascript
// 建立 key → index 的映射
const keyToOldIndex = {}
for (let i = 0; i < prevChildren.length; i++) {
  keyToOldIndex[prevChildren[i].key] = i
}

// 遍历新 children，逐个定位
for (let i = 0; i < nextChildren.length; i++) {
  const nextChild = nextChildren[i]
  if (keyToOldIndex.has(nextChild.key)) {
    // 旧中有这个 key → patch + 移动到正确位置
    patch(prev[keyToOldIndex[key]], nextChild)
  } else {
    // 旧中没有 → 新增
    mountElement(nextChild, container)
  }
}

// 旧中有新中没有 → 卸载
```

**问题**：退化后时间复杂度降为 O(n²)，且仍有不必要的移动。

---

## 四、快速 Diff（Vue 3 采用）

Vue 3 从两端向中间处理，中间区域用**最长递增子序列（LIS）** 定位最小移动。

### 4.1 完整流程

```javascript
function patchKeyedChildren(prevChildren, nextChildren, container) {
  let i = 0, newEnd = nextChildren.length - 1, oldEnd = prevChildren.length - 1

  // 1. 从头部同步（same key at head）
  while (i <= oldEnd && i <= newEnd &&
         prevChildren[i].key === nextChildren[i].key) {
    patch(prevChildren[i], nextChildren[i], container)
    i++
  }

  // 2. 从尾部同步（same key at tail）
  while (i <= oldEnd && i <= newEnd &&
         prevChildren[oldEnd].key === nextChildren[newEnd].key) {
    patch(prevChildren[oldEnd], nextChildren[newEnd], container)
    oldEnd--; newEnd--
  }

  // 3. 处理剩余情况
  if (i > oldEnd) {
    // 新 children 有剩余 → 全部新增
    for (let j = i; j <= newEnd; j++) {
      mountElement(nextChildren[j], container)
    }
  } else if (i > newEnd) {
    // 旧 children 有剩余 → 全部卸载
    for (let j = i; j <= oldEnd; j++) {
      unmount(prevChildren[j])
    }
  } else {
    // 4. 中间区域：建立映射表
    const keyToNewIndex = {}
    for (let j = i; j <= newEnd; j++) {
      keyToNewIndex[nextChildren[j].key] = j
    }

    // 5. 遍历旧 children，确定要 patch / 移动 / 卸载的
    let maxNewIndexSoFar = 0
    const newIndexToProcessed = new Array(newEnd - i + 1).fill(0)

    for (let j = i; j <= oldEnd; j++) {
      const prevChild = prevChildren[j]
      const newIndex = keyToNewIndex[prevChild.key]

      if (newIndex !== undefined) {
        // 旧 key 在新中也有 → patch
        patch(prevChild, nextChildren[newIndex], container)

        // 6. 用 LIS 确定最小移动
        // newIndexToProcessed[newIndex] = newIndex
        // LIS 用来确定哪些节点**不需要移动**
      } else {
        // 旧 key 在新中没有 → 卸载
        unmount(prevChild)
      }
    }
  }
}
```

### 4.2 最长递增子序列（LIS）

```javascript
// 接上面的 newIndexToProcessed
// newIndexToProcessed[newIndex] = newIndex（处理过的标记）

// 求 newIndexToProcessed（从 i 到 newEnd 段）的 LIS
// LIS 中的索引对应的节点不需要移动
// LIS 之外的节点需要移动

function lis(arr) {
  // 贪心 + 二分：O(n log n)
  const tails = []
  for (const val of arr) {
    let lo = 0, hi = tails.length
    while (lo < hi) {
      const mid = (lo + hi) >> 1
      if (tails[mid] <= val) lo = mid + 1
      else hi = mid
    }
    tails[lo] = val
    if (lo === tails.length) tails.push(val)
  }
  return tails.length  // LIS 长度
}
```

### 4.3 移动操作

```javascript
// 7. 根据 LIS 结果反向遍历，确定哪些节点需要移动
// 从尾部向前遍历（减少 DOM insertBefore 操作）

let j = newEnd
for (let k = lis.length - 1; k >= 0; k--) {
  const lisIndex = lis[k]         // LIS 中的位置
  const newIndex = i + lisIndex   // 对应到 newIndexToProcessed 的索引
  const anchor = newIndex + 1 < nextChildren.length
    ? nextChildren[newIndex + 1].el  // 锚点：后一个已处理的节点
    : null

  if (newIndexToProcessed[lisIndex] === 0) {
    // 之前未处理（新增的节点）→ 挂载
    patch(null, nextChildren[newIndex], container, anchor)
  } else {
    // 已处理过但不在 LIS → 移动
    insert(nextChildren[newIndex].el, container, anchor)
  }
}
```

---

## 五、为什么 key 至关重要

| 情况 | 无 key | 有 key |
|---|---|---|
| `[A,B,C] → [A,B,C]` | 3 次 patch，不移动 | 3 次 patch，不移动 |
| `[A,B,C] → [B,A,C]` | C 卸载再重建，2 次 DOM 操作 | 2 次 patch，0 次 DOM 操作 |
| `[A,B] → [A,B,C]` | C 新增 | C 新增 |
| `[A,B,C] → [A]` | B、C 卸载 | B、C 卸载 |

**无 key 时**：就地 patch（按 index 匹配），只适合列表**稳定追加/删除**的场景。  
**有 key 时**：通过 key 精确映射，能正确处理元素的**移动、重排**。

---

## 六、PatchFlag（编译优化）

编译器在模板中标记哪些是动态节点，运行时只对这些节点做 patch：

```javascript
// 模板编译后
const __PatchFlags = {
  TEXT: 1,           // 动态文本
  CLASS: 2,          // 动态 class
  STYLE: 4,          // 动态 style
  PROPS: 8,          // 动态 props（非 style/class 的属性）
  FULL_PROPS: 16,    // 需要全量 diff props
  HYDRATE_EVENTS: 32,
  STABLE_FRAGMENT: 64,
  KEYED_FRAGMENT: 128,
  UNKEYED_FRAGMENT: 256,
}

// 编译后 vnode 示例
h('div', {
  class: normalizeClass(_ctx.col),
  style: _ctx.style,
}, [
  createTextVNode(_Ctx.msg + _ctx.count, "1"),  // TEXT = 动态文本
  h('span', { class: 'static' }, '标签'),       // 无标记 = 完全静态
])
```

**无 PatchFlag 时**：整个 vnode 树都需要 diff。  
**有 PatchFlag 时**：只对动态部分做 patch，忽略静态部分。
