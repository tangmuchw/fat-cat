# JS 简单实现：根据奖品权重计算中奖概率实现抽奖

-   根据权重数组的和值（weightSum），在每次抽奖时生成一个权重随机数（weightRandom），这个权重随机数（weightRandom）是介于 0-weightSum （权重和值）之间的，本文示例设置的权重数组和值为 100，表示生成的权重随机数是介于 0-100 之间的
-   然后让这个权重随机数（weightRandom）去和权重数组中的所有元素值作比较，计算这个权重随机数（weightRandom）位于哪两个奖项之间，符合哪条中奖规则，对应哪个奖项名称

```JavaScript
// 设置奖项名称、权重
const prizes = ['一等奖', '二等奖', '三等奖', '未中奖']
const weights = [1, 5, 20, 74]

// 计算权重之和
const weightSum = weights.reduce((a, sum) => sum + a, 0)

// 根据权重和值 weightSum, 生成介于 0-weightSum 之间的权重随机数
const lottery = () => {
    // 生成介于 0-weightSum 之间的权重随机数, 假设 30
    const random = Math.random() * weightSum

    const nextWeights = weights.concat(random) // [1, 5, 20, 74, 30]
    const sortedWeights = nextWeights.sort((a, b) => a - b) // [1, 5, 20, 30, 74]

    // 索引权重随机数的数组下标
    const randomIdx = sortedWeights.indexOf(random) // 3
    const prizeIdx = Math.min(randomIdx, prizes.length - 1) // 3

    // 本次抽奖的结果
    return prizes[prizeIdx]
}

```
