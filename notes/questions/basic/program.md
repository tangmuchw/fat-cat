[toc]

# 给你两个有序整数数组 nums1 和 nums2，请你将 nums2 合并到 nums1 中，使 nums1 成为一个有序数组。时间复杂度为 O(m+n)

> > 输入: nums1 = [1,2,3,0,0,0], nums2 =[2,5,6]
> > 输出: [1,2,2,3,5,6]

```JavaScript
   const merge = function (nums1, m, nums2, n) {
    let p1 = m - 1, p2 = n - 1,
        tail = m + n - 1,
        cur,

    while (p1 >= 0 || p2 >= 0) {
        if (p1 === -1) {
            cur = nums2[p2--];
        } else if (p2 === -1) { // nums2 已合并完，取下一个 nums1
            cur = nums1[p1--];
        } else if (nums1[p1] > nums2[p2]) {
            cur = nums1[p1--];
        } else {
            cur = nums2[p2--];
        }
        nums1[tail--] = cur;
    }

    return nums1
};
```

# 将 'aabbcca' 转变成 'a2b2c2a1'

```JavaScript
const transferStr = (str) => {
    const len = str.length

    let lastChar = str[0],
        count = 1,
        newStr = ''

    for (let i = 1; i <= len; i++) {
        if (str[i] == lastChar) count++
        else {
            newStr = `${newStr}${lastChar}${count}`
            count = 1
            lastChar = str[i]
        }
    }

    return newStr
}

```
