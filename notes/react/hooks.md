# hooks

## hooks 优点

- 简洁：React Hooks 解决了 HOC 和 Render Props 的嵌套问题,更加简洁
- 解耦: React Hooks 可以更方便地把 UI 和状态分离,做到更彻底的解耦
- 组合: Hooks 中可以引用另外的 Hooks 形成新的 Hooks,组合变化万千
- 函数友好: React Hooks 为函数组件而生，从而解决了类组件的几大问题

## hooks 缺点

- 额外的学习成本
- 写法上有限制（不能出现在条件、循环中），并且写法限制增加了重构成本
- 破坏了 PureComponent、React.memo 浅比较的性能优化效果（为了取最新的 props 和 state，每次 render()都要重新创建事件处函数）
- 在闭包场景可能会引用到旧的 state、props 值
- React.memo 并不能完全替代 shouldComponentUpdate（因为拿不到 state change，只针对 props change）
