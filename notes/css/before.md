# CSS3 利用伪元素(::before)获取标签自定义属性(data-xx)的值

```HTML
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Document</title>
    <style>
        div {
            border: 1px solid #000;
        }

        div::before {
            content: attr(data-text);   /* 伪元素经过 attr() 获取标签自定义属性的值 */
        }

    </style>
</head>
<body>
    <div data-text="aaa">我是一段文本</div>      <!-- data-text标签自定义的属性 -->
</body>
</html>
```
