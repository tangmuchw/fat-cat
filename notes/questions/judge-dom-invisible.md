# 判断 dom 元素是否滚动到底、是否在可视区域

-   clientWidth：在页面上返回内容的可视宽度（宽度包含内边距（padding），不包含边框（border），外边距（margin）和滚动条），只读属性，单位 px。（内联元素以及没有 CSS 样式的元素的 clientWidth 属性值为 0）
-   clientHeight：在页面上返回内容的可视高度（高度包含内边距（padding），不包含边框（border），外边距（margin）和滚动条）
-   offsetWidth：返回元素的宽度，包括边框（border）和内边距（padding），但不包含外边距（margin）
-   offsetHeight：返回任何一个元素的高度包括边框（border）和内边距（padding），但不包含外边距（margin）

-   offsetLeft： 是一个只读属性，返回当前元素相对于 offsetParent 节点左边界的偏移像素值（左边框到最近元素内边距的距离含滚动条）。返回值包含:

    -   元素向左偏移的像素值，元素的外边距（margin）

    -   offsetParent 元素的左侧内边距（padding）、边框（border）及滚动条

-   offsetTop：是一个只读属性，返回当前元素相对于 offsetParent 节点顶部边界的偏移像素值。返回值包含:

    -   元素顶部偏移的像素值，元素的外边距（margin）
    -   offsetParent 元素的顶部内边距（padding）、边框（border）及滚动条

-   scrollWidth：返回整个元素的宽度（包括带滚动条的隐蔽的地方）
-   scrollHeight：返回整个元素的高度（包括带滚动条的隐蔽的地方）
-   scrollTop：返回当前视图中的实际元素的顶部边缘和顶部边缘之间的距离

注： offsetParent 元素是一个指向最近的（指包含层级上的最近）包含该元素的定位元素或者最近的元素

<img src="../../img/dom_structure.png" width="100%" height="auto" style="border-radius:4px;">

## 判断 dom 元素是否滚动到底

> 当 scrollTop + clientHeight = scrollHeight，滚动到底部

## 判断 dom 元素是否在可视区域

> **getBoundingClientRect** 方法返回一个 DOMRect 对象，该对象包含了元素的位置和尺寸信息。DOMRect 对象具有 left、top、right、bottom、width、height 等属性，可以用来计算元素在视口中的位置和大小。

```Javascript
 const viewportWidth = window.innerWidth || document.documentElement.clientWidth;
 const viewportHeight = window.innerHeight || document.documentElement.clientHeight;

const rect = element.getBoundingClientRect();
 const inViewport = rect.top < viewportHeight && rect.bottom > 0 &&
   rect.left < viewportWidth && rect.right > 0;
```

-   top > 0：说明 dom 元素还没到视口的顶部
-   0 < top < clientHeight：说明 dom 元素还没到视口的顶部,但是已经在可视区域了
-   top > clientHeight：说明 dom 元素还没到视口的顶部，且不在可视区域了
-   top < 0：说明 dom 元素已经超过视口的顶部了， 要判断是否在可视区域，需要结合 bottom 值
