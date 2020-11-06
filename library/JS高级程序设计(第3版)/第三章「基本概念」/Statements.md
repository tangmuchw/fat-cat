[toc]

# Statements 语句

## if

## do-while

## while

## for

## for-in

```JavaScript
const object = { a: 1, b: 2, c: 3 };

for (const property in object) {
  console.log(`${property}: ${object[property]}`);
}

// expected output:
// "a: 1"
// "b: 2"
// "c: 3"
```

## for-of

```JavaScript
const array1 = ['a', 'b', 'c'];

for (const element of array1) {
  console.log(element);
}
// expected output: "a"
// expected output: "b"
// expected output: "c"
```

## label

## break & continue 语句

## with

> 将代码的作用域设置到一个特定的对象中。 语法: with (expression) statement

```JavaScript
var qs = location.search.substring(1)
var hostName = location.hostname
var url = location.href

with(location){
  var qs = search.substring(1)
  var hostName = hostname
  var url = href
}

```

## switch
