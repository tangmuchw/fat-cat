# 设计一套全站请求耗时统计工具

## 从代码层面上统计全站所有请求的耗时方式主要有以下几种

-   Performance API：Performance API 是浏览器提供的一组 API，可以用于测量网页性能。通过 Performance API，可以获取页面各个阶段的时间、资源加载时间等。其中，Performance Timing API 可以获取到每个资源的加载时间，从而计算出所有请求的耗时。

```Javascript
// 获取页面加载时间
const loadTime = window.performance.timing.loadEventEnd - window.performance.timing.navigationStart;
console.log('页面加载时间：', loadTime);

// 获取资源加载时间
const resources = window.performance.getEntriesByType('resource');
resources.forEach(resource => {
  console.log('资源URL:', resource.name);
  console.log('资源加载时间:', resource.duration);
});
```

-   XMLHttpRequest 的 load 事件：在发送 XMLHttpRequest 请求时，可以为其添加 load 事件，在请求完成时执行回调函数，从而记录请求的耗时。
-   fetch 的 Performance API：类似 XMLHttpRequest, fetch 也提供了 Performance API，可以通过 Performance API 获取请求耗时。
-   自定义封装的请求函数：可以自己封装一个请求函数，在请求开始和结束时记录时间，从而计算请求耗时。
    设计一套前端全站请求耗时统

## 设计一套前端全站请求耗时统计工具可以遵循以下步骤：

-   实现一个性能监控模块，用于记录每个请求的开始时间和结束时间，并计算耗时。
-   在应用入口处引入该模块，将每个请求的开始时间记录下来。
-   在每个请求的响应拦截器中，记录响应结束时间，并计算请求耗时。
-   将每个请求的耗时信息发送到服务端，以便进行进一步的统计和分析。
-   在服务端实现数据存储和展示，可以使用图表等方式展示请求耗时情况。
-   对于请求耗时较长的接口，可以进行优化和分析，如使用缓存、使用异步加载、优化查询语句等。

## 怎么监控页面有请求

在 JavaScript 中，可以使用 window 对象的 fetch 和 XMLHttpRequest 事件来监控页面上的网络请求。以下是监控这些请求的示例代码：

```Javascript
// 监控fetch请求
window.addEventListener('fetch', event => {
  const { request } = event;
  console.log('Fetch request made:', request.url);
});

// 监控XMLHttpRequest请求
window.addEventListener('xhr', event => {
  const { xhr } = event;
  console.log('XHR request made:', xhr.responseURL);
});
```

这些监控方法只在支持的现代浏览器中有效，并且需要在浏览器的安全上下文中使用，例如在 HTTPS 协议下。此外，这些监控方法需要浏览器的特定权限，通常只有在开发者模式下或者某些扩展程序中才能使用。

对于旧版浏览器或不支持的浏览器，可以使用代理的方式来监控网络请求，例如使用 window.XMLHttpRequest.prototype.open 方法的代理来监控

```Javascript
(function() {
  const originalOpen = window.XMLHttpRequest.prototype.open;

  window.XMLHttpRequest.prototype.open = function(method, url, async) {
    this._url = url;
    originalOpen.apply(this, arguments);
  };

  window.XMLHttpRequest.prototype.send = function() {
    console.log('XHR request made:', this._url);
    return originalSend.apply(this, arguments);
  };
})();
```

这段代码通过重写 XMLHttpRequest 对象的 open 和 send 方法，在发送请求时记录请求的 URL。这种方式可以在所有浏览器中工作，但它会影响所有的 XHR 请求，可能对现有的代码造成影响。
