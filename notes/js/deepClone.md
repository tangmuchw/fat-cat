# 深拷贝

```JavaScript
// 简单的深拷贝
const simpleDeepClone = (origin) => {
    let originProto = Object.getPrototypeOf(origin)
    return Object.assign(Object.create(originProto), origin)
}


// 数组或对象的深拷贝
const deepClone = (origin, newObj) => {
    let temp = newObj || {}

    for(let key in origin){
        if(typeof origin[key] === 'object'){
            temp[key] = origin[key].constructor === Array ? [] :{}
            deepClone(origin[key], temp[key])
        } else {
            temp[key] = origin[key]
        }
    }

    return temp
}
```