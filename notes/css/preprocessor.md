# CSS 预处理器

## SASS

> SASS（Syntactically Awesome Style Sheets）是最早的 CSS 预处理器之一，它最初采用了一种基于缩进的语法风格，称为 SASS 语法。

### 核心特性：

-   变量：用于存储颜色、尺寸等常量，减少代码冗余，提高代码可维护性。
-   嵌套规则：使 CSS 选择器的书写更加直观和紧凑，便于管理和维护。
-   混合：类似于函数，允许重用代码片段，增强代码复用性。

```SASS
@mixin box-shadow($shadow) {
  -webkit-box-shadow: $shadow;
          box-shadow: $shadow;
}
```

-   函数：提供内置函数，如颜色处理、数学运算等，支持自定义函数，增加代码的动态性。

```SASS
// 使用内置函数
$light-blue: lighten(blue, 20%);

// 自定义函数
@function addPadding($val) {
  @return $val + $val / 2;
}

// 使用自定义函数
.container {
  padding: addPadding(10px);
}


```

### 适用场景：

SASS 适用于注重代码整洁度和一致性的项目，尤其在团队开发中，统一的代码风格尤为重要。

## SCSS

> SCSS（Sassy CSS）是 SASS 语法的一种扩展，它采用了与 CSS 相同的语法结构，即使用花括号和分号。

### 核心特性：

-   兼容 CSS：SCSS 保留了 CSS 的所有特性，开发者可以逐步将 CSS 迁移到 SCSS
-   强大的功能集：继承了 SASS 的所有高级特性，如变量、嵌套、混合等。

## LESS

> **LESS（Leaner CSS）是一种动态样式语言，它引入了变量、嵌套、操作符等概念**，使得 CSS 变得更为强大和灵活。LESS 的设计哲学是“CSS with powers”，它旨在让 CSS 更易于管理，同时保持其原有的简单性

### 核心特性：

-   动态特性：变量、嵌套、操作符、函数等使得 LESS 能够处理更复杂的样式逻辑。
-   扩展性：支持函数和自定义操作，允许开发者扩展 LESS 的功能。

#### 变量

```LESS
// 定义变量
@primary-color: #ff4757;
@base-font-size: 16px;

// 使用变量
body {
  background-color: @primary-color;
  font-size: @base-font-size;
}

```

#### 操作符

LESS 支持操作符，如加、减、乘、除和百分比，用于执行数值运算，这在处理尺寸和颜色变化时特别有用。

```LESS
// 使用操作符
.container {
  padding: (@base-font-size * 1.5);
}
```

#### 自定义操作

LESS 还支持自定义操作，允许你创建更复杂的逻辑处理。

```LESS
// 自定义操作
.multiply(@a, @b) {
  @result: (@a * @b);
  .return(@result);
}

// 使用自定义操作
.container {
  width: .multiply(100%, 0.8);
}
```

### 适用场景：

LESS 适用于需要快速迭代和频繁修改样式的项目，其简单的语法和动态特性使其成为原型设计和敏捷开发的理想选择。

## Stylus

> Stylus 是一种语法更为自由和灵活的 CSS 预处理器，它简化了 CSS 的书写方式，去除了许多不必要的符号，如分号和括号，使代码看起来更自然，更易于阅读和编写。

### 核心特性：

-   简洁语法：Stylus 的语法更为宽松，减少了代码的繁琐感。

```Stylus
// 简洁的变量定义和使用
primaryColor = #ff4757
baseFontSize = 16px

body
  backgroundColor primaryColor
  fontSize baseFontSize

// 嵌套规则
.container
  width 100%
  .content
    padding 10px
    &:hover
      backgroundColor darken(primaryColor, 10%)

// 没有花括号和分号，代码更加简洁
```

-   动态特性：支持 JavaScript 表达式，允许在样式中进行更复杂的逻辑处理。

```Stylus
// 使用JavaScript表达式计算宽度
.container
  width (100 / 2)%

// 条件判断
button
  backgroundColor if (isDarkTheme, '#333', '#ccc')

// 循环生成样式
colors = ['red', 'green', 'blue']
each color, index in colors
  .box(index)
    backgroundColor color

// 使用函数
addPadding (val)
  padding val + val / 2

.container
  addPadding(10px)

// JavaScript函数
isDarkTheme = ->
  return window.matchMedia('(prefers-color-scheme: dark)').matches

// 在Stylus中调用JavaScript函数
body
  backgroundColor if isDarkTheme(), '#000', '#fff'
```

### 适用场景：

Stylus 适合那些追求极简主义和高度定制化的项目，对于喜欢探索新语法和编写富有表现力的代码的开发者来说，Stylus 是一个极具吸引力的选择。

## Scss

> scss 即为 Sass 的其中一种语法格式，支持定义变量、嵌套、混合等功能

Scss：

-   完全兼容 CSS 语法（所有有效的 CSS 都是有效的 SCSS）
-   使用.scss 文件扩展名
-   保留了 CSS 的大括号和分号结构
-   在 CSS 基础上添加了变量、嵌套、混合等高级功能
˜