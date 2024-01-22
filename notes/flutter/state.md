# 状态管理

## 以下是管理状态的最常见的方法

-   Widget 管理自己的状态。
-   Widget 管理子 Widget 状态。
-   混合管理（父 Widget 和子 Widget 都管理状态）。

## 如何决定使用哪种管理方法？下面是官方给出的一些原则可以帮助你做决定：

-   如果状态是用户数据，如复选框的选中状态、滑块的位置，则该状态最好由父 Widget 管理。
-   如果状态是有关界面外观效果的，例如颜色、动画，那么状态最好由 Widget 本身来管理。
-   如果某一个状态是不同 Widget 共享的则最好由它们共同的父 Widget 管理。

## InheritedWidget

> 随着 widget 树层级逐渐加深，依赖树形结构上下传递状态信息会变得十分麻烦, 第三种类型的 widget —— InheritedWidget, 提供了一种从共同的祖先节点获取数据的简易方法，示例如下

MyPage

-   StudentState(extends InheritedWidget)
    -   ExamListWidget
        -   ExamWidget
        -   ExamWidget
    -   GradeWidget

现在，当 ExamWidget 或 GradeWidget 对象需要获取 StudentState 的数据时，可以直接使用以下方式：

```Dart
final studentState = StudentState.of(context);
```
