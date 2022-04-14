# 给出 n 个字母（小写字母从 a 到 z），找出出现次数最多的字母，输出该字母

```JavaScript
// 以空间换时间
const getMostOccurrenceLetter = (str) => {
    const result = new Array(26).fill(0)
    const strLen = str.length
    for(let i = 0; i < strLen; i++) {
        result[str[i].charCodeAt() - 97]++
    }

    let maxCount = 0,
        charCodes = []

    const resultLen = result.length
    for(let i = 0; i < resultLen; i++) {
        if(result[i] > maxCount) {
            maxCount = result[i]
        }
    }

     for(let i = 0; i < resultLen; i++) {
        if(result[i] === maxCount) {
            charCodes.push(i)
        }
    }

    return charCodes.map(v => String.fromCharCode(v + 97))

}

console.log(getMostOccurrenceLetter('aaaabbbcccsssddd')) // ['a']

```
