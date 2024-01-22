# Android 端动态化支持

> 环境：Flutter 3.13.0, Dart 3.1.0, DevTools 2.25.0

-   [Flutter Android 工程结构及应用层编译源码深入分析](https://cloud.tencent.com/developer/article/1864377?from=15425)
-   [深入理解 Android 之 Gradle](https://blog.csdn.net/Innost/article/details/48228651)
-   [GRADLE 构建最佳实践](http://www.figotan.org/2016/04/01/gradle-on-android-best-practise/)
-   [Gradle docs-英文版](https://docs.gradle.org/current/userguide/userguide.html?_gl=1*1sr5rit*_ga*MTYzNjQ1MTAwMC4xNjkyNzczNTY2*_ga_7W7NC6YNPT*MTY5Mzk3MjI0Mi4yLjAuMTY5Mzk3MjI0Mi42MC4wLjA.)
-   [Gradle docs-中文版](https://doc.qzxdp.cn/gradle/8.1.1/userguide/build_lifecycle.html)

## 在项目里配置 flavors

> flavors 定义编译时配置并设置在运行时读取的参数，以自定义应用程序的行为

-   android/app/build.gradle 下增加如下代码

```Dart
# 风味维度
flavorDimensions "default"

# 产品风味
productFlavors {
    free {
        dimension "default"
        resValue "string", "app_name", "free flavor example"
        applicationIdSuffix ".free"
    }
}

```

-   根目录下 创建文件 .vscode/launch.json，在 launch.json 里增加以下代码

```JSON
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "free",
      "request": "launch",
      "type": "dart",
      "program": "lib/main_development.dart",
      "args": ["--flavor", "free", "--target", "lib/main_free.dart" ]
    }
  ],
  "compounds": []
}

```

-   终端运行命令：flutter run --flavor free

## 构建和发布为 Android 应用

-   创建一个用于上传你的密钥库（正式发布需手动生成）
    -   keytool -genkey -v -keystore ~/key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias key
-   使用 R8 压缩你的代码：--no-shrink
-   检查 app manifest 文件检查位于 <app dir>/android/app/src/main 的默认 App Manifest 文件 AndroidManifest.xml，并确认各个值都设置正确，特别是：
    -   application：编辑 application 标签中的 android:label 来设置 app 的最终名字。
    -   uses-permission：如果你的代码需要互联网交互，请加入 android.permission.INTERNET 权限标签。标准开发模版里并未加入这个权限（但是 Flutter debug 模版加入了这个权限），加入这个权限是为了允许 Flutter 工具和正在运行的 app 之间的通信。
-   检查 [project]/android/app/build.gradle 文件，并确认各个值都设置正确否,可参考[Gradle 构建文件 文档中模块级构建的部分](https://developer.android.google.cn/studio/build?hl=zh-cn#groovy)。

-   在 **defaultConfig** 配置中

    | 配置名            | 说明                                                                                                                                          |
    | ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
    | applicationId     | 指定唯一的 应用 ID - minSdkVersion: 指定应用适配的最低 SDK 版本。默认为 <code>flutter.minSdkVersion</code>（怎么查看当前 flutter 使用的版本） |
    | targetSdkVersion  | 指定应用适配的目标 SDK 版本。默认为 <code>flutter.targetSdkVersion</code>                                                                     |
    | versionCode       | 用于内部版本号的正整数。该数字仅用于比较两个版本间数字较大的为更新版本。该版本不会对用户展示                                                  |
    | versionName       | 向用户展示的版本号。该字段必须设置为原始字符串或字符串资源的引用                                                                              |
    | buildToolsVersion | 如果你正在使用高于 3.0.0 版本的 Android Gradle Plugin，你的项目会自动使用 AGP 默认指定的构建工具版本。你也可以手动指定构建工具的版本          |

    -   在 android 配置中
        -   compileSdkVersion: 指定 Gradle 用于编译应用的 API 版本。默认为 flutter.compileSdkVersion

## 构建的 apk 说明

> 带上参数<code>--split-per-abi</code>打包后，会生成一下三个 APK 文件

[project]/build/app/outputs/apk/release/app-armeabi-v7a-release.apk
[project]/build/app/outputs/apk/release/app-arm64-v8a-release.apk
[project]/build/app/outputs/apk/release/app-x86_64-release.apk

-   **arm64-v8a:** 第 8 代、64 位 ARM 处理器
-   armeabiv-v7a: 第 7 代及以上的 ARM 处理器，是目前主流版本，大部分 Android 设备都使用它
-   x86/x86_64: x86 架构的手机都会包含由 Intel 提供的称为 Houdini 的指令集动态转码工具，实现对 arm .so 的兼容。**平板、模拟器用得比较多**

## 生成 apk 签名

-   [给 APK 签名—两种方式（flutter android 安装包）](https://blog.csdn.net/ly_xiamu/article/details/131923058)

## 版本更新提醒和下载 APK

-   获取本地版本号
-   请求服务器的 API 接口获取服务器保存的版本号
    -   **修改对应 build 过程，build 完成后，向外生成当前最新的版本号**
-   请求服务器的 API 接口获取服务器保存的版本号
-   本地版本和服务器版本不一致提示升级，弹窗提示用户是否更新
-   本地版本和服务器版本不一致提示升级，弹窗提示用户是否更新
-   用户确定升级，调用文件传输方法下载 apk 文件
-   监听下载进度
-   下载完成打开 APK 进行安装
