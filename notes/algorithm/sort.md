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

    // 基准的值换到了末尾
    swap(list, pivotIdx, end)

    // 重新排序数列，所有元素比哨兵值小的摆放在哨兵前面，所有元素比哨兵值大的摆在哨兵的后面（相同的数可以到任一边）
    // i 记录最后一个小于基准值的索引
    for(let i = start - 1, j = start; j < end; j++){
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