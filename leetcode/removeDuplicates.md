# 删除排序数组中的重复项

> 输入：nums = [0,0,1,1,1,2,2,3,3,4]
> 输出：5, nums = [0,1,2,3,4]
> 解释：函数应该返回新的长度 5 ， 并且原数组 nums 的前五个元素被修改为 0, 1, 2, 3, 4 。不需要考虑数组中超出新长度后面的元素。

## 解析

> 双指针解法

```JavaScript

const removeDuplicates = (list) => {
    if(!Array.isArray(list)) return 0

    const len = list.length

    let left = 0

    for(let right = 1; right < len; right++) {
        // 如果左指针和右指针指向的值一样，说明有重复
        // 这个时候，左指针不动，右指针继续右移
        // 如果他俩指向的值是不一样，就使右指针指向的值赋值到左指针 +1 上,
        if(list[right] !== list[left]) list[++left] = list[right]
    }

    return ++left

}

```
