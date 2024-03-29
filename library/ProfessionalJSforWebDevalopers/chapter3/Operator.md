[toc]

# Operator 操作符

## 一元操作符

> ++， --， +， -

## 位操作符

- 按位非 (~): 操作数的负值减 1；~-1 => 0
- 按位与 (&): 只在两个数值的对应位都是 1 时才返回 1， 任何一位是 0， 结果都是 0
- 按位或 (|): 有一个位是 1 的情况就返回 1，而只有在两个位都是 0 的情况下才返回 0
- 按位异或 (^): 在两个数字对应位上只有一个 1 时才返回 1， 如果对应的两位都是 1 或是 0 ，则返回 0
- 左移 (<<): 将数值的所有位向左移动指定的位数, eg: 2 >> 5 // 64
- 右移 (<<): 将数值的所有位向右移动指定的位数

## 布尔操作符

- 逻辑非 (!)
- 逻辑与 (&&)
- 逻辑或 (||)

## 乘性操作符

- 乘法 (\*)
- 除法 (\/)
- 求模 (\%)

## 加性操作符

- 加法 (+)
- 加法 (-)

## 关系操作符

- <
- \>
- <=
- \>=

## 相等操作符

### 相等和不相等 (==, !=)

> 这两个操作符都会现转换操作数(强制转型)，然后再比较它们的相等性 => 转成基本类型值 -> 最终以数值的方法比大小

### Exercise

- "NaN" == NaN ?
- undefined == 0 ?
- null == 0 ?
- undefined == undefined ?
- "5" == 5 ?

### 全等和不全等 (===, !==)

> 全等和不全等在比较相等性，除了比较值是否相等之外，还要比较其数据类型是否相等

## 条件操作符

- ?:

## 赋值操作符

- =, \*=, +=, /=, -=

## 逗号操作符

- , => var num1 = 1, num2 = 2;

## 可选链操作符

- ?.

## Q&A

> (1) '1012' > '20' 与 '1012' - '20' > 0 的结果? => [答案](/notes/js/>.md)

> (2) 0.1 + 0.2 不等于 0.3，why? => [答案](/notes/questions/roundOff.md)

> (3) [] == ![] 与 {} == !{} 的结果? => [答案](/notes/js/==.md)

---

```JavaScript
 "NaN" == NaN // false
 undefined == 0 // false
 null == 0 // false
 undefined == undefined // true
 "5" == 5 // true
```
