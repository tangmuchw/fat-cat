# 模板字符串简单实现

```js
/**
 * 模板渲染（支持表达式执行）
 * @param {string} templateStr - 模板字符串
 * @param {object} data - 数据对象
 * @returns {string} 渲染后的字符串
 */

function renderTemplateWithExpr(templateStr, data) {
    // [^}]：否定字符集，表示匹配除了 } 之外的任意单个字符（包括字母、数字、符号、空格等）；
    // +：量词，表示匹配前面的字符 / 字符集1 次或多次（即不能为空）。
    const reg = /\$\{([^}]+)\}/g;

    return templateStr.replace(reg, (match, expr) => {
        expr = expr.trim();
        try {
            // 用 with 语句将 data 作为上下文，使表达式可以直接访问 data 的属性
            with (data) {
                // 执行表达式并返回结果
                return eval(expr);
            }
        } catch (e) {
            // 表达式执行错误时返回空字符串并打印错误
            console.error("表达式执行错误：", e);
            return "";
        }
    });
}

const template = "Hello ${ 'xxx${name}' }，你今年 ${age} 岁，来自 ${city}";
const data = { name: "小明", age: 18, city: "重庆" };

console.log(renderTemplateWithExpr(template, data));
/* 输出：
  姓名：小明
  明年年龄：19
  姓名大写：小明
  计算：7
*/
```

```js
function myTemplate(strings, ...values) {
    let result = "";
    console.log(values); // Array ["World"]

    for (let i = 0; i < strings.length; i++) {
        // 添加静态部分
        result += strings[i];

        // 添加动态部分（如果存在）
        if (i < values.length) {
            // 处理各种类型的值
            const value = values[i];
            if (value === null) {
                result += "null";
            } else if (value === undefined) {
                result += "undefined";
            } else {
                // 尝试调用 toString()
                try {
                    result += value.toString();
                } catch (e) {
                    result += String(value);
                }
            }
        }
    }

    return result;
}

// 使用
const name = "World";
console.log(myTemplate`Hello, ${name}!`);
```

---

## V8 引擎中模板字符串的核心实现（伪代码还原）

以下是 V8 源码中模板字符串相关逻辑的**简化伪代码**（基于 V8 源码的 `template-literal.cc`/`runtime-template-literal.cc`），帮你理解核心逻辑：

### 1. 基础模板字符串（无标签）的实现逻辑

```cpp
// V8 伪代码：处理基础模板字符串 `a${b}c`
Handle<String> EvaluateTemplateLiteral(
    Isolate* isolate,
    Handle<FixedArray> quasis,        // 静态字符串片段：["a", "c"]
    Handle<FixedArray> expressions) { // 表达式结果：[b的值]
  // 1. 计算总长度，预分配内存（性能优化）
  int total_length = 0;
  for (int i = 0; i < quasis->length(); i++) {
    total_length += Handle<String>::cast(quasis->get(i))->length();
  }
  for (int i = 0; i < expressions->length(); i++) {
    total_length += Handle<String>::cast(ToString(isolate, expressions->get(i)))->length();
  }

  // 2. 创建拼接后的字符串
  Handle<SeqOneByteString> result = factory->NewRawOneByteString(total_length);
  int pos = 0;

  // 3. 交替拼接静态片段和表达式结果
  for (int i = 0; i < quasis->length(); i++) {
    // 拼接静态片段
    Handle<String> quasi = Handle<String>::cast(quasis->get(i));
    CopyChars(result, pos, quasi);
    pos += quasi->length();

    // 拼接对应表达式（最后一个静态片段后无表达式）
    if (i < expressions->length()) {
      Handle<String> expr_str = ToString(isolate, expressions->get(i));
      CopyChars(result, pos, expr_str);
      pos += expr_str->length();
    }
  }

  return result;
}
```

### 2. 带标签的模板字符串（如 `tag`hello${name}``）的实现逻辑

带标签的模板字符串会先创建「模板对象（TemplateObject）」并缓存，再调用标签函数：

```cpp
// V8 伪代码：创建模板对象（缓存静态片段，提升性能）
Handle<JSArray> CreateTemplateObject(
    Isolate* isolate,
    Handle<FixedArray> raw_quasis,  // 原始静态片段（未转义）
    Handle<FixedArray> cooked_quasis) { // 转义后的静态片段
  // 1. 检查缓存，避免重复创建
  Handle<JSArray> cache = GetTemplateObjectCache(isolate);
  for (int i = 0; i < cache->length(); i++) {
    if (IsEqualTemplateObject(cache->get(i), raw_quasis, cooked_quasis)) {
      return Handle<JSArray>::cast(cache->get(i));
    }
  }

  // 2. 创建新的模板对象（包含 raw 和 cooked 两个属性）
  Handle<JSObject> template_obj = factory->NewJSObject();
  template_obj->SetProperty(isolate, factory->raw_string(), raw_quasis);
  template_obj->SetProperty(isolate, factory->cooked_string(), cooked_quasis);

  // 3. 存入缓存，后续复用
  cache->Add(template_obj);
  return template_obj;
}

// 调用标签函数
Handle<Object> CallTemplateTag(
    Isolate* isolate,
    Handle<Function> tag,          // 标签函数
    Handle<JSArray> template_obj,  // 模板对象
    Handle<FixedArray> expressions) { // 表达式结果
  // 构建参数：tag(template_obj, expr1, expr2, ...)
  Handle<FixedArray> args = factory->NewFixedArray(1 + expressions->length());
  args->set(0, template_obj);
  for (int i = 0; i < expressions->length(); i++) {
    args->set(i + 1, expressions->get(i));
  }

  // 调用标签函数并返回结果
  return Execution::Call(isolate, tag, isolate->global_proxy(), args);
}
```

---

## 三、和手写模拟版的核心区别

| 维度     | 手写模拟版（正则替换）         | 引擎原生实现（V8）               |
| -------- | ------------------------------ | -------------------------------- |
| 执行阶段 | 运行时                         | 编译+运行时（编译期拆分结构）    |
| 性能     | 正则匹配+多次替换，性能低      | 预计算长度+内存预分配，性能极高  |
| 功能     | 仅支持变量替换                 | 支持表达式、转义、标签函数、缓存 |
| 安全性   | 需手动处理注入（如 eval 风险） | 引擎层面隔离，无注入风险         |

---
