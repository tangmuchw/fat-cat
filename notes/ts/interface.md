# interface （接口）
>> 在ts里，接口的作用就是为这些类型命名和为你的代码或第三方代码定义契约

```JavaScript
interface LabelledValue {
  label: string;
}

function printLabel(labelledObj: LabelledValue) {
  console.log(labelledObj.label);
}

let myObj = {size: 10, label: "Size 10 Object"};
printLabel(myObj);
```

## 可选属性
```JavaScript
interface SquareConfig {
  color?: string;
  width?: number;
}
```

## 只读属性
```JavaScript
interface Point {
  readonly x: number;
  readonly y: number;
}

let p1: Point = { x: 10, y: 20 }
p1.x = 5 // Error
```