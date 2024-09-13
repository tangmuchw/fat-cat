# React 17.x 为什么要废弃 ComponentWillMount、ReceiveProps 和 Update 这三个生命周期

componentWillMount 是 React 组件的生命周期方法之一，它在组件即将被挂载到 DOM 中之前被调用。在该方法中，你可以执行一些准备工作，例如初始化状态、订阅事件或者发送网络请求等。

componentWillReceiveProps 是 React 组件的生命周期方法之一，它在组件接收到新的 props 之前被调用。在这个方法中，你可以根据新的 props 来更新组件的状态或执行其他一些操作。

componentWillUpdate 是 React 组件的生命周期方法之一，它在组件即将更新并且重新渲染到 DOM 中之前被调用。在该方法中，你可以执行一些与组件更新相关的操作，例如根据新的 props 或 state 进行一些计算或准备工作

在 React 中，componentWillMount、componentWillReceiveProps 和 componentWillUpdate 这三个生命周期方法被废弃，主要是出于以下几个原因：

-   **异步渲染的引入**：React 16 开始引入了异步渲染的概念，以提高性能和用户体验。在异步渲染模式下，组件的生命周期方法不再保证同步执行。因此，之前的生命周期方法可能会在不可预测的时机被触发，导致不一致的行为和难以调试的问题。为了解决这个问题，React 弃用了一些生命周期方法，以确保组件的行为更加可预测和稳定。
-   新的生命周期方法替代：React 推荐使用新的生命周期方法来替代被废弃的方法，例如 componentDidMount、componentDidUpdate 和 getDerivedStateFromProps。这些新的方法更符合 React 的设计理念，并且能够更好地满足开发者的需求。
