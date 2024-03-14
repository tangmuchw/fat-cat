# lerna 发包原理

> 参考 [lerna 发包原理浅析](https://zhuanlan.zhihu.com/p/392438222?utm_id=0)

## 基本原理

> 获取最新的 tag，然后用 git diff 获取自该 tag 以来有更新的文件，以此来确定有哪些需要发布的包。如果没有 tag，则认为全部的包都需要发布。

## 核心实现逻辑

-   获取有更新的包，与 lerna changed 逻辑一致，依赖 collectUpdates
-   获取有更新的包的新版本号 getVersionsForUpdates
-   设置版本号 setUpdatesForVersions
-   让用户确认版本号 confirmVersions
-   修改 package.json updatePackageVersions
