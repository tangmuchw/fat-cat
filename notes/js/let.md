# let

>> babel在let定义的变量前加了道下划线，避免在块级作用域外访问到该变量

```JavaScript
    // 源代码
    for (let i = 0; i < 10; i++){
        console.log(i)
    }

    console.log(i)


    // babel 转化后
     for (let _i = 0; i < 10; i++){
        console.log(i)
    }

    console.log(i)
```