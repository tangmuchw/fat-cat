# 编辑距离。给定两个单词 word1 和 word2，计算出将 word1 转换成 word2 所使用的最少操作数。可以对一个单词进行如下操作：1.插入一个字符 2.删除一个字符 3.替换一个字符

> 输入：word1='horse', word2='ros'
> 输出：3
> 解释： horse => rorse (将'h'替换'r') => rose (删除'r') => ros (删除'e')

| \*  | ""  | r   | o   | s   |
| --- | --- | --- | --- | --- |
| ""  | 0   | 1   | 2   | 3   |
| h   | 1   | 1   | 2   | 2   |
| o   | 2   | 2   | 1   | 3   |
| r   | 3   | 2   | 2   | 2   |
| s   | 3   | 3   | 3   | 2   |
| e   | 3   | 4   | 4   | 3   |

- add = dp[i, j - 1], 代表插入一个字符
- delete = dp[i - 1, j]，代表删除一个字符
- replace = dp[i - 1, j - 1]，代表替换一个字符
- dp = 1 + min(add, delete, replace)

```JavaScript
    const getMinDistance = (word1 = 'horse', word2 = 'ros') => {
        let len1 = word1.length
        let len2 = word2.length

        let dp = [[]]

        // 默认第 0 行 和 第 0 列字符变为空字符为被删除的次数
        for (let i = 0; i <= len2; i++) dp[0][i] = i
        for (let j = 1; j <= len1; j++) {
            dp[j] = []
            dp[j][0] = j
        }

        for (let i = 1; i <= len1; i++) {
            for (let j = 1; j <= len2; j++) {
                if (word1[i - 1] === word2[j - 1]) dp[i][j] = dp[i - 1][j - 1]
                else dp[i][j] = Math.min(
                    dp[i - 1][j - 1],
                    dp[i - 1][j],
                    dp[i][j - 1]
                ) + 1
            }
        }


        return dp[len1][len2]
    }

    console.log(getMinDistance('horse', 'ros')) // 3
```
