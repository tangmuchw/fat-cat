# 求二叉树所有根到叶子路径组成的数字之和

> 二叉树每个节点的 value 范围是 1-9
> 例如：
> 1
> 2 3
> 4 5
> 从根到叶子共 3 条：1->2->4, 1->2->5, 1->3
> 构成的数字为 124，125，13，求和 124 + 125 + 13 = 262 即为所求

```JavaScript
 const root = {
     val: 1,
     left: {
         val: 2,
         left: {
             val: 4,
             left: null,
             right: null
         },
         right: {
             val: 5,
             left: null,
             right: null
         }
     },
     right: {
         val: 3,
         left: null,
         right: null
     }
 }


 const getSum = (root, sum = 0) => {
     if(root === null) return 0

     sum = root.val + sum * 10

     if(root.left === null && root.right === null) return sum

     return getSum(root.left, sum) + getSum(root.right, sum)
 }

// const getSum = (data, num = data.val) => {
//     const { left, right } = data

//     if (left === null || right === null) return num

//     const nextNum = num * 10
//     return getSum(left, nextNum + left.val) + getSum(right, nextNum + right.val)
// }

 console.log(getSum(root, 0))
```
