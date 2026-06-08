# 01 - 响应系统（Reactivity）

> 源码：`packages/reactivity/src/effect.ts`、`baseHandlers.ts`、`ref.ts`、`computed.ts`

---

## 一、副作用函数（effect）

### 1.1 什么是副作用函数

执行时会**间接影响其他函数结果**的函数。

```javascript
// 副作用函数：修改了全局状态
let count = 0;
function effect() {
    count++; // 任何读取 count 的地方都会看到新值
}
```

在 Vue 3 里，组件的 render 函数就是一个副作用函数——它读取响应式数据，当数据变化时自动重新执行。

### 1.2 effect 的完整实现

```javascript
// packages/reactivity/src/effect.ts

let activeEffect = null; // 当前正在执行的 effect
const effectStack = []; // effect 栈（支持嵌套）

function effect(fn, options) {
    const effectFn = createReactiveEffect(fn, options);
    // 默认立即执行一次（lazy=false）
    if (!options.lazy) {
        effectFn();
    }
    return effectFn;
}

function createReactiveEffect(fn, options) {
    const effect = function reactiveEffect() {
        // 关键：每次执行前 cleanup（清除旧的依赖联系）
        // 解决"分支切换后旧依赖没清除"的问题
        cleanup(effect);

        // 入栈：支持嵌套
        effectStack.push(effect);
        activeEffect = effect;

        // 执行用户函数 → 触发 Proxy get → 自动 track
        try {
            fn();
        } finally {
            // 出栈
            effectStack.pop();
            activeEffect = effectStack[effectStack.length - 1];
        }
    };

    // deps 数组：记住所有与这个 effect 关联的依赖集合
    // cleanup 时用来从各个 Set 中删除自己
    effect.deps = [];
    effect.options = options;
    effect.active = true;

    return effect;
}
```

### 1.3 cleanup（分支切换问题）

没有 cleanup 时：

```javascript
effect(() => {
    document.body.innerText = data.ok ? data.text : "default";
});
data.ok = false;
data.text = "world"; // 仍会触发 effect 重跑 —— 不应该！
```

有 cleanup 后：每次 effect 执行前，先从**所有关联的依赖集合中删除自己**，再重新执行，重新建立联系。

```javascript
function cleanup(effect) {
    // 倒序删除：删除数组中元素不会导致后续元素 index 错位
    for (let i = effect.deps.length - 1; i >= 0; i--) {
        effect.deps[i].delete(effect);
    }
    effect.deps.length = 0;
}
```

> **为什么要倒序？** 假设 `deps = [S1, S2, S3]`，正序删除 S1 后数组变成 `[S2, S3]`，`i=1` 时实际删的是原来的 S3（index 错位）。倒序无此问题。

### 1.4 嵌套 effect（组件场景）

组件渲染时，父子组件各有一个 render effect：

```javascript
effect(() => {           // 父组件 render effect
    render Parent
    effect(() => {       // 子组件 render effect（嵌套）
        render Child
    })
})
```

`effectStack` 保证：**内层 effect 执行时，只跟内层 effect 建立 track 联系**，外层 effect 的依赖不受内层影响。

---

## 二、依赖收集（track）

### 2.1 桶的数据结构

用 WeakMap → Map → Set 三层嵌套：

```
bucket (WeakMap)
└── target               (原始对象)
    └── key              (属性名)  →  Set<effect>
                                    ├── effect1
                                    └── effect2
```

**为什么用 WeakMap？** 当 target 没有任何引用时，GC 自动回收 WeakMap 的 entry，不泄漏内存。

### 2.2 track 实现

```javascript
// packages/reactivity/src/effect.ts

function track(target, key) {
    if (!activeEffect) return; // 不在 effect 中读取，跳过

    let depsMap = bucket.get(target);
    if (!depsMap) {
        bucket.set(target, (depsMap = new Map()));
    }
    let deps = depsMap.get(key);
    if (!deps) {
        depsMap.set(key, (deps = new Set()));
    }

    // 建立双向联系：
    // deps.add(activeEffect)       → key → effect
    // activeEffect.deps.push(deps) → effect → deps（cleanup 时用）
    deps.add(activeEffect);
    activeEffect.deps.push(deps);
}
```

> **同一个 key 多次访问**：deps 已在 Set 中，`add` 是幂等的，`deps.length` 会增长（因为每次 track 都 push 同一个 Set 引用）。cleanup 时同一个 Set 会被重复删除，但 Set.delete 是幂等的，不影响正确性。

