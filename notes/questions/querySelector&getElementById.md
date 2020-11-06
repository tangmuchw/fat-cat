# querySelector&getElementById

> document.getElementById：返回一个匹配特定 ID 的元素。由于元素的 ID 在大部分情况下要求是独一无二的，这个方法自然而然地成为了一个高效查找特定元素的方法

> document.querySelector：返回文档中与指定选择器或选择器组匹配的第一个 HTMLElement 对象。如果找不到匹配项，则返回 null

- 匹配是使用**深度优先先序**遍历，从文档标记中的第一个元素开始，并按子节点的顺序依次遍历

## 区别

- getElement(s)ByXXX 获取的是**动态集合**，会随着 dom 结构的变化而变化
- querySelector 获取的是**静态集合**
