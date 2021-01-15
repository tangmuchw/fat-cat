# 媒体查询属性 @media

> @media 可以针对不同的屏幕尺寸设置不同的样式，特别是如果你需要设置设计响应式的页面，@media 是非常有用的。

```CSS
// 如果文档宽度小于 300 像素则修改背景颜色(background-color):
@media screen and (max-width: 300px) {
    body {
        background-color: red;
    }
}
```
