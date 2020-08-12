## 对 requestAnimationFrame 的理解
>> 告诉浏览器——你希望执行一个动画，并且要求浏览器在下次重绘之前调用指定的回调函数更新动画。该方法需要传入一个回调函数作为参数，该回调函数会在浏览器下一次重绘之前执行
- 顾名思义就是**请求动画帧**
- 其最大优势是**由系统来决定回调函数的执行时机**
- 与react 16.x 的更新dom机制有关

## package.json 中的peerDependencies
>> 指定当前组件的依赖以及其版本。如果组件使用者在项目中安装了其他版本的同一依赖，会提示报错。**起一个检查依赖版本报错机制**

## 虚拟DOM的好处
>> 减少了同一时间内的页面多处内容修改所触发的浏览器reflow和repaint的次数，可能把多个不同的DOM操作几种减少到了几次甚至一次，优化了触发浏览器reflow和repaint的次数

## 编程 compose 实现
```JavaScript
/**
 * 解析实现
 * foo = (num) => add(multiply(num))
*/

const compose = (...funcs) => {
    if(!funcs.length) return (num) => { console.log(num) }

    return funcs.reduce((a, f) => (...arg) => a(f(...arg)))
}

// 问题描述
const add = num => num  + 10
const multiply = num => num * 2
const foo = compose(multiply, add)
console.log(foo(5)) // 30
```