### 2.3 触发 track 的地方

**Proxy get 拦截器**中调用 `track`：

```javascript
// packages/reactivity/src/baseHandlers.ts
get(target, key, receiver) {
    track(target, key)
    const res = Reflect.get(target, key, receiver)
    // 如果是对象，递归代理（深响应）
    if (isObject(res)) {
        return reactive(res)
    }
    return res
}
```

---

## 三、触发更新（trigger）

### 3.1 trigger 实现

```javascript
// packages/reactivity/src/effect.ts

function trigger(target, key, type) {
    const depsMap = bucket.get(target);
    if (!depsMap) return;

    const effects = depsMap.get(key);
    if (effects) {
        const effectsToRun = new Set(effects);
        effectsToRun.forEach((effect) => {
            // 避免同 effect 递归触发（读写在同一个 effect）
            if (effect === activeEffect) return;
            // 有 scheduler → 由 scheduler 决定何时执行
            // 无 scheduler → 直接执行
            if (effect.options.scheduler) {
                effect.options.scheduler(effect);
            } else {
                effect();
            }
        });
    }
}
```

### 3.2 操作类型（TriggerOpTypes）

```javascript
// 数组 push/pop 会触发两种不同的 trigger
const TriggerOpTypes = {
    SET: 'set',         // 修改已有属性（对应 Object.setPrototypeOf）
    ADD: 'add',         // 新增属性（对应 Proxy [[DefineOwnProperty]]）
    DELETE: 'delete',   // 删除属性
    CLEAR: 'clear'     // 整个对象被替换
}

// 在 Proxy set 拦截器中：
set(target, key, newVal, receiver) {
    const type = Object.prototype.hasOwnProperty.call(target, key)
        ? TriggerOpTypes.SET
        : TriggerOpTypes.ADD
    const res = Reflect.set(...)
    if (res) {
        trigger(target, key, type)
    }
    return res
}
```

### 3.3 三个坑的解决方案

| 坑               | 原因                             | 解决方案                         |
| ---------------- | -------------------------------- | -------------------------------- |
| forEach 无限循环 | Set 遍历中 delete+add 会重复访问 | `new Set(effects)` 复制后遍历    |
| 同 effect 递归   | 读写在同一个 effect 里           | `effect === activeEffect` 时跳过 |
| 分支切换遗留     | 老依赖没清除                     | 每次 effect 执行前 `cleanup()`   |

---

## 四、计算属性（computed）

### 4.1 核心需求

- **惰性求值**：不立即计算，第一次 .value 时才执行
- **缓存**：依赖不变时返回缓存，不重算
- **依赖追踪**：嵌套在 effect 中时正确收集依赖

### 4.2 完整实现

```javascript
// packages/reactivity/src/computed.ts

class ComputedRefImpl {
    _value = undefined; // 缓存值，显式声明
    effect = null; // 内部 effect，显式声明
    _dirty = true; // 脏标记

    constructor(getter, options) {
        this.effect = effect(getter, {
            lazy: true, // 惰性：不立即执行
            scheduler: () => {
                // 响应式数据变化 → 标记为脏
                if (!this._dirty) {
                    this._dirty = true;
                    // 通知 computed 的依赖方（watch 等）需要更新
                    trigger(this, "value", TriggerOpTypes.SET);
                }
            },
        });
    }

    get value() {
        // 读取时也要 track（让 computed 被外层 effect 依赖）
        trackRefValue(this);
        // 如果是脏的，重新计算
        if (this._dirty) {
            this._value = this.effect();
            this._dirty = false;
        }
        return this._value;
    }
}

function computed(getter, options) {
    return new ComputedRefImpl(getter, options);
}
```

### 4.3 工作流程

```
首次读取 .value
  → _dirty=true → 执行 effect() → 结果缓存 → _dirty=false

依赖的响应式数据变化
  → trigger → scheduler → _dirty=true
  （注意：此时不执行 effect，只标记脏）

下次读取 .value
  → _dirty=true → 重新计算 effect()
```

### 4.4 computed 嵌套（嵌套 computed）

```javascript
const count = ref(1);
const double = computed(() => count.value * 2);
const triple = computed(() => double.value * 3);

count.value = 2;
// double 的 scheduler 触发 → double._dirty = true
// triple 的 scheduler 触发 → triple._dirty = true
// 读取 triple.value 时，先算 double（也是脏的，先算 count），再算 triple
```

