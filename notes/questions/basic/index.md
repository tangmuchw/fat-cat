[toc]

# 箭头函数与普通函数区别？能不能作为构造函数？
- 最大的区别其实就是this指向
 + 箭头函数没有自己的this，箭头函数的this指向**在定义时候**继承**自外层的一个普通函数**的this，永远不会改变
- 箭头函数没有prototype， 所以箭头函数本身没有this
- 箭头函数不能作为构造函数使用
- 箭头函数不绑定arguments，取而代之用rest参数...代替arguments对象，来访问箭头函数的参数列表
 ```JavaScript
 const getRest = (...params) => { 
     console.log(params)
 }
 ```
- 箭头函数不能作Generator函数，不能使用yield关键字



