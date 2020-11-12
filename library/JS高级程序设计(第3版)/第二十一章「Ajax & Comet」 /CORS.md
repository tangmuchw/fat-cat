[toc]

# CORS 跨域资源共享

> 默认情况下，XHR 对象只能访问与包含它的页面位于同一个域中的资源

> CORS（Cross-Origin Resource Sharing）: 其背后的基本思想，就是使用自定义的 HTTP 头部让浏览器与服务器进行沟通，从而决定请求或响应是应该成功，还是应该失败

- Access-Control-Allow-Origin

## IE 对 CORS 的实现

> 微软在 IE8 中引入了 XDR（XDomainRequest）类型。

```JavaScript
var xdr = new XDomainRequest()
xdr.onload = function(){
    // 只能访问 responseText, 没办法确定响应的 status 等信息
    console.log(xdr.responseText)
}
xdr.onerror = function(){
    // 如果响应中缺少 Access-Control-Allow-Origin 头部，也会触发 error
    console.error('An error occurred')
}
xdr.open('get', '...')
xdr.send(null)

```

### XDR 特点

- cookie 不会随请求发送, 也不会随响应返回
- 只能设置请求头部信息中的 Content-Type 字段
- 不能访问响应头部信息
- 只支持 GET 和 POST 请求

## 其他浏览器对 CORS 的实现

> Firefox 3.5+、Safari 4+、Chrome、iOS 版 Safari 和 Android 平台中的 WebKit 都通过 XMLHttpRequest 对象实现了对 CORS 的原生支持，**即要请求位于另一个域中的资源，使用标准的 XHR 对象并在 open() 方法中传入绝对 URL 即可**

### 其限制

- 不能使用 setRequestHeader() 设置自定义头部

- 不能发送和接收 cookie
- 调用 getAllResponseHeaders() 方法总会返回空字符串

## Preflighted Requests

> CORS 通过 Preflighted Requests 的透明服务器验证机制支持开发人员使用自定义的头部、GET 或 POST 之外的方法，以及不同类型的主体内容

- Origin
- Access-Control-Request-Method
- Access-Control-Request-Headers: NCZ

-----响应

- Access-Control-Allow-Origin
- Access-Control-Allow-Methods
- Access-Control-Allow-Headers
- Access-Control-Max-Age: 将这个 Preflight 请求缓存多长时间（以秒表示）

## 带凭根的请求

> 默认情况下，跨源请求不提供凭根（cookie、HTTP 认证及客户端 SSL 证明等）
> 通过将 <code>withCredentials</code> 属性设置为 <code>true</code>, 可以指定某个请求应该发送凭根。如果服务器接收凭根的请求，会用 **Access-Control-Allow-Credentials: true** 在 HTTP 头部响应

## 跨浏览器的 CORS

```JavaScript
const createCORSRequest = (method, url) => {
    let xhr = new XMLHttpRequest()

    if('widthCredentials' in xhr){
        xhr.open(method, url, true)
    } else if(typeof XDomainRequest) {
        xhr = new XDomainRequest()
        xhr.open(method, url)
    } else {
        xhr = null
    }
    return xhr
}

const rqt = createCORSRequest('get', 'url')
if(rqt){
    // onload => 用于替代 onreadystatechange 检测成功
    rqt.onload = () => {
        // 处理 rqt.responseText
    }

    rqt.send(null)
}
```