---

## 五、ref

### 5.1 ref 原理

原始值（string/number）无法被 Proxy 代理，需要包装成对象：

```javascript
// packages/reactivity/src/ref.ts

class RefImpl {
    _rawValue = undefined;
    _value = undefined;
    dep = null; // 专门给 ref 自己的依赖集合

    constructor(value) {
        this._rawValue = value;
        // 如果是对象，走 reactive 路径（深响应）
        this._value = isObject(value) ? reactive(value) : value;
        this.dep = new Set();
    }

    get value() {
        trackRefValue(this); // 让 ref 被外层 effect 追踪
        return this._value;
    }

    set value(newVal) {
        if (hasChanged(newVal, this._rawValue)) {
            this._rawValue = newVal;
            this._value = isObject(newVal) ? reactive(newVal) : newVal;
            triggerRefValue(this); // 触发更新
        }
    }
}

function ref(value) {
    return new RefImpl(value);
}

function trackRefValue(ref) {
    if (activeEffect) {
        ref.dep.add(activeEffect);
        activeEffect.deps.push(ref.dep);
    }
}

function triggerRefValue(ref) {
    const dep = ref.dep;
    if (dep) {
        triggerEffects(dep);
    }
}
```

### 5.2 toRef / toRefs（防止解构丢失响应式）

```javascript
function toRef(obj, key) {
    return {
        get value() {
            return obj[key];
        },
        set value(v) {
            obj[key] = v;
        },
    };
}

function toRefs(obj) {
    const result = {};
    for (const key in obj) {
        result[key] = toRef(obj, key);
    }
    return result;
}
```

解构后仍保持响应式的原因：toRef 返回的对象在 get/set 时**直接代理到原响应式对象**，没有脱离 Proxy 拦截。

### 5.3 proxyRefs（模板自动脱 ref）

模板中 `{{ count }}` 不需要写 `.value`，因为组件代理会拦截属性访问，自动解包 ref：

```javascript
// 模板访问 this.count 时：
// proxy.get → resolve → { count: ref.value } → 自动返回 .value
```

---

## 六、watch

### 6.1 watch 本质

watch 是对 effect 的**二次封装**：创建一个 lazy effect，在 scheduler 中调用用户回调。

### 6.2 完整实现（包含 onInvalidate）

```javascript
// packages/runtime-core/src/apiWatch.ts

function watch(source, cb, options = {}) {
    let getter;
    if (typeof source === "function") {
        getter = source;
    } else {
        // 非函数 → 深度遍历响应式对象，建立依赖
        getter = () => traverse(source);
    }

    let oldValue;
    let newValue;

    const job = () => {
        // scheduler 触发 → 重新执行 getter 获取新值
        newValue = effectFn();
        // 调用用户回调
        cb(newValue, oldValue);
        // 更新旧值，供下次使用
        oldValue = newValue;
    };

    const effectFn = effect(getter, {
        lazy: true,
        scheduler: () => {
            // 异步批量：微任务队列中执行
            queueJob(job);
        },
    });

    if (options.immediate) {
        // 立即执行一次，回调的 oldValue 为 undefined
        job();
    } else {
        // 延迟执行，获取初始值
        oldValue = effectFn();
    }

    // 返回停止函数
    return () => {
        effectFn.active = false;
        effectFn.deps.length = 0;
    };
}
```

### 6.3 过期的副作用（onInvalidate）

解决竞态问题：

```javascript
watch(obj, async (newVal, oldVal, onInvalidate) => {
    // 注册过期回调：每次 watch 重新执行时先调用它
    let expired = false;
    onInvalidate(() => {
        expired = true;
    });

    const res = await fetch("/api/" + newVal);
    if (!expired) {
        data = res; // 只在未过期时采纳结果
    }
});

// 时序：
// 1. watch 触发 → 注册 invalidate1 → fetch A 发出
// 2. watch 再次触发 → 注册 invalidate2（清除 invalidate1）
// 3. fetch B 返回 → expired=false → 采纳
// 4. fetch A 返回 → expired=true → 丢弃
```

### 6.4 调度时机（flush）

| flush         | 时机                                   |
| ------------- | -------------------------------------- |
| `sync`        | 同步执行，响应式数据变化后立即执行回调 |
| `pre`（默认） | 微任务队列，DOM 更新之前执行           |
| `post`        | 微任务队列，DOM 更新之后执行           |

