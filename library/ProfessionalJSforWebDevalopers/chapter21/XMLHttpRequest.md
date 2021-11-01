[toc]

# XMLHttpRequest 对象

## 响应的数据

- responseText: 作为响应主体被返回的文本
- responseXML: 如果响应的内容类型是'text/xml'或'application/xml'，这个属性中将保存包含着响应数据的 XML DOM 文档
- status: 响应的 HTTP 状态
- statusText: HTTP 状态的说明

## XHR 对象的 readyState 属性

> 该属性表示请求/响应过程的当前活动阶段

- 0: 未初始化。尚未调用 open() 方法
- 1: 启动。已经调用 open() 方法，但尚未调用 send() 方法
- 2: 发送。已经调用 send() 方法，但尚未接收到响应
- 3: 接收。已经接收到部分响应数据
- 4: 完成。已经接收到全部响应数据。而且已经可以在客户端使用了

```JavaScript
var xhr = new XMLHttpRequest() // IE => ActiveXObject

// 前端设置是否带cookie
xhr.withCredentials = true;

xhr.open('get', 'example.txt', true) // 第三个参数表示是否异步发送请求

xhr.setRequestHeader('MyHeader','MyValue')

xhr.send(null) // send() 接收一个参数，即要作为请求主体发送的数据

xhr.onreadystatechange = function(){
    if(xhr.readyState == 4) {
        if((xhr.status >=200 && xhr.status < 300) || xhr.status == 304) {
            // TODO: do something
            console.log(xhr.responseText)
        } else {
            console.error('Request was unsuccessful: ' + xhr.status)
        }
    }
}

```
