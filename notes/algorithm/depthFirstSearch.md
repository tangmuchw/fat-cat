# 深度优先遍历（Depth-First-Search）:

## 特点

- 深度优先遍历不需要记住所有的节点，所以**占用空间少**
- 深度优先遍历有回溯的操作，没有路走了需要回头，所以相对而言**时间会长一点**
- 采用**堆栈的形式**，即先进后出
- DFS 应用举例如 DOM 树的遍历

```Javascript
const data = [
    {
        name: 'a',
        children: [
            { name: 'b', children: [{ name: 'e' }] },
            { name: 'c', children: [{ name: 'f' }] },
            { name: 'd', children: [{ name: 'g' }] },
        ],
    },
    {
        name: 'a2',
        children: [
            { name: 'b2', children: [{ name: 'e2' }] },
            { name: 'c2', children: [{ name: 'f2' }] },
            { name: 'd2', children: [{ name: 'g2' }] },
        ],
    }
]

// 递归
const depthFirstSearch = (data) => {
    let result = []

    const mapChild = (dt = {}) => {
        const { name. children } = dt

        result.push(name)
        children && children.forEach(mapChild)
    }

    data.forEach(mapChild)

    return result
}

const rlt = depthFirstSearch(data);
console.log(rlt); // ["a", "b", "e", "c", "f", "d", "g", "a2", "b2", "e2", "c2", "f2", "d2", "g2"]

```
