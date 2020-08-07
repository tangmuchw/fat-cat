# 深拷贝

```JavaScript
// 简单的深拷贝
const simpleDeepClone = (origin) => {
    let originProto = Object.getPrototypeOf(origin)
    return Object.assign(Object.create(originProto), origin)
}


// 数组或对象的深拷贝
const deepClone = (obj, newObj) => {
    let temp = newObj || {}

    for(let key in obj){
        if(typeof obj[key] === 'object'){
            temp[key] = obj[key].constructor === Array ? [] :{}
            deepClone(obj[key], temp[key])
        } else {
            temp[key] = obj[key]
        }
    }

    return temp
}
```