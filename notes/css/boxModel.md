# 盒模型介绍

> CSS3 中的盒模型有以下两种：标准盒模型、IE（替代）盒模型

- 两种盒子模型都是由 content + padding + border + margin 构成
- 盒子内容宽/高度计算范围不同
  - 标准盒模型：只包含 content
  - IE 盒模型：content + padding + border
- 可以通过 <code>box-sizing</code> 来该改变元素的盒模型
  - <code>box-sizing: content-box</code>：标准盒模型（默认值）
  - <code>box-sizing: border-box</code>：IE 盒模型

## 块级盒子（Block box）

- 盒子会在内联的方向上扩展并占据父容器在该方向上的所有可用空间，在绝大数情况下意味着盒子会和父容器一样宽
- 每个盒子都会换行
- width 和 height 属性可以发挥作用
- 内边距（padding）, 外边距（margin） 和 边框（border） 会将其他元素从当前盒子周围“推开”

## 内联盒子（Inline box）

- 盒子不会产生换行
- width 和 height 属性将不起作用
- 垂直方向的内边距、外边距以及边框会被应用但是不会把其他处于 <code>inline</code> 状态的盒子推开
- 水平方向的内边距、外边距以及边框会被应用且会把其他处于 <code>inline</code> 状态的盒子推开
