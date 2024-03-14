# 排序算法

## js 中的 sort

> 当数组长度小于等于 10 的时候，采用插入排序，大于 10 的时候，采用快排;
> 对于长度大于 1000 的数组，采用的是快排与插入排序混合的方式进行排序的，因为，当数据量很小的时候，插入排序效率优于快排。
> compareFn(a, b) 为 a - b，即将数组升序排列
> | compareFn(a, b) 返回值 | 排序顺序 |
> | ---------------------- | ---------------------- |
> | > 0 | a 在 b 后，如 [b, a] |
> | < 0 | a 在 b 前，如 [a, b] |
> | === 0 | 保持 a 和 b 原来的顺序 |

```JavaScript
 /**
 * @description 交换数组中两项
 */
 const swap = (list, idxA, idxB) => {
     if(idxA === idxB) return

     const a = list[idxA]
     const b = list[idxB]
     const c = a ^ b

     list[idxA] = c ^ a
     list[idxB] = c ^ b

     // => [list[idxB], list[idxA]] = [list[idxA], list[idxB]]
 }
```

## 冒泡排序

-   时间复杂度**O(n\*n)**
-   思路

*   比较相邻的元素，前者比后者大的话，两者交换位置
*   对每一对相邻元素做相同操作，从开始第一对到最后一对，这样子最后的元素就是最大元素
*   针对 n 个元素重复以上步骤，每次循环排除当前最后一个
*   重复以上步骤，直到排序完成

```JavaScript
const bubbleSort = (list) => {
   const len = list?.length - 1

   if(!len) return []

   // 最外层循环控制的内容是循环次数
   // 每一次比较的内容都是相邻两者之间的大小关系
   const count = len - 1
   for(let i = 0; i < len; i++) {
       for(let j = 0; j < count; j++){
           if(list[j] > list[j + 1]) [list[j + 1], list[j]] = [list[j], list[j + 1]]
       }
   }

   return list
}
```

## 快速排序

> 快速排序使用分治法策略来把一个数组分为两个子数组

-   平均时间复杂度**O(nlogn)**
-   首先从数组中挑出一个元素，并将这个元素称为<code>基准</code>（pivot）
-   重新排序数组，所有比基准值小的元素摆放在基准前面，所有比基准值大的元素摆在基准后面，相同的数可以放在任何一边
-   在这个分区结束排序，该基准就处于数组的中间位置，这个称为分区（partition）操作，
-   之后，在子序列中继续重复这个方法，直到最后整个数据序列排序完成

```JavaScript
 const separateList = (list, comparator, start = 0, end = list.length - 1) => {
    if(start >= end) return

    // 随机取一个基准
    const randomIdx = start + Math.random() * (end - start + 1)
    const pivotIdx = Math.floor(randomIdx)
    const pivot = list[pivotIdx]

    // 基准的值换到了末尾, 为了后面进行基准对比
    swap(list, pivotIdx, end)

    // 重新排序数列，所有元素比哨兵值小的摆放在哨兵前面，所有元素比哨兵值大的摆在哨兵的后面（相同的数可以到任一边）
    // lastMinIdx 记录最后一个小于基准值的索引
    let lastMinIdx = start - 1
    for(let i = start; i < end; i++){
        // a < b
        if(comparator(list[i], pivot) < 0){
            lastMinIdx++
            swap(list, lastMinIdx, i)
        }
    }

    // 将基准放在中间位置，作为分区
    swap(list, lastMinIdx + 1, end)

    // 递归地把小于哨兵值元素的子数列和大于哨兵值元素的子数列排序
    separateList(list, comparator, start, lastMinIdx)
    separateList(list, comparator, lastMinIdx + 2, end)

    return list
 }

const quickSort = (list, comparator = (a, b) => a - b) => {
    return separateList(list, comparator)
}

console.log(quickSort([1, 7, 4, 8, 3, 18])) // [1, 3, 4, 7, 8, 18] => take 0.069 s
```

## 插入排序

> 插入排序是一种简单且稳定的算法，适用于已排好序的序列，往其他插入某个元素，保证数据有序

-   时间复杂度：O(n\*n)

### 特点

-   序列中的数据分为两个区域：已排序区域和未排序区域
-   从序列的最左侧开始定义排序区域
-   已排序区域的数据按照从小到达的顺序进行排列
-   元素比较时，首先用未排序区域的第一个元素与已排序区域的最后一个元素进行比较

```JavaScript
 const insertSort = (list) => {
     const len = list.length

     for(let i = 1; i < len; i++){
         let temp = list[i]
            leftLastIdx = i - 1 // 假定记录要插入的位置个位置前一个位置

        // 数值大的往后插
         while(leftLastIdx >= 0 && list[leftLastIdx] > temp) {
             list[leftLastIdx + 1] = list[leftLastIdx] // 已排序的元素大于新元素，将该元素插到一下个位置
             leftLastIdx-- // 检查已排序区域的上一个位置
         }

        list[leftLastIdx + 1] = temp // 交换被插入位置的值
     }

     return list
 }

console.log(insertSort([1, 7, 4, 8, 3, 18])) // [1, 3, 4, 7, 8, 18] => take 0.066 s
```

## 归并排序

> 归并排序使用是分治思想

-   **分**的过程， 将其分成左右两个部分，分别递归
-   **治**的过程，将左右两个部分合并

-   空间复杂度：O(n)
-   时间复杂度：O(nlogn)

```JavaScript

/**
* @description 递归方法，实现对数组的分割和合并
* @params {Array} tempList 存放被分割的数组
* @params {number} start 开始下标
* @params {number} end 结束下标
*/
 const combine = (leftList, rightList) => {
    const leftLen = leftList.length
    const rightLen = rightList.length

    let result = [],
        leftIdx = 0,
        rightIdx = 0

    while (leftIdx < leftLen && rightIdx < rightLen) {
        result.push(leftList[leftIdx] <= rightList[rightIdx] ? leftList[leftIdx++] : rightList[rightIdx++])
    }

    if (leftIdx < leftLen) result.push(...leftList.slice(leftIdx))
    else result.push(...rightList.slice(rightIdx))

    return result
}

const mergeSort = (list) => {
    const len = list.length

    if (len < 2) return list

    const mid = Math.floor(len / 2)
    const leftList = mergeSort(list.slice(0, mid))
    const rightList = mergeSort(list.slice(mid))

    return combine(leftList, rightList)
}

console.log(mergeSort([1, 7, 4, 8, 3, 18])) // [1, 3, 4, 7, 8, 18] => take 0.071 s
```
