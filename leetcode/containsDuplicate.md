# 存在重复元素

> 给定一个整数数组，判断是否存在重复元素。
> 如果存在一值在数组中出现至少两次，函数返回 <code>true</code> 。如果数组中每个元素都不相同，则返回 <code>false</code> 。

## 示例

> 输入: [1,1,1,3,3,4,3,2,4,2]
> 输出: true

## 解析

```JavaScript
const containsDuplicate = (nums) => {
    const sets = new Set(nums)
    if(sets.size !== nums.length) return true

    return false
}

const containsDuplicate2 = (nums) => {
 nums.sort((a, b) => a - b)

 for(let i = 1; i < nums.length - 1; i++) {
     if(nums[i] === nums[i - 1]) return true
 }

 return false
}

```
