## JS 数据类型

- 基本类型 Number,Boolean, String, null, undefined （ES6 新增的）, BigInt（ES2020）
- 引用类型 Object
- 对象子类型 Array, Function

## Number() 的存储空间是多大？如果后台发送了一个超过最大自己的数字怎么办

- Math.pow(2, 53) ，53 为有效数字，会发生截断，等于 JS 能支持的最大数字。
