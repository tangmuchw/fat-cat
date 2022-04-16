# 经典三分栏布局（圣杯布局和双飞翼布局）

> 圣杯布局和双飞翼布局的目的：

- 三栏布局，中间一栏最先加载和渲染
- 两侧内容固定，中间内容随着宽度自适应
- 一般用于 PC 网页

## 圣杯布局和双飞翼布局的技术实现总结

- 使用 float 布局
- 两侧使用 margin 负值，以便和中间内容横向重叠
- 防止中间内容被两侧覆盖，圣杯布局用 <code>padding</code>，双飞翼布局用 <code>margin</code>

### 圣杯布局

```HTML
<div id="container" class="clearfix">
  <p class="center">中间</p>
  <p class="left">左边</p>
  <p class="right">右边</p>
</div>

```

```CSS
#container {
  padding-left: 200px;
  padding-right: 150px;
  overflow: auto;
}
#container p {
  float: left;
}
.center {
  width: 100%;
  background-color: lightcoral;
}
.left {
  width: 200px;
  /* 这里添加 position 比较重要 */
  position: relative;
  left: -200px;
  margin-left: -100%;
  background-color: lightcyan;
}
.right {
  width: 150px;
  margin-right: -150px;
  background-color: lightgreen;
}
.clearfix:after {
  content: "";
  display: table;
  clear: both;
}
```

### 双飞翼布局

```HTML
<div id="main" class="float-left">
  <div id="main-wrap">中间</div>
</div>
<div id="left" class="float-left">左边</div>
<div id="right" class="float-left">右边</div>

```

```CSS
.float-left {
  float: left;
}

#main {
  width: 100%;
  height: 200px;
  background-color: lightpink;
}

#main-wrap {
  margin: 0 190px 0 190px;
}

#left {
  width: 190px;
  height: 200px;
  background-color: lightsalmon;
  margin-left: -100%;
}

#right {
  width: 190px;
  height: 200px;
  background-color: lightskyblue;
  margin-left: -190px;
}
```
