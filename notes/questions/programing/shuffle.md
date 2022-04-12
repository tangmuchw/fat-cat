# 洗牌算法

```JavaScript
 Array.prototype.shuffle = function(){
     let me = this

     for(let i = me.length - 1; i >= 0; i--){
         let randomIdx = Math.floor(Math.random()*(i+1))
         let temp = me[randomIdx]

         me[randomIdx] = me[i]
         me[i] = temp
     }

     return me
 }

 console.log([1,2,3,4,5,6,7,8].shuffle())
```
