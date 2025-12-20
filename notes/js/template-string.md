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
