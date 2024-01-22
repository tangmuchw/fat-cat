# 变量声明

> 基本类型

-   Numbers(int, double)
-   Strings(String)
-   Booleans(bool)
-   Records((value1, value2))
-   Lists(List, also known as arrays)
-   Sets(Set): 是一个无序的，元素唯一的集合
-   Maps(Map): 是一个无序的 key-value （键值对）集合, **与 JavaScript 不同，Dart 对象不是 Map**
-   Runes(Runes; often replaced by the characters API)
-   Symbols(Symbol)
-   The value null(Null)

> 其他类型

-   Object: 除了 Null 以外的所有 Dart 类的超类
-   Enum: 所有枚举的超类
-   Future 和 Stream: 用于异步处理
-   Iterable: 用于 for-in 循环和同步生成器函数
-   Never: 指示表达式永远不能成功地完成求值。最常用于总是抛出异常的函数
-   dynamic: 表示要禁用静态检查。通常你应该使用 Object 或 Object?代替
-   void: 表示该值永远不会被使用。通常用作返回类型。

## var

> 可以接收任何类型的变量，但最大的不同是 Dart 中 var 变量一旦赋值，类型便会确定，则不能再改变其类型

```Dart
var t = "hi world";
// 下面代码在dart中会报错，因为变量t的类型已经确定为String，
// 类型一旦确定后则不能再更改其类型。
t = 1000;
```

## late

> 使用场景

-   声明一个在声明后初始化的非空变量。
-   惰性初始化变量。

```Dart
late String description;

void main() {
  description = 'Feijoada!';
  print(description);
}

// This is the program's only call to readThermometer().
late String temperature = readThermometer(); // Lazily initialized.

```

## dynamic 和 Object 对象

> <code>dynamic</code> 与 <code>Object</code> 声明的变量都可以赋值任意对象，且后期可以改变赋值的类型，这和 <code>var</code> 是不同的

-   Object: 是 Dart 所有对象的根基类
-   dynamic: dynamic 与 Object 不同的是 dynamic 声明的对象编译器会提供所有可能的组合，而 Object 声明的对象只能使用 Object 的属性与方法, 否则编译器会报错

## final 和 const

-   final: 只能被设置一次
-   const: 编译时的 常量

## 空安全

## Records(记录)

```Dart
main() {
    // Returns multiple values in a record:
    (String, int) userInfo(Map<String, dynamic> json) {
    return (json['name'] as String, json['age'] as int);
    }

    final json = <String, dynamic>{
    'name': 'Dash',
    'age': 10,
    'color': 'blue',
    };

    // Destructures using a record pattern:
    var (name, age) = userInfo(json);

    /* Equivalent to:
    var info = userInfo(json);
    var name = info.$1;
    var age  = info.$2;
    */
}
```

## Collections（集合）

-   List: 在 Dart 中，数组是 List 对象

```Dart
main() {
    var list = [
        'Car',
        'Boat',
        'Plane',
        ];

    // 要创建一个编译时常量列表，在list字面量之前添加const:
    var constantList = const [1, 2, 3];
    // constantList[1] = 1; // This line will cause an error.
}

```

-   Sets: Dart 中的 set 是唯一项的无序集合。集合的 Dart 支持由集合字面量和 set 类型提供。

```Dart
main() {
    var halogens = {'fluorine', 'chlorine', 'bromine', 'iodine', 'astatine'};

    var elements = <String>{};
    elements.add('fluorine');
    elements.addAll(halogens);
    assert(elements.length == 5);
}
```

-   Maps: 一般来说，映射是一个关联键和值的对象。键和值都可以是任何类型的对象。每个键只出现一次，但是您可以多次使用相同的值。映射的 Dart 支持由映射字面值和 map 类型提供。

```Dart
main() {
   var gifts = Map<String, String>();
    gifts['first'] = 'partridge';
    gifts['second'] = 'turtledoves';
    gifts['fifth'] = 'golden rings';

    var nobleGases = {
        2: 'helium',
        10: 'neon',
        18: 'argon',
    };
}

```

## Typedefs

> 类型别名(通常称为 typedef，因为它是用关键字 typedef 声明的)是引用类型的一种简明方式。

```Dart
main() {
  typedef IntList = List<int>;
  IntList il = [1, 2, 3];
}

```
