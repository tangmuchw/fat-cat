# 数组中的第 K 个最大元素,在未排序的数组中找到第 k 个最大的元素。请注意，你需要找的是数组排序后的第 k 个最大的元素，而不是第 k 个不同的元素。

> 输入: [3,2,1,5,6,4] 和 k = 2 => [1,2,3,4,5,6]
> 输出: 5
> 输入: [3,2,3,1,2,4,5,5,6] 和 k = 4 => [1,2,2,3,3,4,5,5,6]
> 输出: 4

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
