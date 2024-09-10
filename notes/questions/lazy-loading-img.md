# 常见图片懒加载方式有哪些

-   **使用 loading 属性**：HTML 的<img>标签提供了一个 loading 属性，允许开发者指定图片的加载策略。通过设置 loading="lazy"，可以告诉浏览器延迟加载图片，直到图片进入视口（viewport）附近才开始加载。这种方式是现代且推荐的做法，因为它提供了良好的用户体验，同时减少了不必要的资源加载，从而提高了页面加载速度并减轻了服务器的负担 ‌
-   使用 IntersectionObserver API‌：这是一种更高级的技术，它允许开发者观察目标元素与视窗（viewport）的交叉状态。当元素进入视窗时，可以触发相应的操作，如加载图片。这种方法提供了更大的灵活性，但实现起来可能相对复杂一些 ‌

```Javascript
// 创建观察对象
var  observer = new IntersectionObserver(callback, options)

// 观察指定DOM对象
observer.observe( DOM对象 )
```
