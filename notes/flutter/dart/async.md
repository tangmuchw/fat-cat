# 异步支持

## Feature

> 表示一个异步操作的最终完成（或失败）及其结果值的表示

-   Feature.then
-   Feature.catchError
-   Feature.whenComplete: 无论异步任务执行成功或失败都需要做一些事的场景
-   Feature.wait: 等待多个异步任务都执行结束后才进行一些操作

## Stream

> Stream 也是用于接收异步事件数据，和 **Future 不同的是，它可以接收多个异步操作的结果（成功或失败）**，

-   Stream 常用于会多次读取数据的异步任务场景，如网络内容下载、文件读写等

```Dart
main() async {
    // 有时代码逻辑需要调用多个异步函数，并等待它们全部完成后再继续执行
    // 使用 Future.wait() 静态方法管理多个 Future 以及等待它们完成：
    Future<void> deleteLotsOfFiles() async =>  ...
    Future<void> copyLotsOfFiles() async =>  ...
    Future<void> checksumLotsOfOtherFiles() async =>  ...

    await Future.wait([
    deleteLotsOfFiles(),
    copyLotsOfFiles(),
    checksumLotsOfOtherFiles(),
    ]);
    print('Done with all the long steps!');
}
```

```Dart
main() async {
  Future<void> delete() async =>  ...
  Future<void> copy() async =>  ...
  Future<void> errorResult() async =>  ...

  try {
    // 获得多个异步的结果
    // Wait for each future in a list, returns a list of futures:
    var results = await [delete(), copy(), errorResult()].wait;

    } on ParallelWaitError<List<bool?>, List<AsyncError?>> catch (e) {

    print(e.values[0]);    // Prints successful future
    print(e.values[1]);    // Prints successful future
    print(e.values[2]);    // Prints null when the result is an error

    print(e.errors[0]);    // Prints null when the result is successful
    print(e.errors[1]);    // Prints null when the result is successful
    print(e.errors[2]);    // Prints error
  }
}
```
