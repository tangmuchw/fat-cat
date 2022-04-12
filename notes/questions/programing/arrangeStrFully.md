# 字符串的全排列

> 输入：'abc'
> 输出：['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

```JavaScript
const arrangeStr = (str) => {
    const len = str.length
    if(len <= 1) return [str]

    if(len === 2) return [`${str[0]}${str[1]}`,`${str[1]}${str[0]}`]

    let result = []
    for(let i = 0; i < len; i++) {
        let pivotChar = str[i],
         nextStr = str.slice(0, i) + str.slice(i + 1),
         newResult = arrangeStr(nextStr)

        const newLen = newResult.length
        for(j = 0; j < newLen; j++){
            result.push(`${pivotChar}${newResult[j]}`)
        }

    }

    return result
}

```
