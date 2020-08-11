# 小部分

## 给你两个有序整数数组 nums1 和 nums2，请你将 nums2 合并到 nums1 中，使 nums1 成为一个有序数组。时间复杂度为O(m+n)

>> 输入: nums1 = [1,2,3,0,0,0], nums2 =[2,5,6]
>> 输出: [1,2,2,3,5,6]


```JavaScript
    // 使用归并排序中的并思想
    const mergeSort = (leftList, rightList) => {
        const leftLen = leftList.length
        const rightLen = rightList.length
        const mid = Math.floor(leftLen / 2)

        let tail = leftLen + rightLen - 1,
         lPointer = mid - 1,
         rPointer = rightLen - 1

        while(rPointer >= 0) {
            if(leftList[lPointer] < rightList[rPointer]) {
                leftList[tail] = rightList[rPointer]
                rPointer--
            } else {
                leftList[tail] = leftList[lPointer]
                lPointer--
            }
            
            tail--
        }

        return leftList
    }
```