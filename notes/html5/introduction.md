# html5

-   HTML5 是 **HTML 最新的修订版本**，2014 年 10 月由万维网联盟（W3C）完成标准制定。
-   HTML5 的设计目的是**为了在移动设备上支持多媒体**。

最小的 HTML5 文档：

```html
<!DOCTYPE html>
<!-- 声明为 HTML5 文档 -->
<html>
    <head>
        <meta charset="utf-8" />
        <title>文档标题</title>
    </head>

    <body>
        文档内容......
    </body>
</html>
```

## html5 的改进

-   新元素：canvas，audio，video，source，track，article，阿斯德，details，dialog
-   新属性
-   完全支持 CSS3
-   Video 和 Audio
-   2D/3D 制图
-   本地存储
-   本地 SQL 数据
-   Web 应用

## HTML5 多媒体

使用 HTML5 你可以简单的在网页中播放 视频(video)与音频 (audio) 。

## HTML5 应用

-   本地数据存储
-   访问本地文件
-   本地 SQL 数据
-   缓存引用
-   Javascript 工作者
-   XHTMLHttpRequest 2

## HTML5 图形

使用 HTML5 你可以简单的绘制图形:

-   使用 <canvas> 元素。
-   使用内联 SVG。
-   使用 CSS3 2D 转换、CSS3 3D 转换。

## HTML5 使用 CSS3

-   新选择器
-   新属性
-   动画
-   2D/3D 转换
-   圆角
-   阴影效果
-   可下载的字体

## HTML5 表单

新表单元素, 新属性，新输入类型，自动验证。

## HTML5 拖放，地理定位

## HTML5 新的 Input 类型

-   color：主要用于选取颜色
-   date：从一个日期选择器选择一个日期
-   datetime
-   datetime-local
-   email
-   month
-   number
-   range
-   search
-   tel
-   time
-   url
-   week

## HTML5 Web 存储

-   localStorage：用于长久保存整个网站的数据，保存的数据没有过期时间，直到手动去除
-   sessionStorage：用于临时保存同一窗口(或标签页)的数据，在关闭窗口或标签页之后将会删除这些数据

## HTML5 Web SQL 数据库

Web SQL 数据库可以在最新版的 Safari, Chrome 和 Opera 浏览器中工作
以下是规范中定义的三个核心方法：

-   openDatabase：这个方法使用现有的数据库或者新建的数据库创建一个数据库对象。
-   transaction：这个方法让我们能够控制一个事务，以及基于这种情况执行提交或者回滚。
-   executeSql：这个方法用于执行实际的 SQL 查询

## HTML5 应用程序缓存

使用 HTML5，通过创建 cache manifest 文件，可以轻松地创建 web 应用的离线版本

## HTML5 Web Workers

web worker 是运行在后台的 JavaScript，不会影响页面的性能。

## HTML5 服务器发送事件(Server-Sent Events)

HTML5 服务器发送事件（server-sent event）允许网页获得来自服务器的更新

## HTML5 WebSocket

WebSocket 是 HTML5 开始提供的一种在单个 TCP 连接上进行全双工通讯的协议。

WebSocket 使得客户端和服务器之间的数据交换变得更加简单，允许服务端主动向客户端推送数据。在 WebSocket API 中，浏览器和服务器只需要完成一次握手，两者之间就直接可以创建持久性的连接，并进行双向数据传输。

在 WebSocket API 中，浏览器和服务器只需要做一个握手的动作，然后，浏览器和服务器之间就形成了一条快速通道。两者之间就直接可以数据互相传送。
