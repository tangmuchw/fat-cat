# CSS 世界

[toc]

## 声明块

> 声明块是花括号（{}）包裹的一系列声明。

## 选择器

> 是用来瞄准目标元素的东西。

-   类选择器：指以“.”这个点号开头的选择器。很多元素可以应用同一个类选择器。“类”，天生就是被公用的命。
-   ID 选择器：“#”打头，权重相当高。ID 一般指向唯一元素。但是，在 CSS 中，ID 样式出现在多个不同的元素上并不会只渲染第一个，而是雨露均沾。但显然不推荐这么做。
-   属性选择器：指含有[]的选择器，形如[title]{}、[title= "css-world"]{}、[title ～="css-world"]{}、[title^="css-world"]{}和[title$="css-world"]{}等。
-   伪类选择器：一般指前面有个英文冒号（：）的选择器，如：first-child 或：last-child 等。
-   伪元素选择器：就是有连续两个冒号的选择器，如：first-line：first-letter、：before 和：after。

## 关系选择器

> 关系选择器是指根据与其他元素的关系选择元素的选择器，常见的符号有空格、>、～，还有+等，这些都是非常常用的选择器。

-   后代选择器：选择所有合乎规则的后代元素。**空格连接**。
-   相邻后代选择器：仅仅选择合乎规则的儿子元素，孙子、重孙元素忽略，因此又称“子选择器”。**>连接**。适用于 IE7 以上版本。
-   兄弟选择器：选择当前元素后面的所有合乎规则的兄弟元素。**～连接**。适用于 IE7 以上版本。
-   相邻兄弟选择器：仅仅选择当前元素相邻的那个合乎规则的兄弟元素。**+连接**。适用于 IE7 以上版本。

## @规则

> @规则指的是以@字符开始的一些规则，像@media、@font-face、@page 或者@support，诸如此类。

## 块级元素

> “块级元素”对应的英文是 block-level element，常见的块级元素有<div>、<li>和<table>等。需要注意是，“块级元素”和“display 为 block 的元素”不是一个概念。例如，<li>元素默认的 display 值是 list-item，<table>元素默认的 display 值是 table，但是它们均是“块级元素”，因为它们都符合块级元素的基本特征，也就是**一个水平流上只能单独显示一个元素，多个块级元素则换行显示**。

### display: inline-table 的盒子

> 外面是“内联盒子”，里面是“table 盒子”。得到的就是一个可以和文字在一行中显示的表格。

按钮就是 CSS 世界中极具代表性的 inline-block 元素，可谓展示“**包裹性**”最好的例子，具体表现为：**按钮文字越多宽度越宽（内部尺寸特性），但如果文字足够多，则会在容器的宽度处自动换行（自适应特性）类似只能宽度行为**。浮动元素以及绝对定位元素都具有包裹性。

例子：页面某个模块的文字内容是动态的，可能是几个字，也可能是一句话。希望文字少的时候居中显示，文字超过一行的时候居左显示。

```CSS
.box {
    text-align: center;
}

.content {
    display: inline-block;
    text-align: left;
}
```

## 内联元素

> 可以和文字在一行显示。例如 图片，按钮，输入框、下拉框等原生表单控件。

### 幽灵空白节点

> “幽灵空白节点”是内联盒模型中非常重要的一个概念，具体指的是：在 HTML5 文档声明中，内联元素的所有解析和渲染表现就如同每个行框盒子的前面有一个“空白节点”一样。这个“空白节点”永远透明，不占据任何宽度，看不见也无法通过脚本获取，就好像幽灵一样，但又确确实实地存在，表现如同文本节点一样，因此，我称之为“幽灵空白节点”。

## float

> float 属性著名的特性表现，就是会让父元素的高度塌陷。

## BFC

> BFC，block formatting context，块级格式化上下文。
> 如果一个元素具有 BFC，内部子元素再怎么翻江倒海，都不会影响外部的元素。

### 触发 BFC

-   <html> 根元素
-   float 的值不为 none
-   overflow 的值为 auto、scroll 或 hidden
-   display 的值为 table-cell、table-caption 和 inline-block 中的任何一个
-   position 的值不为 relative 和 static
