# flex

> flex 属性用于设置或检索弹性盒模型对象的子元素如何分配空间。
> 设为 Flex 布局以后，子元素的 float、clear 和 vertical-align 属性将会失效。
> [摘自阮一峰的网络日志-Flex 布局教程：语法篇](http://www.ruanyifeng.com/blog/2015/07/flex-grammar.html)

- display: flex;
- display: inline-flex; => 行内元素
- display: -webkit-flex; => Safari

## 基本概念

> 采用 Flex 布局的元素，称为 Flex 容器（flex container）, 简称「容器」
> 「容器」的所有子元素（儿子辈）自动成为容器成员，成为 Flex 项目（flex item），简称「项目」
> 容器默认存在两根轴：水平的主轴（main axis）和垂直的交叉轴（cross axis）

## 容器的属性

- flex-direction: row | row-reverse | column | column-reverse; // 决定主轴的方向
- flex-wrap: nowrap | wrap | wrap-reverse; // 决定项目如何换行（默认情况下，项目都排在一条线上）
- flex-flow: <flex-direction> || <flex-wrap>;
- justify-content: flex-start | flex-end | center | space-between | space-around; // 定义项目在主轴上的对其方式
- align-items: flex-start | flex-end | center | baseline | stretch; // 定义项目在交叉轴上如何对齐
- align-content: flex-start | flex-end | center | space-between | space-around | stretch; // 定义多根轴线的对齐方式。如果项目只有一根轴线，该属性不起作用

## 项目的属性

- order: <integer>; // 定义项目的排列顺序。数值越小，排列越靠前，默认为 0
- flex-grow: <number>; // 定义项目的放大比例，默认是 0，即如果存在剩余空间，也不放大。
- flex-shrink: <number>; // 定义项目的缩小比例，默认为 1, 即如果空间不足，该项目将缩小。
- flex-basis: <length> | auto; // 定义了在分配多余空间之前，项目占据主轴空间（main size）。浏览器根据这个属性，计算主轴是否有多余空间。默认值为 auto，即项目的本来大小。
- flex: none | [<'flex-grow'>, <'flex-shrink'>] | <'flex-basis'>; // none => 0 0 auto; auto => 1 1 auto
- align-self: auto | flex-start | flex-end | center | baseline | stretch; // 定义单个项目有与其他项目一样的对齐方式。默认为 auto