```javascript
scheduler: () => {
    if (options.flush === "post") {
        queuePostRenderEffect(job); // DOM 更新后
    } else if (options.flush === "sync") {
        job(); // 同步
    } else {
        queueJob(job); // 默认 pre
    }
};
```

### 6.5 traverse（深度监听）

```javascript
function traverse(source, seen = new Set()) {
    if (!isObject(source) || seen.has(source)) {
        return source;
    }
    seen.add(source);
    for (const key in source) {
        traverse(source[key], seen); // 递归访问每个属性，建立依赖
    }
    return source;
}
```

---

## 七、reactive / shallowReactive / readonly

### 7.1 深响应（reactive）

```javascript
// packages/reactivity/src/baseHandlers.ts

const mutableHandlers = {
    //  receiver 让代理中的 getter/setter 的 this 绑定到实际调用者，而不是原始目标对象。
    get(target, key, receiver) {
        track(target, key);
        const res = Reflect.get(target, key, receiver);
        // 深响应：访问到的对象也递归代理
        if (isObject(res)) {
            return reactive(res);
        }
        return res;
    },
    set(target, key, newVal, receiver) {
        // 判断 key 是不是 target 对象自己拥有的属性（不是继承来的）
        const type = Object.prototype.hasOwnProperty.call(target, key)
            ? TriggerOpTypes.SET
            : TriggerOpTypes.ADD;
        const res = Reflect.set(target, key, newVal, receiver);
        if (res) {
            trigger(target, key, type);
        }
        return res;
    },
    deleteProperty(target, key) {
        const hadKey = Object.prototype.hasOwnProperty.call(target, key);
        const res = Reflect.deleteProperty(target, key);
        if (res && hadKey) {
            trigger(target, key, TriggerOpTypes.DELETE);
        }
        return res;
    },
};

function reactive(obj) {
    return new Proxy(obj, mutableHandlers);
}
```

### 7.2 浅响应（shallowReactive）

```javascript
// 区别：get 中不递归代理
const shallowHandlers = {
    get(target, key, receiver) {
        track(target, key);
        return Reflect.get(target, key, receiver); // 不做 isObject 判断
    },
    // set 同 mutableHandlers
};
```

### 7.3 readonly

```javascript
// 任何写入操作都报警告
const readonlyHandlers = {
    get(target, key, receiver) {
        track(target, key);
        return Reflect.get(target, key, receiver);
    },
    set(target, key) {
        console.warn("Readonly object cannot be modified");
        return true; // 返回 true 表示 set 成功（但实际没生效）
    },
    deleteProperty(target, key) {
        console.warn("Readonly object cannot be deleted");
        return true;
    },
};
```

---

## 八、响应式 API 全景

```
reactive(obj)      Proxy 代理整个对象，深响应
shallowReactive    只代理第一层，浅响应
readonly           只读代理，写入报警告

ref(value)         包装原始值为 { value }
  └─ ref(inner)    自动深响应

computed(fn)       惰性求值 + 脏标记缓存

watch(source, cb)  监听响应式数据变化
  ├─ immediate     创建时立即执行
  ├─ flush         控制时机 pre/post/sync
  └─ onInvalidate  竞态处理

effect(fn)         注册副作用，自动追踪依赖
  └─ scheduler    自定义调度器

toRef/toRefs       保持解构后响应式
proxyRefs          模板中自动脱 ref
traverse           深度遍历建立依赖
```

---

## 九、关键设计思想

1. **WeakMap 桶**：key 是原始对象引用，无引用时 GC 自动回收，不泄漏内存。

2. **cleanup 解决分支残留**：每次 effect 执行前清除旧联系，重新建立新联系。

3. **scheduler 解耦 trigger 与执行**：trigger 时调用 scheduler，把调度权交给用户（computed 标记 dirty、watch 批量执行）。

4. **lazy + scheduler 实现 computed**：effect 设为 lazy 后只有手动调用才执行；scheduler 标记 dirty，惰性地在 .value 读取时重算。

5. **Proxy 拦截一切访问**：任何对响应式对象的 get/set/delete 都被拦截，在 get 中 track，在 set/delete 中 trigger。

6. **双向记录**：`key → Set<effect>`（trigger 时精确查找）和 `effect → deps[]`（cleanup 时清除所有联系）同时建立。
