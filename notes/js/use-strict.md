# 严格模式

> JavaScript 严格模式（strict mode）即在严格的条件下运行

-   严格模式通过在脚本或函数的头部添加 use strict; 表达式来声明
-   严格模式下，this 的值为 undefined

## 为什么使用严格模式:

-   消除 Javascript 语法的一些不合理、不严谨之处，减少一些怪异行为。
-   消除代码运行的一些不安全之处，保证代码运行的安全。
-   提高编译器效率，增加运行速度。
-   为未来新版本的 Javascript 做好铺垫。

## 严格模式的限制

-   不允许使用未声明的变量

```Javascript
"use strict";
x = 3.14;                // 报错 (x 未定义)
```

-   不允许删除变量或对象或函数

```Javascript
"use strict";
var x = 3.14;
delete x; // 报错
```

-   不允许变量重名
-   不允许使用八进制
-   不允许使用转义字符
-   不允许对只读属性赋值
-   不允许删除一个不允许删除的属性
-   变量名不能使用 "arguments" 字符串
-   不允许使用 with(通常被当做重复引用同一个对象中的多个属性的快捷方式，可以不需要重复引用对象本身，导致数据泄漏)
-   禁止 this 关键字指向全局对象
-   保留关键字
    -   implements
    -   interface
    -   let
    -   package
    -   private
    -   protected
    -   public
    -   static
    -   yield
