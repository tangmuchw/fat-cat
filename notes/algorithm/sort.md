# 排序算法

## js中的sort
>> 当数组长度小于等于10的时候，采用插入排序，大于10的时候，采用快排;
对于长度大于1000的数组，采用的是快排与插入排序混合的方式进行排序的，因为，当数据量很小的时候，插入排序效率优于快排。

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
 }
```

## 冒泡排序

- 时间复杂度**O(n*n)**
- 思路
 + 比较相邻的元素，前者比后者大的话，两者交换位置
 + 对每一对相邻元素做相同操作，从开始第一对到最后一对，这样子最后的元素就是最大元素
 + 针对n个元素重复以上步骤，每次循环排除当前最后一个
 + 重复以上步骤，直到排序完成

 ```JavaScript
 const bubbleSort = (list) => {
    const len = list.length

    if(!list || !len) return []

    // 最外层循环控制的内容是循环次数
    // 每一次比较的内容都是相邻两者之间的大小关系 
    for(let i = 0; i < len - 1; i++) {
        for(let j = 0; j < len - 1 - i; j++){
            if(list[j] > list[j + 1]){
                [
                    list[j],
                    list[j + 1]
                ] = [
                    list[j + 1],
                    list[j]
                ]
            }
        }
    }

    return list
 }
 ```

 ## 快速排序

 >> 快速排序使用分治法策略来把一个数组分为两个子数组
 - 平均时间复杂度**O(nlogn)**
 - 首先从数组中挑出一个元素，并将这个元素称为<code>基准</code>（pivot）
 - 重新排序数组，所有比基准值小的元素摆放在基准前面，所有比基准值大的元素摆在基准后面，相同的数可以放在任何一边
 - 在这个分区结束止呕，该基准就处于数组的中间位置，这个称为分区（partition）操作，
 - 之后，在子序列中继续重复这个方法，直到最后整个数据序列排序完成

```JavaScript
 const quickSort = (list, comparator = (a, b) => a - b) => {
    return separateList(list, comparator)
 }

 const separateList = (list, comparator, start = 0, end = list.length - 1) => {
    if(start >= end) return

    // 随机取一个基准
    const randomIdx = Math.random() * (end - start + 1) + start
    const pivotIdx = Math.floor(randomIdx)
    const pivot = list[pivotIdx]

    // 基准的值换到了末尾, 为了后面进行基准对比 
    swap(list, pivotIdx, end)

    // 重新排序数列，所有元素比哨兵值小的摆放在哨兵前面，所有元素比哨兵值大的摆在哨兵的后面（相同的数可以到任一边）
    // i 记录最后一个小于基准值的索引
    let i = start - 1
    for(let j = start ; j < end; j++){
        // a < b
        if(comparator(list[j], pivot) < 0){
            i++
            swap(list, i, j)
        }
    }

    // 将基准放在中间位置，作为分区
    swap(list, i + 1, end)

    // 递归地把小于哨兵值元素的子数列和大于哨兵值元素的子数列排序
    separateList(list, comparator, start, i)
    separateList(list, comparator, i + 2, end)

    return list
 }
```

## 插入排序
>> 插入排序是一种简单且稳定的算法，适用于已排好序的序列，往其他插入某个元素，保证数据有序
- 时间复杂度：O(n*n)

### 特点
- 序列中的数据分为两个区域：已排序区域和未排序区域
- 从序列的最左侧开始定义排序区域
- 已排序区域的数据按照从小到达的顺序进行排列
- 元素比较时，首先用未排序区域的第一个元素与已排序区域的最后一个元素进行比较

```JavaScript
 const insertSort = (list) => {
     const len = list.length

     for(let i = 1; i < len; i++){
         let temp = list[i]
         let j = i - 1

         while(j >= 0 && list[j] > temp) {
            // 已排序的元素大于新元素，将该元素移到一下个位置
             list[j + 1] = list[j]
             j--
         }

         list[j + 1] = temp
     }

     return list
 }
```


## 归并排序
>> 归并排序使用是分治思想
- **分**的过程， 将其分成左右两个部分，分别递归
- **治**的过程，将左右两个部分合并

- 空间复杂度：O(n)
- 时间复杂度：O(nlogn)

```JavaScript

/**
* @description 递归方法，实现对数组的分割和合并
* @params {Array} tempList 存放被分割的数组
* @params {number} start 开始下标
* @params {number} end 结束下标
*/
 const mergeSort = (originList, tempList = [], start = 0, end = originList.length) => {
    if (start >= end) return

    let mid = Math.floor((start + end) / 2) // 定义该值将originList从中间分割 
    
    // 分别对新分割好的数组进行分割
    mergeSort(originList, tempList, start, mid)
    mergeSort(originList, tempList, mid + 1, end)

    // 对分割好的数组进行排序和合并操作
    combine(originList, tempList, 0, tempList.length)
 }

 const combine = (originList, tempList, start, end) => {
     // 已知每个数组被分割成了两个子数组, 左和右数组
     // 从左和右数据的最小下标开始，一次进行比较
     let mid = Math.floor((start + end) / 2),
      i = start,
      j = mid + 1,
      pos = start

      // tempList[i]到tempList[mid]为左，反之为右
      // 左当前元素小，就先放在新数组里，反之，右小先放新数组里
      while(i !== mid + 1 && j !== end + 1){
           tempList[pos++] = originList[i] <= originList[j] ? originList[i++] : originList[j++] 
      }

     // 上个操作完成后，左或右可能有剩余，继续将剩余元素补充到需序列总
     // 归并右边剩下的
     while(j !== end + 1) {
         tempList[pos++] = originList[j++]
     }

     // 归并左边剩下的
     while(i !== mid + 1) {
         tempList[pos++] = originList[i++]
     }

     // 转移到原数组
     while(start !== end + 1){
         originList[start] = tempList[start]
         start++
     }
 }

 let originList = [5,4,8,4,9,10,32] 
 mergeSort(originList, [])
 console.log(originList)
```