# function 函数

## 理解参数

- 可以通过 arguments 对象来访问参数数组
- arguments 对象可以与命名参数一起使用
- 没有传递值的命名参数将自动被赋予 undefined 值
- **严格模式下, 没有传递值的命名参数，使用 arguments 无法改变其被自动赋予为 undefined 值 **

> Noticing: ECMAScript 中的所有参数传递都是值，不是通过引用传递参数

### All in all

- 基本数据类型作为函数参数 a，相当于你复制了份内容，不会影响 a
- 复杂数据类型作为函数参数 b，虽然传递的方式是值传递，但传递的对应内存地址，也就是说
  函数里可以直接改变 b

## 重载

- 函数没有重载

## Q&A

1.

```JavaScript
var a = [1,2,3];

var b = a;

a = [4,5,6];

console.log(b) // [1, 2, 3]

```

2.

```JavaScript
var a = [1,2,3];

var b = a;

a.pop();

console.log(b) // [1, 2]

```

3.

```JavaScript
var a = 1;

var obj = {
    b: 2
};

var fn = function () {};
fn.c = 3;

function test(x, y, z) {
    x = 4;
    y.b = 5;
    z.c = 6;
    return z;
}
test(a, obj, fn);

console.log(a + obj.b + fn.c) // 12

```
