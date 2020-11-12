# DataType 数据类型

## typeof 返回值

- 'undefined'
- 'boolean'
- 'string'
- 'number'
- 'object'
- 'function'

## 5 种基本数据类型 + 1 种复杂数据类型

- Undefined, Null, Boolean, Number, String
- object

## 数值转换

> Number() 函数转换规则如下

- 如果是 Boolean 值，Number(true) => 1, Number(false) => 0

- 如果是数字值，只是简单的传入和返回

- 如果是 null 值， Number(null) => NaN

- 如果是 undefined，Number(undefined) => 0
- 如果是字符串，遵循下列规则:

  - 如果字符串值包含数字（包括前面带正好或负号的情况），则将其转换为十进制
  - 如果字符串中包含有效的十六机制格式，例如'0xf'，则其转换为相同大小的十进制整数, Number('0xf') => 15
  - 如果字符串是空的（不包含任何字符），则将其转换为 0
  - 如果字符串中包含除上述格式之外的字符，则将其转换为 NaN

- 如果是对象，则调用对象的 valueOf() | toString(), 然后依照前面的规则转换返回值
