# 文件操作

## APP 目录

-   临时目录: 使用 <code>getTemporaryDirectory()</code>获取临时目录；系统可随时清楚临时目录的文件
-   文档目录: 使用 <code>getApplicationDocumentsDirectory()</code>来获取应用程序的文档目录，改目录用于存储只有自己可以访问的文件
-   外部存储目录：使用 <code>getExternalStorageDirectory()</code> 来获取外部存储目录，不支持 IOS

## shared_preferences

> 主要的作用用于将数据**异步持久化到磁盘**。因为持久化数据只是存储到临时目录，当 app 删除时该存储的数据就是消失，web 开发时清除浏览器存储的数据也将消失。

-   [Flutter 数据存储--shared_preferences 使用详情](https://blog.csdn.net/eastWind1101/article/details/127977741)
-   [dart:io](https://api.dart.dev/stable/3.1.1/dart-io/dart-io-library.html)
