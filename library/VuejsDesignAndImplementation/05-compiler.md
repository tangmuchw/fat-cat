# 05 - 编译器

> 源码：`packages/compiler-core/src/parse.ts`、`transform.ts`、`codegen.ts`

---

## 一、编译器工作流

```
模板字符串
     ↓
┌─────────────────────────┐
│      Parser（解析）       │  状态机驱动，逐字符扫描
│  模板字符串 → AST         │
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│     Transform（转换）     │  插件链，逐节点处理
│  AST → 优化后的 AST       │  v-if/v-for/v-once 标记
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│    Codegen（代码生成）    │  从 AST 生成 render 函数代码
│  AST → JavaScript 代码   │
└─────────────────────────┘

生成结果：
const render = function(_ctx) {
  return _h('div', { class: _ctx.class }, [_toDisplayString(_ctx.msg)])
}
```

---

## 二、解析器（Parser）

### 2.1 状态机

解析器维护一个**当前状态**（文本 / 标签开始 / 标签结束 / 属性），根据状态决定如何处理下一个字符。

```javascript
// 简化版状态机
const enum State {
  HTML_MODE,        // 解析 HTML 内容
  TAG_OPEN,         // 遇到 <，进入标签开始状态
  TAG_CLOSE,        // 遇到 </，进入闭合标签状态
  TAG_NAME,         // 解析标签名
  INSIDE_TAG,       // 解析标签内部属性
  TEXT,             // 解析文本内容
  INTERPOLATION,    // 解析 {{
}
```

### 2.2 核心解析循环

```javascript
function parse(template) {
  let cursor = 0
  while (cursor < template.length) {
    if (startsWith(template, cursor, '{{')) {
      // 插值解析
      parseInterpolation()
    } else if (template[cursor] === '<') {
      // 标签开始/结束
      if (template[cursor + 1] === '/') {
        parseTagEnd()     // 闭合标签
      } else if (/[a-zA-Z]/.test(template[cursor + 1])) {
        parseTagStart()   // 开始标签
      }
    } else {
      // 文本内容
      parseText()
    }
    cursor++
  }
}
```

### 2.3 AST 节点结构

```javascript
// 元素节点
{
  type: 'Element',
  tag: 'div',
  props: [
    { type: 'Attribute', name: 'class', value: 'container' },
    { type: 'Directive', name: 'bind', exp: '_ctx.msg' }
  ],
  children: []
}

// 文本节点
{ type: 'Text', content: 'hello' }

// 插值节点
{ type: 'Interpolation', content: { type: 'Expression', value: '_ctx.msg' } }
```

### 2.4 递归下降解析

```javascript
// 解析 <div class="box">hello <span>nested</span> world</div>

parseElement() {
  // 1. 解析标签名
  const tag = parseTagName()

  // 2. 解析属性
  const props = parseAttributes()

  // 3. 自闭合判断
  if (template[cursor] === '/>') { return node }

  // 4. 解析子节点（递归下降）
  const children = []
  while (!isTagEnd()) {
    children.push(parseNode())  // 递归
  }

  return { type: 'Element', tag, props, children }
}
```

### 2.5 HTML 实体解码

```javascript
// 命名字符引用：如 &nbsp; → 空格
// 使用 Trie 树加速查找
function decodeHtmlEntity(html) {
  let result = ''
  let i = 0
  while (i < html.length) {
    if (html[i] === '&') {
      const end = html.indexOf(';', i)
      if (end !== -1) {
        const entity = html.slice(i + 1, end)
        if (entity in HTML_ENTITIES) {
          result += HTML_ENTITIES[entity]
          i = end + 1
          continue
        }
      }
    }
    result += html[i++]
  }
  return result
}

// 数字字符引用：如 &#60; → < 或 &#x3C; → <
```

---

## 三、Transform（转换）

### 3.1 插件链

```javascript
// transform.ts
const nodeTransforms = [
  transformOnce,      // 标记 v-once 静态节点
  transformIf,         // v-if 转为三元表达式
  transformFor,       // v-for 转为循环函数
  transformExpression, // 解析插值中的变量路径
  transformSlot,      // v-slot
  transformElement,   // v-bind/v-on
]
```

### 3.2 v-if 转换

```html
<div v-if="ok">yes</div>
<div v-else-if="maybe">maybe</div>
<div v-else>no</div>

<!-- 编译后 -->
ok ? _h('div', 'yes') : maybe ? _h('div', 'maybe') : _h('div', 'no')
```

