# 模板字符串简单实现

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
