# 找出所有出现两次的元素。需要不用到任何额外的空间并在 O(n)时间复杂度内解决这个问题

> 输入: [4,3,2,7,8,2,3,1]
> 输出: [2,3]

```JavaScript
 // 原地哈希： 将值为list[i]的数字映射到list[i]-1的下标位置

 const findTwiceEle = (list) => {
     const len = list.length

     for(let i = 0; i < len; i++){
         const ele = list[i]
         const idx = ele - 1

         if(ele !== list[idx]) {
             [list[idx], list[i]] = [list[i] , list[idx]]
             i--
         }

     }

     console.log('list =>',list) //  [1, 2, 3, 4, 3, 2, 7, 8]

     for(let j = 0; j < len; j++) {
         if(list[j] - 1 !== j) {
             list.push(list[j])
         }
     }

     return list.slice(len)
 }

 console.log(findTwiceEle([4,3,2,7,8,2,3,1]))
```
