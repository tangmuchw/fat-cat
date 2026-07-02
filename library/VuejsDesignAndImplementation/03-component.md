# 03 - 组件机制（Component）

> 源码：`packages/runtime-core/src/component.ts`、`componentRenderUtils.ts`、`apiWatch.ts`、`apiLifecycle.ts`、`helpers/slots.ts`

---

## 一、组件的本质

组件是一个**返回 vnode 的对象**（或函数）：

```javascript
// 最简组件
const MyComponent = {
    render() {
        return h("div", "hello");
    },
};

// defineComponent 只是把对象结构化，本身不增加响应式逻辑
const MyComponent = defineComponent({
    data() {
        return { msg: "hello" };
    },
    render() {
        return h("div", this.msg);
    },
});
```

---

## 二、组件实例创建

### 2.1 createComponentInstance

```javascript
// packages/runtime-core/src/component.ts

function createComponentInstance(vnode) {
    const type = vnode.type; // 用户组件对象

    const instance = {
        type,
        vnode, // vnode 引用实例
        el: null, // 挂载后指向真实 DOM
        props: {}, // props（只读）
        attrs: {}, // 未声明的 attrs（非 props 部分）
        slots: {}, // 插槽
        ctx: {}, // 组件上下文（provide/inject 等）
        setupState: {}, // setup() 返回的对象
        data: null, // data() 返回的对象
        render: null, // render 函数
        proxy: null, // 组件代理（访问 this.xxx）
        isMounted: false,
        isUnmounted: false,
        update: null, // 组件的 update effect
        next: null, // 待更新的 vnode（用于异步更新）
        bc: null, // beforeCreate
        bm: null, // beforeMount
        m: null, // mounted
        bu: null, // beforeUpdate
        u: null, // updated
        um: null, // unmounted
    };

    return instance;
}
```

---

## 三、setup() 执行

setup 是组件初始化阶段**最先执行的选项**，在 props 解析之后、data 之前。

### 3.1 setup 返回值两种形式

```javascript
// 形式1：返回对象 → 直接成为组件实例的代理属性
const Comp = {
    setup() {
        const count = ref(0);
        return { count }; // 模板中 this.count 直接用
    },
};

// 形式2：返回函数 → 作为 render 函数
const Comp = {
    setup(props, { emit }) {
        return () => h("div", props.msg + "!");
    },
};
```

### 3.2 setupStatefulComponent

```javascript
// packages/runtime-core/src/componentRenderUtils.ts

function setupStatefulComponent(instance) {
    const Component = instance.type;

    // 1. 创建组件代理（访问 this）
    // 模板中 this.count → proxy.count → setupState.count / data.xxx / props.xxx
    instance.proxy = new Proxy(instance.ctx, {
        get(target, key) {
            const res = resolveSetupState(instance, key);
            if (res !== undefined) return res;
            // 依次从 setupState → data → props → ctx 查找
        },
    });

    // 2. 执行 setup(props, { emit, slots, expose })
    const setup = Component.setup;
    if (setup) {
        const setupContext = {
            attrs: instance.attrs,
            slots: instance.slots,
            emit: bind(emit, instance),
            expose: (exposed) => Object.assign(instance.exposed, exposed),
        };
        const setupResult = setup(instance.props, setupContext);

        // 3. 处理 setup 返回值
        if (typeof setupResult === "function") {
            // 返回 render 函数
            instance.render = setupResult;
        } else if (typeof setupResult === "object") {
            // 返回响应式对象
            instance.setupState = reactive(setupResult);
        }
    }

    // 4. 解析 data
    if (Component.data) {
        instance.data = Component.data();
    }

    // 5. 编译 render 函数（模板没有 render 时）
    if (!instance.render) {
        instance.render = Component.template
            ? compile(Component.template, runtimeDOMOptions)
            : () => {};
    }
}
```

---

## 四、组件渲染（renderComponentNode）

组件的 render 也是一个 effect：**读取响应式数据 → 返回 vnode**。

```javascript
// packages/runtime-core/src/componentRenderUtils.ts

function renderComponentRoot(instance) {
    const { type: Component, vnode, proxy } = instance;

    // 执行 render 函数：render(this) = render(proxy)
    // render 中访问 this.xxx → proxy.xxx → 响应式追踪
    const subTree = instance.render.call(proxy, proxy);

    // 递归 patch 渲染子节点
    patch(null, subTree, container);
    return subTree;
}
```

---

## 五、组件更新流程

### 5.1 更新触发

```
响应式数据变化
  → trigger 找到组件的 update effect
  → scheduler: queueJob(update)
  → 微任务中批量执行
    → renderComponentRoot(instance)
      → instance.render() 重新执行 → 新的 vnode
      → patch(prevSubTree, nextSubTree) 对比更新
```

### 5.2 异步更新合并

同一 tick 中多次修改同一响应式数据，只触发一次 render：

