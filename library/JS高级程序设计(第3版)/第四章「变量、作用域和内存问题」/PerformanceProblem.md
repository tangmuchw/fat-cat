# PerformanceProblem 性能问题

> IE7 发布后，JavaScript 引擎的垃圾收集例程改变了工作方式：触发垃圾收集的变量分配、字面量和数组与纳素的临界值被调整为动态修正。IE7 中的各项临界值在初始时与 IE6 相等(256 个变量，4096 个对象或数组字面量和数据元素 slot 或者 64KB 的字符串)。

- 如果垃圾收集例程回收的内存分配量低于 15%, 则变量、字面量和数据元素的临界值就会加倍。
- 如果例程回收了 85% 的内存分配量，则将各种临界值重置回默认值。

## 有关性能的 API

- IE, window.CollectGarbage() 会立即执行垃圾收集
- Opera 7 及更高版本中，调用 window.opera.collect() 启动垃圾收集例程
- Chrome, window.performance 对象