```javascript
// transformIf.ts
function transformIf(node) {
  // 收集 v-if / v-else-if / v-else 分支
  const branches = []
  let current = node
  while (current) {
    if (current.props.find(p => p.name === 'v-if')) {
      branches.push({ condition: current.props.find(p => p.name === 'v-if').exp, node: current })
      break
    } else if (current.props.find(p => p.name === 'v-else')) {
      branches.push({ condition: null, node: current })
      break
    }
    current = current.children[0]  // 继续向下找
  }

  // 用三元表达式拼接
  const last = branches.pop()
  let returned = createCall('h', [last.node.tag, ...])
  while (branches.length) {
    const branch = branches.pop()
    returned = createConditional(branch.condition, returned, createCall('h', [...]))
  }
}
```

### 3.3 v-for 转换

```html
<li v-for="item in list" :key="item.id">{{ item.name }}</li>

<!-- 编译后 -->
list.map(item => _h('li', { key: item.id }, [_toDisplayString(item.name)]))
```

### 3.4 静态提升（Static Hoisting）

```html
<div>
  <span>static text</span>
  {{ dynamic }}
</div>

<!-- 编译后：static 部分提升到渲染函数外，只创建一次 -->
const _hoisted = _h('span', 'static text')
function render(_ctx) {
  return _h('div', [_hoisted, _toDisplayString(_ctx.dynamic)])
}
```

### 3.5 PatchFlag 生成

编译器分析模板中的动态部分，生成 PatchFlag：

```html
<div :class="cls" :id="id">{{ text }}</div>

<!-- 编译后 -->
_h('div', {
  [__PatchFlags.CLASS]: _ctx.cls,
  [__PatchFlags.PROPS]: { id: _ctx.id }
}, [_toDisplayString(_ctx.text, __PatchFlags.TEXT)])
```

---

## 四、Codegen（代码生成）

### 4.1 生成器结构

```javascript
// codegen.ts
function generate(ast) {
  const code = ast.body.map(statement => genNode(statement))
  return `const render = function(_ctx) { return ${code} }`
}

function genNode(node) {
  switch (node.type) {
    case 'Element': return genElement(node)
    case 'Text': return `_v("${node.content}")`
    case 'Interpolation': return `_toDisplayString(${genExpression(node.content)})`
    case 'Conditional': return `${genExpression(node.test)} ? ${genNode(node.consequent)} : ${genNode(node.alternate)}`
    case 'For': return `${genExpression(node.source)}.map(${genIterator})`
  }
}
```

### 4.2 genElement 完整示例

```javascript
function genElement(node) {
  const { tag, props, children, patchFlag } = node

  // 1. 生成 props 对象（带 PatchFlag）
  const propsCode = genProps(props, patchFlag)

  // 2. 生成 children
  let childrenCode = ''
  if (children.length === 1 && children[0].type === 'Text') {
    childrenCode = `"${children[0].content}"`  // 文本子节点优化
  } else if (children.length > 0) {
    childrenCode = children.map(c => genNode(c)).join(', ')
  }

  // 3. 组装
  if (childrenCode) {
    return `_h('${tag}', ${propsCode}, [${childrenCode}])`
  } else {
    return `_h('${tag}', ${propsCode})`
  }
}
```

---

## 五、SSR 编译

### 5.1 思路

SSR 编译目标是**生成 HTML 字符串**，而不是 render 函数返回 vnode：

```javascript
// SSR Codegen
function ssrGenerate(node) {
  switch (node.type) {
    case 'Element':
      const tag = node.tag
      const html = `<${tag}>`
      const children = node.children.map(ssrGenerate).join('')
      return html + children + `</${tag}>`
    case 'Text':
      return escapeHtml(node.content)
    case 'Interpolation':
      return `{{ ${node.content} }}`  // 占位符
  }
}
```

### 5.2 SSR 渲染函数

```javascript
// 服务端执行
function renderToString(component) {
  const vnode = createVNode(component.type, component.props)
  return vnode.type.render(vnode).children  // 取文本拼接
}
```

---

## 六、编译优化总结

| 优化手段 | 原理 | 效果 |
|---|---|---|
| **静态提升** | 不变的 vnode 提到 render 函数外 | 减少重复创建 |
| ** PatchFlag** | 标记动态属性/文本类型 | patch 时只比较动态部分 |
| **预字符串化** | 20+ 静态子节点序列化为 innerHTML | 减少 vnode 创建 |
| **事件缓存** | `@click="count++"` 函数引用缓存 | 避免重复 bind |
| **Block** | 收集动态子节点列表，统一 patch | 减少递归层级 |
