# 类型操作

## 泛型

> 带参数的类型

-   泛型约束

```Typescript
interface Lengthwise {
  length: number;
}

function loggingIdentity<Type extends Lengthwise>(arg: Type): Type {
  console.log(arg.length); // Now we know it has a .length property, so no more error
  return arg;
}
```

-   泛型参数默认值

```Typescript
declare function create(): Container<HTMLDivElement, HTMLDivElement[]>;
```

## keyof 类型运算符

> 使用 keyof 运算符创建新类型，keyof 运算符**采用对象类型并生成其键的字符串或数字字面联合**

```Typescript
type Point = { x: number; y: number };
type P = keyof Point;  // => type P = "x" | "y":
```

## typeof 类型运算符

> 使用 typeof 运算符创建新类型

```
let s = "hello";
let n: typeof s; // => let n: string
```

## 索引访问类型

> 使用 Type['a'] 语法访问类型的子集

```Typescript
type Person = { age: number; name: string; alive: boolean };
type Age = Person["age"]; // => type Age = number
```

## 条件类型

> 在类型系统中表现得像 if 语句的类型
> 表达式： SomeType extends OtherType ? TrueType : FalseType;

## 映射类型

> 通过映射现有类型中的每个属性来创建类型

-   映射修饰符：readonly 和 ? 分别影响可变性和可选性。
    映射类型建立在索引签名的语法之上，用于声明未提前声明的属性类型

```Typescript
type OnlyBoolsAndHorses = {
  [key: string]: boolean | Horse;
};
```

## 模板字面类型

> 通过模板字面字符串更改属性的映射类型

```Typescript
type EmailLocaleIDs = "welcome_email" | "email_heading";
```
