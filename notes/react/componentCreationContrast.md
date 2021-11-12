# 组件创建对比， HOC、RenderProps 和 Hooks

## HOC

> 高阶组件是接受一个组件为参数，返回新组件的组件

```JavaScript

function withSubscription(WrappedComponent){
    return class extends React.Component {
        constructor(props){
            super(props);
            this.state = {
                data: ''
            }
        }

        setData = data => this.setState({ data })

        render(){
            return (
                <>
                    <WrappedComponent setData={this.setData} {...this.state} {...this.props}/>
                </>
            )
        }
    }
}
```

### 优点

- 提取公共逻辑，不会影响内层组件的状态
  ，降低耦合度

### 缺点

- 使用多个高阶组件会层层嵌套，即使使用装饰器也不优雅
- state/内部方法相同的话会进行覆盖，除非每个组件定义一个唯一的对象包裹需要传递的内容
- 数据源头不清晰，难以知道这个参数来自哪里

## renderProps

> 组件接受一个函数，这个函数获取组件的 state 实现渲染逻辑

```JavaScript

 class RenderPropsWrapperComponent extends Component<any, any> {
    constructor(props) {
        super(props.state)
        this.state = {
            data: ''
        }
    }

    setData = data => {
        this.setState({ data })
    }
    render() {
        return <div>{this.props.render({ state: this.state, setData: this.setData })}</div>
    }
}

const MyComponent = () => {
    return <RenderPropsWrapperComponent render={({state, setData}) => {
        return <div onClick={() => setData('ddd')}>点击改变 data: {state.data}</div>
    }}/>
}

```

### 优点

- 清楚知道这个 state 数据源来自哪里

### 缺点

- 使用起来会有嵌套地狱
- 不能在 return 外使用数据

## Hooks

> 不是用 class 的情况下可以使用 state

### 优点 & 缺点 见 [hooks](./hooks.md)
