# 盒模型介绍

> CSS3 中的盒模型有以下两种：标准盒模型、IE（替代）盒模型

- 两种盒子模型都是由 content + padding + border + margin 构成
- 盒子内容宽/高度计算范围不同
  - 标准盒模型：只包含 content
  - IE 盒模型：content + padding + border
- 可以通过 <code>box-sizing</code> 来该改变元素的盒模型
  - <code>box-sizing: content-box</code>：标准盒模型（默认值）
  - <code>box-sizing: border-box</code>：IE 盒模型
