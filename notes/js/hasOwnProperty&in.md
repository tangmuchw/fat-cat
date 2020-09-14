# hasOwnProperty & in 的区别

## hasOwnProperty 
>> hasOwnProperty 只能判断是否是属于自身的属性，无法找到原型身上的属性（**只在属性存在于实例中时才返回true**）`


## in 原型上的属性也能找到（只要通过对象能访问到属性就返回true）


```JavaScript
 let person = {
     name: '小狗'
 }

 console.log(person.hasOwnProperty('name')) // true
 console.log(person.hasOwnProperty('hasOwnProperty')) // false

 console.log('name' in person) // true
 console.log('hasOwnProperty' in person) //true
```