# type 与 interface 的区别

## type（类型别名）

> 用来**给一个类型起新名字**。type 类型别名可以用来表示 基本类型、对象类型、联合类型、元组和交集

## interface（接口）

接口是命名 **数据结构**（例如对象）的另一种方式。与 type 不同，**interface 仅限于描述对象类型**。

## 相同点

-   都可以用来定义对象和函数
-   都可以实现继承：type 和 interface 并不互斥（interface 可以继承对象类型 type）
-   type 和 interface 都支持扩展

## 区别

-   type 侧重于直接定义类型
-   type 还可以给一个或多个类型起一个新名称（当变量用）
-   type 可以声明基本类型、元组类型（type Data = [number, string]）、联合类型
-   type 可以通过 typeof 操作符来声明
-   interface 可以声明合并，但 type 不可以，会报**重复定义**的警告
