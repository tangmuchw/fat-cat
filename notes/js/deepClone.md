# 深拷贝

## Object.assign

> > 缺点：对于 Object.assign()而言, 如果对象的属性值为简单类型（string， number），通过 Object.assign({},srcObj);得到的新对象为‘深拷贝’；如果属性值为对象或其它引用类型，那对于这个对象而言其实是浅拷贝的

```JavaScript
// 简单的深拷贝
const simpleDeepClone = (origin) => {
    let originProto = Object.getPrototypeOf(origin)
    return Object.assign(Object.create(originProto), origin)
}

```

## 普通函数(数组或对象的深拷贝)

> > 缺点： 函数无法深拷贝，并且数据太多进行深拷贝，容易导致堆栈溢出

```JavaScript
// 数组或对象的深拷贝
// for-in origin
// typeof origin[key] === 'object'
// 检查 origin[key].constructor === Array
// 递归
const deepClone = (origin, newObj) => {
    let temp = newObj
        ? newObj
        : origin.constructor === Array ? {}: []

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

## 更完善版

```JavaScript
    const isTypeofObject = (origin) => {
        const type = typeof origin
        return type !== null && (type === 'object' || type === 'function')
    }


    const getPrototypeStr = (origin) => {
        if(origin === null) return '[object null]'
        if(origin === undefined) return '[object undefined]'

        return Object.prototype.toString.call(origin)
    }


    const cloneRegExp = (regExp) => {
        let rlt = new regExp.constructor(regExp.source, /\w*$/.exec(regExp))

        rlt.lastIndex = regExp.lastIndex
        return rlt
    }

    const getCopyReferenceType = (origin, originPrototypeStr) => {
        // 需要处理： arrayBuffer， init32array, dateview等
        switch(originPrototypeStr){
            case '[object RegExp]':
             return cloneRegExp(origin)
            default:
             return {}
        }
    }


    const advanceDeepClone = (origin, wMap = new WeakMap()) => {
        if(!isTypeofObject(origin) || typeof origin === 'function') return origin

        // 处理引用类型
        let  temp = Array.isArray(origin) ? [] : getCopyReferenceType(origin, getPrototypeStr(origin))


        // 处理循环引用
        if(wMap.has(origin)) return wMap.get(origin)

        wMap.set(origin, temp)

        // for..in不会枚举Symbol的key
        // getOwnPropertySymbols
        for(let key in origin){
            temp[key] = advanceDeepClone(origin[key], wMap)
        }

        return temp
    }

```
