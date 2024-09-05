# react-router 基本原理

## 前端在路由上经历的四次变化

-   1.最初的路由管理权有后端完全控制：前端页面通过在模板中插入后端语言变量的方式完成开发。这个时代最明显的技术特征是 Java 的 JSP
-   2.但当 AJAX 技术兴起后，前端网页不再与后端页面直接耦合了，工程也得以分离。这个时代最明显的特征是多个 HTML 页面，并由 Nginx 等静态文件服务完成托管，这是第二次变化。
-   3.第三次变化，在这次变化中，最明显的是 JavaScript 成为前端开发的主角，无论是 HTML、CSS 还是路由都通过 JavaScript 来控制。在这个阶段中，最具特征的技术栈是 AngularJS。通过在 Hash 中添加路由路径的方式控制前端路由，如 http://example.com#a，使得开发者的注意力得以从前端的繁杂信息中进一步收敛。
-   4.浏览器对 HTML5 中 History pushState 的支持，前端路由迎来了第四次变化。这次我们终于可以不再写 #a 这样的路由了，而是回归到最初的写法——http://example.com/a。

## 为什么 History pushState 可以办到呢？它分两部分进行

-   第一部分在**浏览器完成**，HTML5 引入了 history.pushState() 和 history.replaceState() 两个函数，它们分别可以添加和修改历史记录条目。

    -   在浏览器侧的表现行为则是：pushState 修改当前浏览器地址栏中的网址路径；
    -   replaceState 则是替换网址路径。
        > 使用 pushState 和 replaceState 时，浏览器并不会刷新当前页面，而仅仅修改网址，此时如果用户刷新页面才会重新拉取。 所以需要注意，既然http://example.com本身指向编译产出物 index.html，那么http://example.com/a 也需要指向 index.html，那就需要在服务端去配置完成

-   第二部分是在**服务端的进行配置修改**，被称为 historyApiFallback。如果你了解过 webpack 的配置，那么一定看见过 historyApiFallback，它的作用就是将所有 404 请求响应到 index.html。那么同理需要在 Nginx 或者 Node 层去配置 historyApiFallback，同样是将 404 请求响应到 index.html 就可以了

## 实践方案

> 翻开 React Router 的代码，你会发现 React Router 提供了三个库，分别是 react-router、react-router-dom 及 react-router-native。会发现 react-router 是没有 UI 层的，**react-router-dom = react-router + Dom UI**，而 **react-router-native = react-router + native UI**

在 DOM 版本中提供的基础路由是 BrowserRouter，它的源码是这样的：

```Javascript
import { Router } from "react-router";
import { createBrowserHistory as createHistory } from "history";

class BrowserRouter extends React.Component {
  history = createHistory(this.props);

  render() {
    return <Router history={this.history} children={this.props.children} />;
  }
}

```

在 React Router 中路由通过**抽象 history 库统一管理完成**，history 库支持 BrowserHistory 与 MemoryHistory 两种类型。打开源码看一下 **BrowserHistory 实际上调用的就是浏览器的 History API**。
因为 React Native 并不是运行在浏览器环境中，所以需要在内存中构建一个自己的版本，原理上就是一个数组，即 MemoryHistory

## 工作方式

### 设计模式

-   Monorepo 设计：即一个仓库对应多个工程，React Router 使用了 Monorepo 的工程架构，使工程代码对团队中的每一个人都**具备透明度**。在同一次迭代中，库之间互相引用代码也更为容易（与 Monorepo 相反，Multirepo 设计：是我们常用的开发模式，一个仓库对应一个工程，子团队自行维护）
-   Context：使用 Context API 完成数据共享

### 关键模块

从功能角度，我们可以把 React Router 的组件分为三类

-   Context 容器，分别是 Router 与 MemoryRouter，主要提供上下文消费容器
-   直接消费者，提供路由匹配功能，分别是 Route、Redirect、Switch
-   与平台关联的功能组件，分别是 react-router-dom 中的 Link、NavLink（都会转化成 a 标签，NavLink 拥有高亮显示效果的，而 link 没有） 以及 react-router-native 中的 DeepLinking

## 总结

React Router 路由的基础实现原理分为两种：

-   如果是切换 Hash 的方式，那么依靠浏览器 Hash 变化即可；
-   如果是切换网址中的 Path，就要用到 HTML5 History API 中的 pushState、replaceState 等。
    -   在使用这个方式时，还需要在服务端完成 historyApiFallback 配置。在 React Router 内部主要依靠 history 库完成，这是由 React Router 自己封装的库，为了实现跨平台运行的特性，内部提供两套基础 history，一套是直接使用浏览器的 History API，用于支持 react-router-dom；另一套是基于内存实现的版本，这是自己做的一个数组，用于支持 react-router-native。
-   React Router 的工作方式可以分为设计模式与关键模块两个部分。
    -   从设计模式的角度出发，在架构上通过 Monorepo 进行库的管理。Monorepo 具有团队间透明、迭代便利的优点。
    -   其次在整体的数据通信上使用了 Context API 完成上下文传递。
    -   在关键模块上，主要分为三类组件：
        -   第一类是 Context 容器，比如 Router 与 MemoryRouter；
        -   第二类是消费者组件，用以匹配路由，主要有 Route、Redirect(v6 版本已去掉)、Switch 等；
        -   第三类是与平台关联的功能组件，比如 Link、NavLink、DeepLinking（native） 等。
