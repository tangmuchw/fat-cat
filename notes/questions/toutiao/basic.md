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