```javascript
// count.value++ 三次
// → 触发三次 trigger
// → 但 update effect 已在队列中
// → 队列去重后只执行一次 render
queueJob(update);
// 微任务执行时：count 已经是最终值，只 patch 一次
```

---

## 六、props 与 attrs

### 6.1 区分规则

```javascript
// 子组件声明了 props
const Child = {
    props: ["msg", "count"],
};

// 父组件传递
// <Child msg="hello" count="1" class="wrapper" />

// msg 和 count → props（声明过的）
// class="wrapper" → attrs（未声明的）
```

### 6.2 props 响应式

props 是**只读的响应式对象**，子组件修改 props 会报警告：

```javascript
// 子组件中
this.msg = "new value"; // 警告：props are readonly
```

props 变化触发子组件更新的原理：

```javascript
// 父组件 render 执行
// <Child :msg="msg" />
// msg 是响应式的 → Child 的 props.msg 自动更新
// props 更新触发 Child 的 update effect 重新执行
```

---

## 七、生命周期钩子

### 7.1 钩子注册

```javascript
// 用户代码
export default {
    mounted() {
        console.log("mounted");
    },
};

// Vue 内部
// 在组件实例创建时，从 Component 选项中提取，存入 instance.m
// 执行时机在组件渲染过程中
```

### 7.2 时序图

```
createComponentInstance
    ↓
beforeCreate  ← 实例刚创建，data/props 未解析
    ↓
setup()        ← 最先执行（可返回 render 或对象）
    ↓
created       ← data/props 已就绪
    ↓
render()      ← 编译 render（如果需要）
    ↓
beforeMount   ← 首次挂载前
    ↓
patch()       ← 挂载 DOM
    ↓
mounted       ← DOM 已挂载
    ↓（响应式数据变化）
beforeUpdate  ← patch 前
    ↓
patch()       ← 更新 DOM
    ↓
updated       ← DOM 已更新
    ↓（unmount）
beforeUnmount ← 卸载前
    ↓
unmount()     ← DOM 移除
    ↓
unmounted     ← 完全卸载
```

---

## 八、provide / inject

### 8.1 实现原理

provide/inject 本质是**基于实例 ctx 的属性查找链**：

```javascript
// 父组件
setup() {
  provide('theme', 'dark')
  return { /* ... */ }
}

// 子组件
setup() {
  const theme = inject('theme')
  return { theme }
}
```

查找路径：子组件 ctx → 父组件 ctx → 爷组件 ctx → ... → 根组件 ctx

### 8.2 源码简析

```javascript
function provide(key, value) {
    // 当前组件实例的 ctx 上存一份
    const currentInstance = getCurrentInstance();
    currentInstance.ctx[key] = value;
}

function inject(key) {
    const currentInstance = getCurrentInstance();
    // 从当前实例向上遍历 ctx 链查找
    let parent = currentInstance.parent;
    while (parent) {
        if (parent.ctx[key] !== undefined) {
            return parent.ctx[key];
        }
        parent = parent.parent;
    }
}
```

---

## 九、插槽（slots）

### 9.1 编译时

```html
<!-- 父组件模板 -->
<Layout>
    <template #header>导航</template>
    <template #default>内容</template>
</Layout>

<!-- 编译后 vnode.children -->
Layout.children = [ { key: 'header', fn: () => h('div', '导航') }, { key:
'default', fn: () => h('div', '内容') } ]
```

### 9.2 子组件使用插槽

```html
<!-- 子组件模板 -->
<div class="layout">
    <slot name="header" />
    <slot />
</div>

<!-- 编译后 render 函数 -->
render() { return [ h('div', { class: 'layout' }, [ slots.header?.() || null, //
调用插槽函数，返回 vnode slots.default?.() || null ]) ] }
```

### 9.3 作用域插槽

子组件数据传递给插槽内容：

```html
<!-- 子组件 -->
<slot :item="item" :index="index" />

<!-- 父组件使用 -->
<Comp>
    <template #default="{ item, index }">
        {{ index }}: {{ item.name }}
    </template>
</Comp>
```

原理：**插槽函数携带子组件作用域的变量**，`item` 和 `index` 在调用 `slots.default()` 时传入。

---

## 十、组件实例的代理（this）

Vue 3 中组件 render 里的 `this` 指向一个代理：

```javascript
// 模板中 {{ this.count }}
// 实际等于 proxy.count

const proxy = new Proxy(instance, {
    get(target, key) {
        // 依次查找：
        // 1. setupState（setup 返回的对象）
        // 2. data（data() 返回的对象）
        // 3. props（显式声明的 props）
        // 4. ctx 上的 provide/inject 等
        // 5. 原型链（Vue 公开的 $parent 等）
    },
    set(target, key, value) {
        // 同上，但优先查找 setupState/data
    },
});
```

优先级：**setupState > data > props > ctx**
