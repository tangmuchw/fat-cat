[toc]

# 常见跨域的解决方案

> 参考 [前端常见跨域解决方案（全）](https://segmentfault.com/a/1190000011145364)

## 通过 jsonp 跨域

> 通常为了减轻 web 服务器的负载，我们把 js、css，img 等静态资源分离到另一台独立域名的服务器上，**在 html 页面中再通过相应的标签从不同域名下加载静态资源，而被浏览器允许**，基于此原理，我们可以通过动态创建 script，再请求一个带参网址实现跨域通信。

- jsonp 缺点：**只能实现 get 一种请求**

```JavaScript
    var script = document.createElement('script');
    script.type = 'text/javascript';

    // 传参一个回调函数名给后端，方便后端返回时执行这个在前端定义的回调函数
    script.src = 'http://www.xxx.com/login?user=admin&callback=handleCallback';
    document.head.appendChild(script);

    // 回调执行函数
    function handleCallback(res) {
        console.log(JSON.stringify(res));
    }

    // 服务器返回
    // handleCallback({"status": true, "user": "admin"})
```

## postMessage

### 解决一下问题

- 页面和其打开的新窗口的数据传递
- 多窗口之间消息传递
- 页面与嵌套的 iframe 消息传递
- 上面三个场景的跨域数据传递

```JavaScript
   window.postMessage(data, origin)
   window.addEventListener('message', handler, false);
```

## CORS 跨域资源共享

> 详见 [CORS](./CORS.md)

## document.domain + iframe 跨域

> 实现原理：两个页面都通过 js 强制设置 document.domain 为基础主域，就实现了同域。

- 缺点：此方案仅限主域相同，子域不同的跨域应用场景。

父窗口(http://www.xxx.com/parent.html)

```HTML
    <iframe id="iframe" src="http://child.xxx.com/child.html"></iframe>
    <script>
        document.domain = 'xxx.com';
        var user = 'me';
    </script>
```

子窗口(http://child.xxx.com/child.html)

```HTML
    <script>
        document.domain = 'xxx.com';
        // 获取父窗口中变量
        console.log('Get js data from parent =>', window.parent.user);
    </script>
```
