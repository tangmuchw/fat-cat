# basic types（基本类型）
>> 最简单的数据单元：数字，字符串，结构体，布尔值，枚举类型

## 布尔值

```JavaScript
 let isDone: boolean = false
```


## 数字

```JavaScript
 let decLiteral: number = 6
```


## 字符串

```JavaScript
 let name: string = 'smith'
```


## 数组

```JavaScript
 let list: number[] = [1, 2, 3]

 let list: Array<number> = [1, 2, 3]
```


## 元组（Tuple）

```JavaScript
 // Declare a tuple type
 let x: [string, number]

 // Initialize it
 x = ['hello', 10] // OK

 // Initialize it incorrectly
 x = [10, 'hello'] // Error
```


## 枚举
>> enum类型是对JavaScript标准数据类型的一个补充。 像C#等其它语言一样，使用枚举类型可以为一组数值赋予友好的名字
- 默认情况下，从**0**开始为元素编号

```JavaScript
 enum Color {Red = 1, Green, Blue}
 let colorName: string = Color[2];

 console.log(colorName);  // 显示'Green'因为上面代码里它的值是2
```


## Any
>> 为那些在编程阶段还不清楚类型的变量指定一个类型

```JavaScript
 let notSure: any = 4;
 notSure = "maybe a string instead";
 notSure = false; // okay, definitely a boolean
```

## Void
>> 表示没有任何类型

```JavaScript
 function warnUser(): void {
    console.log("This is my warning message");
 }
```

## Null 和 undefined


## Never
>> never类型表示的是那些永不存在的值的类型
- 例如， never类型是那些总是会抛出异常或根本就不会有返回值的函数表达式或箭头函数表达式的返回值类型
```JavaScript
// 返回never的函数必须存在无法达到的终点
function error(message: string): never {
    throw new Error(message);
}

// 推断的返回值类型为never
function fail() {
    return error("Something failed");
}

// 返回never的函数必须存在无法达到的终点
function infiniteLoop(): never {
    while (true) {
    }
}
```

## Object
>> **object**表示非原始类型

```JavaScript
declare function create(o: object | null): void
```


## 类型断言
- “尖括号”语法
```JavaScript
let someValue: any = 'this is a string'
let strLength: number = (<string>someValue).length
```

- as 语法（ts中使用jsx， 只有as语法断言是被允许的）
```JavaScript
let someValue: any = 'this is a string'
let strLength: number = (someValue as string).length
```