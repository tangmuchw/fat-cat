## 对 requestAnimationFrame 的理解
>> 告诉浏览器——你希望执行一个动画，并且要求浏览器在下次重绘之前调用指定的回调函数更新动画。该方法需要传入一个回调函数作为参数，该回调函数会在浏览器下一次重绘之前执行
- 顾名思义就是**请求动画帧**
- 其最大优势是**由系统来决定回调函数的执行时机**
- 与react 16.x 的更新dom机制有关

## package.json 中的peerDependencies
>> 指定当前组件的依赖以及其版本。如果组件使用者在项目中安装了其他版本的同一依赖，会提示报错。**起一个检查依赖版本报错机制**

## 虚拟DOM的好处
>> 减少了同一时间内的页面多处内容修改所触发的浏览器reflow和repaint的次数，可能把多个不同的DOM操作几种减少到了几次甚至一次，优化了触发浏览器reflow和repaint的次数

## 编程 compose 实现
```JavaScript
/**
 * 解析实现
 * foo = (num) => add(multiply(num))
*/

const compose = (...funcs) => {
    if(!funcs.length) return (num) => { console.log(num) }

    return funcs.reduce((a, f) => (...arg) => a(f(...arg)))
}

// 问题描述
const add = num => num  + 10
const multiply = num => num * 2
const foo = compose(multiply, add)
console.log(foo(5)) // 30
```


## 找出所有出现两次的元素。需要不用到任何额外的空间并在O(n)时间复杂度内解决这个问题
>> 输入: [4,3,2,7,8,2,3,1]
>> 输出: [2,3]

```JavaScript
 // 原地哈希： 将值为list[i]的数字映射到list[i]-1的下标位置

 const findTwiceEle = (list) => {
     const len = list.length

     for(let i = 0; i < len - 1; i++){
         const ele = list[i]
         const idx = ele - 1
         
         if(ele !== list[idx]) {
             [list[idx], list[i]] = [list[i] , list[idx]]
             i--
         } 

     }

     console.log('list =>',list) //  [1, 2, 3, 4, 3, 2, 7, 8]

     for(let j = 0; j < len - 1; j++) {
         if(list[j] - 1 !== j) {
             list.push(list[j])
         }
     }

     return list.slice(len)
 }

 console.log(findTwiceEle([4,3,2,7,8,2,3,1]))
```


## 给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的那 两个 整数，并返回他们的数组下标。你可以假设每种输入只会对应一个答案。但是，你不能重复利用这个数组中同样的元素。
>> 示例 nums = [2, 7, 11, 15], target = 9
>>  nums[0] + nums[1] = 2 + 7 = 9, 输出 [0, 1]

```JavaScript
 const twoSum = (list, target) => {
     for(let i = 0; i < list.length; i++ ){
         let temp = target - list[i]
         let idx = list.lastIndexOf(temp)

         if(idx !== -1 && idx !== i) return [i, idx]
     }
 }
```

## 洗牌算法
```JavaScript
 Array.prototype.shuffle = function(){
     let me = this

     for(let i = me.length - 1; i >= 0; i--){
         let randomIdx = Math.floor(Math.random()*(i+1))
         let temp = me[randomIdx]

         me[randomIdx] = me[i]
         me[i] = temp
     }

     return me
 }

 console.log([1,2,3,4,5,6,7,8].shuffle())
```


## 数组中的第 K 个最大元素,在未排序的数组中找到第 k 个最大的元素。请注意，你需要找的是数组排序后的第 k 个最大的元素，而不是第 k 个不同的元素。
>> 输入: [3,2,1,5,6,4] 和 k = 2 => [1,2,3,4,5,6]
>> 输出: 5
>> 输入: [3,2,3,1,2,4,5,5,6] 和 k = 4 => [1,2,2,3,3,4,5,5,6]
>> 输出: 4

```JavaScript
const swap = (list, idxA, idxB) => {
     if(idxA === idxB) return

     const a = list[idxA]
     const b = list[idxB]
     const c = a ^ b
     
     list[idxA] = c ^ a
     list[idxB] = c ^ b
 }

 const separateList = (list, start = 0, end = list.length - 1) => {
     if(start >= end) return

     const randomIdx = Math.random() * (end - start + 1) + start
     const pivotIdx = Math.floor(randomIdx)
     const pivot = list[pivotIdx]

     swap(list, pivotIdx, end)

     let i = start - 1
     for(let j = start; j < end; j++){
         if(list[j] < pivot) {
             i++
             swap(list, i, j)
         }
     }

     swap(list, i + 1, end)

     separateList(list, start, i)
     separateList(list, i + 2, end)

     return list
 }

 const quickSort = (list) => {
     return separateList(list)
 }

 const list = [3,2,3,1,2,4,5,5,6]
 const k = 4
 const findKthLargest = (nums, k) => {
    quickSort(nums)
    console.log(nums)
    return nums[nums.length - k]
      
 }

 console.log(findKthLargest(list, k))
```


## 爬楼梯。假设你正在爬楼梯，需要n阶你才能到达楼顶。每次你可以爬1或2哥台阶，你有多少种不同的不同的方法可以爬到楼顶
>> 输入： 2
>> 输出： 2
>> 解释： 有两种方法可以爬到楼顶。1. 1阶 + 1阶； 2. 2阶

