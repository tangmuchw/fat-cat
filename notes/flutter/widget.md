# Widget 介绍

> 参考文档[Widget 介绍](https://book.flutterchina.club/chapter2/flutter_widget_intro.html#_2-2-1-widget-%E6%A6%82%E5%BF%B5)

-   @immutable: 代表 Widget 是不可变的,这会限制 Widget 中定义的属性（即配置信息）必须是不可变的（final）

## Flutter 中的四棵树

-   Flutter 框架的处理流程是这样的：

    -   根据 Widget 树生成一个 Element 树，Element 树中的节点都继承自 Element 类。
    -   根据 Element 树生成 Render 树（渲染树），渲染树中的节点都继承自 RenderObject 类。
    -   根据渲染树生成 Layer 树，然后上屏显示，Layer 树中的节点都继承自 Layer 类。

### 为什么不允许 Widget 中定义的属性变化呢？

因为，Flutter 中如果属性发生变化则会重新构建 Widget 树，即重新创建新的 Widget 实例来替换旧的 Widget 实例，所以允许 Widget 的属性变化是没有意义的，因为一旦 Widget 自己的属性变了自己就会被替换。这也是为什么 Widget 中定义的属性必须是 final 的原因

### 组件分类

-   具备 UI 属性的独立业务模块；
-   不具备 UI 属性的基础业务功能；
-   不具备业务属性的 UI 控件
-   不具备业务属性的基础功能

## Element、BuildContext 和 RenderObject

### Element

> 组件最终的 Layout、渲染都是通过 RenderObject 来完成的，从创建到渲染的大体流程是：**根据 Widget 生成 Element，然后创建相应的 RenderObject 并关联到 Element.renderObject 属性上，最后再通过 RenderObject 来完成布局排列和绘制**。
