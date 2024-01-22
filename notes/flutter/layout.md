# 布局（Layout）过程

> 在进行布局的时候，Flutter 会以 DFS（深度优先遍历）方式遍历渲染树，并 **将限制以自上而下的方式** 从父节点传递给子节点。子节点若要确定自己的大小，则 必须 **遵循父节点传递的限制**。子节点的响应方式是在父节点建立的约束内 **将大小以自下而上的方式** 传递给父节点。

> Layout（布局）过程主要是确定每一个组件的布局信息（大小和位置），Flutter 的布局过程如下：

-   父节点向子节点传递约束（constraints）信息，限制子节点的最大和最小宽高
-   子节点根据约束信息确定自己的大小（size）

-   父节点根据特定布局规则（不同布局组件会有不同的布局算法）确定每一个子节点在父节点布局空间中的位置，用偏移 offset 表示
-   递归整个过程，确定出每一个节点的大小和位置

    > 可以看到，组件的大小是由自身决定的，而组件的位置是由父组件决定的

## 重新布局的边界节点-relayoutBoundary

> 一个组件是否是 relayoutBoundary 的条件是什么呢？这里有一个原则和四个场景，原则是“组件自身的大小变化不会影响父组件”，如果一个组件满足以下四种情况之一，则它便是 relayoutBoundary ：

-   当前组件父组件的大小不依赖当前组件大小时；这种情况下父组件在布局时会调用子组件布局函数时并会给子组件传递一个 parentUsesSize 参数，该参数为 false 时表示父组件的布局算法不会依赖子组件的大小。
-   组件的大小只取决于父组件传递的约束，而不会依赖后代组件的大小。这样的话后代组件的大小变化就不会影响自身的大小了，这种情况组件的 sizedByParent 属性必须为 true。
-   父组件传递给自身的约束是一个严格约束（固定宽高，下面会讲）；这种情况下即使自身的大小依赖后代元素，但也不会影响父组件。
-   组件为根组件；Flutter 应用的根组件是 RenderView，它的默认大小是当前设备屏幕大小

## Flutter 的渲染模型

> Flutter 通过绕过系统 UI 组件库，使用自己的 widget 内容集，削减了抽象层的开销。用于绘制 Flutter 图像内容的 Dart 代码被编译为机器码，并使用 Skia 进行渲染。 Flutter 同时也嵌入了自己的 Skia 副本（未来会迁移到 Impeller），让开发者能在设备未更新到最新的系统时，也能跟进升级自己的应用，保证稳定性并提升性能。

## 从用户操作到 GPU

-   User input: Responses to input gestures(keyboard, touchscreen, etc.)
-   Animation: User interface changes triggered by the tick of a timer
-   Build: App code that creates widgets on the screen
-   Rendering
    -   Layout: Positioning and sizing elements on the screen
    -   Paint: Converting elements into a visual representation(将元素转换为可视表示形式)
    -   Composition(构成): Overlaying visual elements in draw order(按绘制顺序叠加视觉元素)
-   Rasterize(栅格化): Translating output into GPU render instructions(将输出转换为 GPU 渲染指令)
