# 将 'aabbcca' 转变成 'a2b2c2a1'

```JavaScript
const transferStr = (str) => {
    const len = str.length

    let lastChar = str[0],
        count = 1,
        newStr = ''

    for (let i = 1; i <= len; i++) {
        if (str[i] == lastChar) count++
        else {
            newStr = `${newStr}${lastChar}${count}`
            count = 1
            lastChar = str[i]
        }
    }

    return newStr
}

```
