# 买卖股票的最佳时机 II

> 给定一个数组 prices ，其中  prices[i] 是一支给定股票第 i 天的价格。

设计一个算法来计算你所能获取的最大利润。你可以尽可能地完成更多的交易（多次买卖一支股票）。

注意：你不能同时参与多笔交易（你必须在再次购买前出售掉之前的股票）。

## 示例

> 输入: prices = [7,1,5,3,6,4]
> 输出: 7
> 解释: 在第 2 天（股票价格 = 1）的时候买入，在第 3 天（股票价格 = 5）的时候卖出, 这笔交易所能获得利润 = 5-1 = 4 。
>   随后，在第 4 天（股票价格 = 3）的时候买入，在第 5 天（股票价格 = 6）的时候卖出, 这笔交易所能获得利润 = 6-3 = 3 。

## 解析

- 比较简单的解法，即求上升区间的高度和

```JavaScript

const maxProfit = (prices) => {
    const len = prices?.length
    if(!len) return 0

    let max = 0,
        profit = 0

    for(let i = 0; i < len - 1; i++) {
        profit = prices[i + 1] - prices[i]
        if(profit > 0) max+=profit
    }

    return max
}

```

- 使用动态规划
  - 建立数学模型

```JavaScript

const maxProfit = (prices) => {
    const len = prices?.length
    if(!len) return 0

    let noHold = 0 // 未持有股票
    let hold = - prices[0] // 持有股票

    for(let i = 1; i < len - 1; i++) {
        // 未持有与卖出相比, 先购入
        noHold = Math.max(noHold, hold + prices[i])
        // 持有与刚购入相比，再卖出
        hold = Math.max(hold, noHold - prices[i])
    }

    // 最后一天肯定是手里没有股票的时候利润才会最大，
    // 所以这里返回的是 noHold
    return noHold

}

```
