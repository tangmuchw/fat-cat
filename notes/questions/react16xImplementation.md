# 简单说一下 react 16.x 执行过程

- jsx 经过 babel 转变成 render 函数
- create update
- enqueueUpdate
- scheduleWork 更新 expirationTime
- requestWork
- workLoop 大循环
- Effect List
- commit

**待扩展对应细节...**
