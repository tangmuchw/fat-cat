# 跨域的几种方式

## 什么是跨域

> 跨域就是当在页面上发送 ajax 请求时，由于浏览器同源策略的限制，要求当前页面和服务端必须同源，也就是协议、域名和端口号必须一致。

## JSONP 方式解决跨域

> jsonp 的原理就是利用了 script 标签不受浏览器同源策略的限制，然后和后端一起配合来解决跨域问题的。

```JavaScript
// 客户端代码
<script>
    // 封装一个jsonp函数
    function jsonp({ url, params, callback }) {
        return new Promise((resolve, reject) => {
            // 定义回调函数
            window[callback] = function(data) {
                resolve(data)
            }

            // 创建script标签
            const script = document.createElement('script')
            params = {...params, callback}
            const arr = []
            for(const key in params) {
                if(params.hasOwnProperty(key)) {
                    // 判断当前key是否是params对象自身的属性，有可能会是原型上的属性，所以需要判断一下
                    arr.push(`${key}=${params[key]}`)
                }
            }
            url += `?${arr.join('&')}` // 拼接参数
            script.async = true
            script.src = url
            document.body.appendChild(script)
            script.onload = () => {
                document.body.removeChild(script)
            }
        })
    }
    // 使用jsonp
    jsonp({
        url: 'http://xxx/user',
        params:{ id: '1' },
        callback: 'getUserData'
    }).then(res => {
        console.log('res:', res)
    })
</script>

// 服务器端代码， node
const http = require('http')
const url = require('url')

// 创建server
const server = http.createServer()
// 监听http请求
server.on('request', (req, res) => {
    // 获取客户端传来的回调函数名称
    const  {callback } = url.parse(req.url, true).query
    const user = { // 模拟返回数据
        id: 1,
        name: 'zhangsan',
        age: 12
    }
    // 把数据和回调函数名称拼接成函数调用的方式返回
    const result = `${callback}(${JSON.stringify(user)})`
    res.end(result)
})

// 设置监听端口
server.listen(8081, function() {
    console.log('server is running on 8081 port！')
})


```

## CORS 方式解决跨域

> cors 是跨域资源共享，是一种基于 HTTP 头的机制，该机制通过允许服务器标示除了它自己以外的其它 origin（域，协议和端口），使得浏览器允许这些 origin 访问加载自己的资源。服务端设置了 Access-Control-Allow-Origin 就开启了 CORS

## Nginx 反向代理解决跨域

> nginx 通过反向代理解决跨域也是利用了服务器请求服务器不受浏览器同源策略的限制实现的。

## postMessage 方式解决跨域

> 使用 postMessage 向其它窗口发送数据的时候需要注意的就是，应该始终指定精确的目标 origin，而不是 \*，使用 window 监听 message 事件，接收其他网站发送的 message 时，请始终使用 origin 和 source 属性验证发件人的身份。

## Websocket 方式解决跨域

> 使用 Websocket 也可以解决跨域问题，因为 WebSocket 本身不存在跨域问题，所以我们可以利用 webSocket 来进行非同源之间的通信
> WebSocket 规范定义了一个在 Web 浏览器和服务器之间建立“套接字”连接的 API。 简单来说：客户端和服务器之间存在持久连接，双方可以随时开始发送数据。
