# CSS 实现自适应正方形

> margin/padding 设置百分比，其基准为其父元素的宽度。如父元素宽度为 200px，其子元素设置 padding-bottom: 50%; 相当于 padding-bottom: 100px;

```HTML
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Document</title>
    <style>
        .flex-box {
            display: flex;
        }

        .flex-box div {
                width: 25%;
                background: red;
                /* height: 100px; */
                padding-bottom: 25%;
                /* margin-top: 50%; */
                height: 0;
        }
    </style>
</head>
<body>
    <div class="flex-box">
        <div>wo</div>
        <div>wo</div>
        <div>wo</div>
        <div>wo</div>
    </div>
</body>
</html>
```
