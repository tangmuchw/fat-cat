# BasicPackingType 基本包装类型

> 为了便于操作基本类型值，ECMAScript 提供了 3 个特殊的引用类型：Boolean, Number 和 String。

- 实际上，每当读取一个基本类型值的时候，后台就会创建一个对应的基本包装类型的对象

## 举个例子

> 在读取模式下访问字符串时，后台都会自动完成下列处理：

- 创建 String 类型的一个实例
- 在实例上调用指定的方法
- 销毁这个实例

```JavaScript
var s1 = 'hello'
var s2 = s1.substring(2)

```

```JavaScript
var s1 = new String('hello')
var s2 = s1.substring(2)
s1 = null


```