>> 解题思路：可以这样想，n个台阶，一开始可以爬 1 步，也可以爬 2 步，**那么n个台阶爬楼的爬楼方法就等于 一开始爬1步的方法数 + 一开始爬2步的方法数**，这样我们就只需要计算n-1个台阶的方法数和n-2个台阶方法数，同理，计算n-1个台阶的方法数只需要计算一下n-2个台阶和n-3个台阶，计算n-2个台阶需要计算一下n-3个台阶和n-4个台阶……

```JavaScript
    const climbStairs = (n) => {
        if(n === 1) return 1

        let sum = [0, 1, 2]

        for(let i = 3; i <= n; i++){
            sum[i] = sum[i - 1] + sum[i - 2]
        }

        return sum[n]
    }

    console.log(climbStairs(5)) // 8
```


## 使用最小花费爬楼梯。数组的每个索引作为一个阶梯，第i个阶梯对应着一个非负数的体力花费之cost[i](索引从0开始)，每当你爬上一个阶梯你都要花费对应的体力花费之，然后你可以选择继续爬一个阶梯或者两个阶梯。您需要找到达到楼层顶部的最低花费。在开始时，你可以选择从索引0或1的元素作为初始阶梯
>> 输入： cost = [10, 15, 20]
>> 输出： 15
>> 解释：最低花费是从cost[1]开始，然后走两步即可到阶梯顶，一共花费15

>> 解题：比如当前是第6级阶梯，则站在这级台阶需要的体力就是min{站在第五计级的最小体力 + 这一级体力，站在第四级的最小体力 + 这一级体力 }

```JavaScript
    const minCostClimbStairs = (cost = []) => {
        let dp = [0, 0],
         len = cost.length

        for(let i = 2; i <= len; i++){
            dp[i] = Math.min(dp[i - 1] + cost[i - 1], dp[i - 2] + cost[i - 2])
        }

        return dp[len]
    }

    console.log(minCostClimbStairs([10, 15, 20])) // 15
```


## 编辑距离。给定两个单词word1和word2，计算出将word1转换成word2所使用的最少操作数。可以对一个单词进行如下操作：1.插入一个字符 2.删除一个字符 3.替换一个字符

>> 输入：word1='horse', word2='ros'
>> 输出：3
>> 解释： horse => rorse (将'h'替换'r') => rose (删除'r') => ros (删除'e')

```JavaScript
    const minDistance = (word1, word2) => {
        const len1 = word1.length
        const len2 = word2.length

        if(len1 === 0) return len1
        if(len2 === 0) return len2

        let dp = new Array()

        dp[0][0] = 0

        for(let i = 1; i <= len1; i++) dp[i][0] = i
        for(let j = 1; j <= len2; j++) dp[0][j] = i

        for(let m = 1; m <= len1; m++){
            for(let n = 1; n <= len2; n++) {
                if(word[m -1] === word[n - 1]){
                    // dp[1][1] = dp[0][0]
                    dp[i][j] = dp[i - 1][j - 1]
                } else {
                    // min(dp[0][1] + 1, min(dp[1][0] + 1, dp[0][0] + 1 ))
                    dp[i][j] = Math.min(
                        dp[i - 1][j] + 1,
                        Math.min(
                            dp[i][j - 1] + 1,
                            dp[i - 1][j - 1] + 1
                        )
                    )
                }
            }
        }

        return dp[len1][len2]
       
    }

    console.log(minDistance('horse', 'ros')) // 3
```

## 简单说一下react 16.x执行过程
- jsx经过babel转变成render函数
- create update
- enqueueUpdate
- scheduleWork 更新 expirationTime
- requestWork
- workLoop大循环
- Effect List
- commit

## cookie 跨域时候要如何处理
- 设置Nginx代理服务器，将两个服务器域名统一到一个反向代理服务器

## 301, 302, 303, 307, 308的区别
- 301， 308 属于永久重定向，两者默认缓存，301允许将请求方法从POST改为GET，308不允许
- 302，303，307属于临时重定向
 + 302 妥协处理，允许请求方法从POST改为GET
 + 303 强制浏览器可以将请求方法从POST改为GET
 + 307 不允许浏览器修改请求方法

## 求二叉树所有根到叶子路径组成的数字之和
>> 二叉树每个节点的value范围是1-9
>> 例如：
>>                   1
>>         2                    3 
>>  4          5
>> 从根到叶子共3条：1->2->4, 1->2->5, 1->3
>> 构成的数字为124，125，13，求和124 + 125 + 13 = 262即为所求

```JavaScript
 const root = {
     val: 1,
     left: {
         val: 2,
         left: {
             val: 4,
             left: null,
             right: null
         },
         right: {
             val: 5,
             left: null,
             right: null
         }
     },
     right: {
         val: 3,
         left: null,
         right: null
     }
 }


 const getSum = (root, sum = 0) => {
     if(root === null) return 0

     sum = root.val + sum * 10

     if(root.left === null && root.right === null) return sum

     return getSum(root.left, sum) + getSum(root.right, sum)
 }

 console.log(getSum(root, 0))
```


## compareVersion(version1, version2) {} 版本号可能是7.5.0或者1.12这种格式，输出较大的版本号

```JavaScript
    const compareVersion = (version1, version2) => {
        const versionList1 = version1.split('.')
        const versionList2 = version2.split('.')
        const maxLen = Math.max(version1.length, version2.length)

        for(let i = 0; i < maxLen; i++){
            let v1 = i < version1.length ? versionList1[i] : 0
            let v2 = i < version2.length ? versionList2[i] : 0

            if(v1 === v2) continue

            if(v1 > v2) return 1 // version1大
            else return -1  // version2大
        }


        return 0 // 相等
    }

    console.log(compareVersion('7.5.0', '1.12'))
```