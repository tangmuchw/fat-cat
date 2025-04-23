# JavaScript 高级程序设计（第 4 版）

[toc]

## 标签位置

```Html

<!DOCTYPE html>
<html>
 <head>
 <title>Example HTML Page</title>
 <script src="example1.js"></script>
 <script src="example2.js"></script>
 </head>
 <body>
 <!-- 这里是页面内容 -->
 </body>
</html>
```

这样的做法把所有 JavaScript 文件都放在<head>里，也就意味着必须把所有 JavaScript 代码都下载、解析和解释完成后，才能开始渲染页面（页面在浏览器解析到<body>的起始标签时开始渲染）。
对于需要很多 JavaScript 的页面，这会导致页面渲染的明显延迟，在此期间浏览器窗口完全空白。

```Html
<!DOCTYPE html>
<html>
 <head>
 <title>Example HTML Page</title>
 </head>
 <body>
 <!-- 这里是页面内容 -->
 <script src="example1.js"></script>
 <script src="example2.js"></script>
 </body>
</html>
```

现代 Web 应用程序通常将所有 JavaScript 引用放在<body>元素中的页面内容后面。用户会感觉页面加载更快了，因为浏览器显示空白页面的时间短了。

## 推迟执行脚本

HTML 4.01 为<script>元素定义了一个叫 defer 的属性。这个属性表示脚本在执行的时候不会改
变页面的结构。也就是说，脚本会被延迟到整个页面都解析完毕后再运行。因此，在<script>元素上
设置 defer 属性，相当于告诉浏览器立即下载，但延迟执行。

```Html
<!DOCTYPE html>
<html>
 <head>
 <title>Example HTML Page</title>
 <script defer src="example1.js"></script>
 <script defer src="example2.js"></script>
 </head>
 <body>
 <!-- 这里是页面内容 -->
 </body>
</html>

```
