# JSON 和序列化数据

## 定义模型

models/person.dart

```Dart
import 'package:json_annotation/json_annotation.dart';
part 'address.g.dart';

@JsonSerializable()
class Address {
  String street;
  String city;

  Address(this.street, this.city);

  factory Address.fromJson(Map<String, dynamic> json) =>
      _$AddressFromJson(json);
  Map<String, dynamic> toJson() => _$AddressToJson(this);
}

```

## 为中大型项目使用代码生成

> 利用代码生成的 JSON 序列化数据，意味着可以通过外部的库生成编码模板。在一些初始化设置后，你可以运行文件监听程序，来从你的模型类生成代码。例如，**json_serializable** 和 **built_value** 就是这类的库。

### 使用 json_serializable 生成序列化 JSON 数据

#### 1.定义 JSON 模型

```Dart
import 'package:json_annotation/json_annotation.dart';

/// This allows the `User` class to access private members in
/// the generated file. The value for this is *.g.dart, where
/// the star denotes the source file name.
part 'user.g.dart';

/// An annotation for the code generator to know that this class needs the
/// JSON serialization logic to be generated.
@JsonSerializable()
class User {
  User(this.name, this.email);

  String name;
  String email;

  /// A necessary factory constructor for creating a new User instance
  /// from a map. Pass the map to the generated `_$UserFromJson()` constructor.
  /// The constructor is named after the source class, in this case, User.
  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);

  /// `toJson` is the convention for a class to declare support for serialization
  /// to JSON. The implementation simply calls the private, generated
  /// helper method `_$UserToJson`.
  Map<String, dynamic> toJson() => _$UserToJson(this);
}
```

#### 2.运行代码生成工具

-   一次性代码生成: flutter pub run build_runner build --delete-conflicting-outputs

    -   --delete-conflicting-output: 可选，会在生成代码冲突的时候，删除原来的代码，重新生成

-   持续生成代码: flutter pub run build_runner watch

-   运行以上命令，源代码生成器会创建一个名为 user.g.dart 的文件，它包含了所有必须的序列化数据逻辑。你不必再编写自动化测试来确保序列化数据奏效。现在 由库来负责 确保序列化数据能正确地被转换

### 在后台处理 JSON 数据解析

-   Dart 应用通常只会在单线程中处理它们的工作。并且在大多数情况中，这种模式不但简化了代码而且速度也够快，基本不会出现像动画卡顿以及性能不足这种「不靠谱」的问题。

-   但是，当你需要进行一个非常复杂的计算时，例如解析一个巨大的 JSON 文档。如果这项工作耗时超过了 16 毫秒，那么你的用户就会感受到掉帧

-   为了避免掉帧，像上面那样消耗性能的计算就应该放在后台处理。在 Android 平台上，这意味着你需要在不同的线程中进行调度工作。而在 Flutter 中，你可以使用一个单独的 **Isolate**
