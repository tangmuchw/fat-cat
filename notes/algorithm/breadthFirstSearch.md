# 广度优先遍历（Breadth-First-Search）:

<br />

## 特点

- 广度优先遍历需要先记录所有的节点，**占用空间大**
- 采用**队列的形式**，即先进先出
- BFS 可用来解决计算机游戏（例如即时策略游戏）中找寻路径的问题

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

// 创建一个执行队列，当队列为空时
const breadthFirstSearch = (data) => {
    let result = []
    let queue = data

    while(queue.length > 0){
        //  数据过于复杂时，需要进行深拷贝
        [...queue].forEach(child => {
            queue.shift()
            result.push(child.name)

            child.children && (queue.push(...child.children))
        })
    }

    return result
}

const rlt = breadthFirstSearch(data)
console.log(rlt) // ["a", "a2", "b", "c", "d", "b2", "c2", "d2", "e", "f", "g", "e2", "f2", "g2"]

```
