# AJAX 介绍

AJAX 全称为 Asynchronous JavaScript And XML，就是异步的 JS 和 XML。
通过 AJAX 可以在浏览器中向服务器发送异步请求，最大的优势：**无刷新获取数据**

## XML 介绍

-   XML 可扩展标记语言，被设计用来传输和存储数据。
-   XML 和 HTML 类似，不同的是 HTML 中都是预定义标签，而 XML 中没有预定义标签，全都是自定义标签，用来表示一些数据。比如说我有一个学生数据：name = “xxx” ; age = 18 ; gender = “男”

```xml
//用 XML 表示：
<student>
	<name>xxx</name>
	<age>18</age>
	<gender>男</gender>
</student>
```

**现已经被 JSON 取代**

## 核心对象

XMLHttpRequest，AJAX 的所有操作都是通过该对象进行的。
