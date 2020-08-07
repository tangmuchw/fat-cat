# 数组扁平化

- 可以直接使用es6中的<code>flat</code>方法

```JavaScript
const _flat = (list) => {
    if(!list && !Array.isArray(list)) {
        throw new TypeError('Not Array')
    }

    let arr = list

    while(arr.some(Array.isArray)) {
        arr = [].concat(...arr)
    } 
    
    return arr
}
```