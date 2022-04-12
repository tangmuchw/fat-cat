# compareVersion(version1, version2) {} 版本号可能是 7.5.0 或者 1.12 这种格式，输出较大的版本号

```JavaScript
    const compareMaxVersion = (version1, version2) => {
        const versionList1 = version1.split('.')
        const versionList2 = version2.split('.')
        const maxLen = Math.max(version1.length, version2.length)

        for(let i = 0; i < maxLen; i++){
            let v1 = i < version1.length ? versionList1[i] : 0
            let v2 = i < version2.length ? versionList2[i] : 0

            if(v1 === v2) continue

            if(v1 > v2) return 1 // version1大
            else return -1  // version2大
        }


        return 0 // 相等
    }

    console.log(compareMaxVersion('7.5.0', '1.12'))
```
