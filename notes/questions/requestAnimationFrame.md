# 对 requestAnimationFrame 的理解

> 告诉浏览器——你希望执行一个动画，并且要求浏览器在下次重绘之前调用指定的回调函数更新动画。该方法需要传入一个回调函数作为参数，该回调函数会在浏览器下一次重绘之前执行

- 顾名思义就是**请求动画帧**
- 其最大优势是**由系统来决定回调函数的执行时机**
- 与 react 16.x 的更新 dom 机制有关
