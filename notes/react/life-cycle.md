# React15.x 生命周期

React 的生命周期主要分为三个阶段：MOUNTING、RECEIVE_PROPS、UNMOUNTING

- 组件挂载时（组件状态的初始化，读取初始 state 和 props 以及两个生命周期方法，只会在初始化时运行一次）
    - componentWillMount 会在 render 之前调用
    - componentDidMount 会在 render 之后调用

- 组件更新时（组件的更新过程是指父组件向下传递 props 或者组件自身执行 setState 方法时发生的一系列更新的动作）
    - 组件自身的 state 更新，依次执行
        - shouldComponentUpdate（会接收需要更新的 props 和 state，让开发者增加必要的判断条件，在其需要的时候更新，不需要的时候不更新。如果返回的是 false，那么组件就不再向下执行生命周期方法。）
        - componentWillUpdate
        - render（能获取到最新的 this.state)
        - componentDidUpdate（能获取到最新的 this.state)
    - 父组件更新 props 而更新
        - componentWillReceiveProps
        - shouldComponentUpdate
        - componentWillUpdate
        - render
        - componentDidUpdate

- 组件卸载时
    - componentWillMount（我们常常会在组件的卸载过程中执行一些清理方法，比如事件回收、清空定时器）
