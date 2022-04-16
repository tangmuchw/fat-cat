# BFC

> BFC, Block Formatting Context, 即格式化上下文。是 web 中盒模型布局的 css 渲染模式，指一个独立的渲染区或说是一个隔离的独立容器，**用于决定块级盒的布局以及浮动相互影响范围的一个区域**

## 形成 BFC 的条件

- 浮动元素。float 除 none 以外的值
- 定位元素。position
- display 为以下其中之一的值 inline-block，table-cell，table-caption
- overflow 除了 visible 以外的值（hidden，auto，scroll）

## BFC 的特性

- 1.内部的 Box 会在垂直方向上一个接一个的放置
- 2.垂直方向的距离由 margin 决定：即在常规文档流中，两个兄弟盒子之间的垂直距离是由他们的外边距所决定的，但不是他们的两个外边距之和，而是以较大的为准
- 3.计算 BFC 的高度时，浮动元素也参与计算，利用这点，可以避免高度塌陷
- 4.BFC 区域不会与 float 元素区域重叠：常见的两栏布局为例， 仅左边固定宽度且 float，右边不设宽，因此右边的宽度自适应，随浏览器窗口大小的变化而变化
- 5.BFC 就是页面上的一个独立容器，容器里面的子元素不会影响外面元素
- 6.每个元素的左 margin 值和容器的左 border 相接触

> 防止文字环绕：浮动的盒子会遮盖下面的盒子，但是下面盒子里的文字是不会被遮盖的，文字反而还会环绕浮动的盒子。这也是一个比较有趣的特性

## 创建 BFC 的方式：

- 绝对定位元素
- 行内块级元素，即 display: inline-block
- overflow 的值不为 visible
