[toc]

# 给你两个有序整数数组 nums1 和 nums2，请你将 nums2 合并到 nums1 中，使 nums1 成为一个有序数组。时间复杂度为O(m+n)

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


# 箭头函数与普通函数区别？能不能作为构造函数？
- 最大的区别其实就是this指向
 + 箭头函数没有自己的this，箭头函数的this指向**在定义时候**继承**自外层的一个普通函数**的this，永远不会改变
- 箭头函数没有prototype， 所以箭头函数本身没有this
- 箭头函数不能作为构造函数使用
- 箭头函数不绑定arguments，取而代之用rest参数...代替arguments对象，来访问箭头函数的参数列表
 ```JavaScript
 const getRest = (...params) => { 
     console.log(params)
 }
 ```
- 箭头函数不能作Generator函数，不能使用yield关键字
