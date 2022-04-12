# 如何让 (a == 1 && a ==2 && a == 3) 返回 true

```JavaScript
const a = {
    val: 1,
    toString: function(){
        return a.val++
    },
    // valueOf: function(){
    //     return a.val++
    // }
}

// 利用 Proxy，可以将读取属性的操作（get），转变为执行某个函数，从而实现属性的链式操作
// const a = new Proxy({ val: 1}, {
//     get(target){
//         return () => target.val++
//     }
// })

console.log(a == 1 && a ==2 && a == 3) // true

```
