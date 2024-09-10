# Dom Diff

> [精读《DOM diff 原理详解 》](https://mp.weixin.qq.com/s/KCX8xwY563qCAJqaK2H2EA?st=2BCC724C2A0B94F861A30D70BF64C24EA68983C46651AB21834FB02DDF60896BD70190C0E60EFAFB4E2EE044248F34BCAE5868998B4C03BBF909D25BD8965AD0D9106441BBB9EA5B940AD4B0B9875E4F31A55A4CCA8BF413209BF986FA8F6333915C3610F56B68331E33C2C5B1E1BDB2154EC22E2C651238BB953FDA6EB08275&vid=1688853527239128&cst=E88AD777D5407E011E094949C85251F5BB0E64FA7A001884709CA04204B466743868BA3CEF38C0B32238B5D42FC1ADD4&deviceid=935d7942-b09f-4038-b6eb-c5f25ce0db0a&version=3.1.0.2353&platform=mac)

# Vue 的 Dom Diff

> 为了尽量不宜动，先左右夹击跳过不变的，再找到最长连续子串保持不动，移动其他元素

# React 的 Dom Diff

> 采用了仅右移动方案，在大部分从左往右移的业务场景中，得到了较好的性能

## React DOM Diff 的过程

> 参考文章 [深入理解 react》之 DIFF 算法](https://juejin.cn/post/7357542359565008946) 说明

> _.old.js 和 _.new.js 共存的原因： React 团队在实现 Suspense 和 Concurrent。这两个依赖的时间过期模型遍布 reconciler，所以很难通过几个 tag 来标记改动，并且不影响正常迭代。

-   构建 **workInProgress** 树 🌲 的过程中，需要经历 **beginWork** 流程，而今天的主角 diff 算法就是发生在这个过程中的，在 beginWork 流程中会根据最新的 ReactElement 和 current Fiber 树来生成 workInProgres，因此参与 diff 算法的对象就是新 ReactElement 和 current🌲
-   diff 的核心作用就是**在新生成的 workInProgress 树上打上标签**，以供后面的 commit 流程使用

对于单个节点，没有 diff 的意义，直接判断就好了，因此 diff 只会发生在某一层有多个节点的情况，核心就是 **reconcileChildrenArray** 这个函数

```Javascript
function reconcileChildrenArray(
  returnFiber,
  currentFirstChild,
  newChildren,
  lanes
) {
  var resultingFirstChild = null; // 新构建的第一个childFiber
  var previousNewFiber = null; // 前一个新fiber

  var oldFiber = currentFirstChild; // 第一个oldFiber
  var lastPlacedIndex = 0; // 标记

  var newIdx = 0; // 索引
  var nextOldFiber = null;

  // 第一轮判断
  for (; oldFiber !== null && newIdx < newChildren.length; newIdx++) {
    if (oldFiber.index > newIdx) {
      nextOldFiber = oldFiber;
      oldFiber = null;
    } else {
      nextOldFiber = oldFiber.sibling;
    }

    var newFiber = updateSlot( // 从第一个old fiber 开始与 第一个 newChild 比较，看是否相同
      returnFiber,
      oldFiber,
      newChildren[newIdx],
      lanes
    );

    if (newFiber === null) { // 说明开始不同了 开始退出；
      if (oldFiber === null) {
        oldFiber = nextOldFiber;
      }

      break;
    }

    lastPlacedIndex = placeChild(newFiber, lastPlacedIndex, newIdx);

    if (previousNewFiber === null) {
      resultingFirstChild = newFiber;
    } else {
      previousNewFiber.sibling = newFiber;
    }

    previousNewFiber = newFiber;
    oldFiber = nextOldFiber;
  }


  // 说明 新的ReactElements被用完了 ， 直接删除所有的旧节点就好了
  if (newIdx === newChildren.length) {
    deleteRemainingChildren(returnFiber, oldFiber); // 标记删除节点
    return resultingFirstChild;
  }

  // 说明 oldFiber 被用完了，直接创建新的节点就好了
  if (oldFiber === null) {
    for (; newIdx < newChildren.length; newIdx++) {
      var _newFiber = createChild(returnFiber, newChildren[newIdx], lanes);

      if (_newFiber === null) {
        continue;
      }

      lastPlacedIndex = placeChild(_newFiber, lastPlacedIndex, newIdx);

      if (previousNewFiber === null) {
        resultingFirstChild = _newFiber;
      } else {
        previousNewFiber.sibling = _newFiber;
      }

      previousNewFiber = _newFiber;
    }
    return resultingFirstChild;
  }


  // 说明都没有被用完，只是找到不同的节点而已，开始diff真正的逻辑；
  var existingChildren = mapRemainingChildren(returnFiber, oldFiber); // Keep scanning and use the map to restore deleted items as moves.

  for (; newIdx < newChildren.length; newIdx++) {
    var _newFiber2 = updateFromMap( // 从existingChildren中找存在的fiber
      existingChildren,
      returnFiber,
      newIdx,
      newChildren[newIdx],
      lanes
    );

    if (_newFiber2 !== null) {
      if (_newFiber2.alternate !== null) {
        existingChildren.delete(
          _newFiber2.key === null ? newIdx : _newFiber2.key
        );
      }

      lastPlacedIndex = placeChild(_newFiber2, lastPlacedIndex, newIdx);

      if (previousNewFiber === null) {
        resultingFirstChild = _newFiber2;
      } else {
        previousNewFiber.sibling = _newFiber2;
      }

      previousNewFiber = _newFiber2;
    }
  }

  existingChildren.forEach(function (child) {
    return deleteChild(returnFiber, child);
  });

  return resultingFirstChild;
}

```

-   第一轮判断，找出不同

    -   把 current 树（链表）叫作 old，新的 ReactElements 数组 叫做 new，首先准备几个全局变量 oldFiber 代表 old 的第一个节点，newIdx 代表递增索引，接下来看是第一轮遍历
    -   第一轮会依次遍历 new 的每个节点，从 new 的第一个节点开始与 old 的第一个节点开始对比，如果两个节点相同，则复用，将 oldFiber 指向链表下一个，将索引递增，继续第一轮循环；如果不同，则退出第一轮循环，在退出时需要将新的 fiber 节点的引用关系重新设定。
    -   总结一下能够退出第一轮的有三种情况：
        -   old 节点被用完了
        -   new 节点被用完了
        -   发现了不可复用的节点

-   断言
    -   在断言的部分就是对第一和第二两种情况的处理，如果 **old 节点被用完了，那么说明本次更新中很多新的节点**，需要将他们添加到页面中，所以给他们直接创建 fiber 节点并打上添加的标签就好了
    -   如果 new 节点被用完了，说明在新的更新中，需要删除了后面的节点，因此直接在父 fiber 节点中打上需要**删除子节点的标签**
-   真正的 diff 逻辑

    -   如果发现了第一个不可复用节点，就要开始进入真正 diff 策略的执行了，核心就是用一个叫做 **lastPlacedIndex** 的变量来记录是否需要右移的判断标准，它的初始值是 0，它只会变得更大，不会变的更小，react 的思路就是通过将 old 的节点不断的向右移动，逐渐使其变成 new 的样子
    -   用一个 map 将 key 的对应关系 fiber 保存起来
    -   创建好了这个 map 之后，依次遍历 new 的每个节点，然后判断是否存在于 map 中，如果存在就说明可以复用，并且可以决策是否打标签了，打标签的依据如下（fiber 身上其实也保存了自己在当前列表中处于的索引，我们获取当前这个可以复用的 fiber 的 old 索引）：
        -   如果这个索引小于 lastPlacedIndex 的话，就打上标签
        -   否则将 lastPlacedIndex 赋值为这个索引
    -   移动策略变成**移动到右侧第一个没有打标签的元素之前，而不是移动到最右侧**
    -   在 react 源码中通过**var before = getHostSibling(finishedWork)**；来找到当前打标签的元素应该插入到哪个元素之前，它的策略就是找到最右侧第一个未打上标签的元素。

-   小结：React 的 diff 策略我们可以认为他是右移策略，将需要移动的节点打上标签，然后在 commit 依次遍历这些具有标签的节点将她们移动到右侧的第一个未打标签的元素之前
