# Python3 网络爬虫宝典

## 爬虫程序的完整链条

-   整理需求
-   分析目标
-   发出网络请求
-   文本解析
-   数据入库和数据出库

## 库

-   网页文本解析库： BeautifulSoup、**Parsel** 和 HTMLParser
-   网络请求库：内置的 urllib 模块的 request 对象里的 urlopen，或者 Requests 库 和 Aiohttp 库。（致命爬虫框架 Scrapy）

## 标准数据类型

-   Number（数字）
-   String（字符串）
-   bool（布尔类型）
-   List（列表）
-   Tuple（元组）
-   Set（集合）
-   Dictionary（字典）

### Number

Python3 支持 int、float、bool、complex（复数）。
在 Python 3 里，只有一种整数类型 int，表示为长整型，没有 python2 中的 Long

## 渲染工具

### Pyppeteer 、 Selenium 与 Splash

> 一款支持异步的渲染工具，目前可选的有 Splash 和 Puppeteer。

-   Splash 是一款 JavaScript 渲染服务。
-   Puppeteer 是谷歌公司推出的一款基于 Node 的库，它通过 DevTools 协议来驱动 Chrome 浏览器或者 Chromium 浏览器。

Selenium 能够做到的，Puppeteer 也能够做到，例如窗口截图、生成 PDF 文件、输入文字、点击、拖放和文本提取等，而且 Puppeteer 在单位时间能够处理的任务更多，即效率更高。

> Splash 是一款基于开源的 WebKit 开发的 JavaScript 渲染服务，可以将它部署在服务器上，然后通过 Nginx 的负载均衡功能实现动态增删节点并保持高可用性。

## App 自动化工具

-   Android 调试器

Android 调试桥（Android Debug Bridge，ADB）是一款可以让计算机程序与 Android 设备通信的多功能命令行工具，也就是说，我们可以通过 ADB 操作 Android 模拟器或者真实的 Android 设备。

-   Airtest IDE

Airtest Project 是由网易游戏推出的一款跨平台的自动化测试框架，项目由 Airtest、Poco 和 Airtest IDE 三大组件构成。三大组件相互配合，使得我们可以在 Airtest IDE 中进行图形和代码混合编程。

Poco 是一款跨引擎的 UI 自动化框架，目前支持 Unity 3D、Cocos2d-x、Android 原生 App 和 Airtest IDE。通过它，我们可以操作 Android 或 iOS 智能设备中的大部分游戏和 App。操作包括点击、滑动、拖放和截屏等，另外还支持元素定位、等待元素出现和局部定位。

## 增量爬取的原理与实现

### 增量爬取的分类

-   数据增量：指的是监控并更新指定的数据，例如电商平台中商品的价格、颜色和 H 码等。
-   URL 增量：指的是只爬取“新”页面的行为。

### 增量爬取的实现原理

-   （1）向目标网页发出网络请求。
-   （2）拿到服务器响应的页面后抽取对应的内容。
-   （3）将抽取到的内容与数据库中已存储的数据进行对比。
-   （4）更新数据或不进行处理。

节省空间的占用：pybloomlive

## 分布式爬虫

> 其核心是将队列进行共享

> 分布式爬虫库：scrapy-redis

### 基于 RabbitMQ 的分布式爬虫

RabbitMQ 是一款深受工程师喜爱的消息中间件，它是基于 Erlang 语言开发的。很多高级爬虫工程师都会将消息中间件加入分布式爬虫的设计中，因为它能让整个架构变得更清晰可控。

## Python Readability

> Readability 是一款网页净化产品，它的主要作用是清除网页正文周围那些“混乱”的内容，帮助人们将精力聚焦在有价值的内容上。

网页提取：readability-lxml => GeneralNewsExtractor = install gne

## 爬虫部署平台 Scrapyd

-   pip install scrapy
-   scrapy startproject [project_name]

## 定时工具

APScheduler 的全称是 Advanced Python Scheduler。APScheduler 能够让任务延时执行或定时执行，还可以根据需求随时添加或删除指定的任务。它还允许将任务存储在数据库中，不会因为程序异常而丢失任务。

### Crontab 命令设置周期性指令

Crontab 的时间格式默认占 5 位：
·第 1 位代表第 N 分钟，范围限定正整数 0~59
·第 2 位代表第 N 小时，范围限定正整数 0~23
·第 3 位代表这个月的第 N 天，范围限定正整数 1~31
·第 4 位代表第 N 月，范围限定正整数 1~12
·第 5 位代表这个星期的第 N 天，范围限定正整数 0 ～ 6 或星期数的简写，其中 Sunday 可用 0 或 7 表示。

## Python 语言 Web 框架

-   Django
-   Flask
-   Tornado
