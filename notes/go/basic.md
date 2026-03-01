# go 基础

[toc]

## rune

rune 是 Go 为处理 Unicode 字符设计的一个类型别名，专门解决多字节字符（比如中文、日文、Emoji）的处理问题。

```go
type rune = int32
```

也就是说，rune 本质上就是 int32 类型，它的作用是存储一个Unicode 码点（Unicode Code Point）—— 每个 Unicode 字符都有唯一的码点，比如：
英文字母 'a' 的码点是 97（十进制）
中文字符 '中' 的码点是 20013（十进制）
Emoji '😀' 的码点是 128512（十进制）

```go
s := "Go语言😀"

// len(s) 是字节数：12
fmt.Printf("字节数：%d\n", len(s))

// 转成 []rune 后统计长度，是实际字符数：5
runeSlice := []rune(s)
fmt.Printf("实际字符数：%d\n", len(runeSlice))

// 取第4个字符（言）
fmt.Printf("第4个字符：%c\n", runeSlice[3]) // 输出：言
```

## for

### 枚举集合元素语句

当for语句带有range子句时，它可以通过循环依次从以下对象中取出所有元素：字符串（string）、数组（array）、切片（slice）、映射（map）以及通道（channel）中接收到的值。

```go
var str string = "abc"
for i, x := range str {
    fmt.Printf("%d --> %c\n", i, x)
}

```

### continue 与 break 语句

- continue语句会跳过当前一轮循环，并从下一轮循环的更新子句处开始执行。
- break 结束整个循环。

## 结构体

结构体类型可以封装字段列表，使之组成一个整体。

```go
type person struct {
    name string
    age unit8
}

p := person{} // 结构体的实例化
```

## 类型嵌套

Go 语言的类型不嗯呢该进行继承，但可以嵌套

## 类型断言

类型断言（type assertion） 对动态类型的变量进行分析，并返回变量所引用的真实对象。

```go
var x interface {} = float64(0.00123)
z, ok := x.(int8)
if ok {
    fmt.Printf("断言成功")
}
```

## 数组与切片

### 数组

#### 数组的初始化

```go
var x [n]T = [n]T{}
var x = [n]T{}
x := [n]T{}
// n 表示元素个数
```

#### *[n]T 与 [n]*T 的区别

- \*[n]T： 指针类型，存放类型为[n]T 的实力内存地址
- [n]\*T： 数组类型，其元素类型为指向 int 数值的指针类型(\* int)

```go
var d = [3]float32{0.001, 0.002, 0.003}
var pd = &d // 指针类型，其值是数组实例 d 的内存地址

var a, b, c = 50, 60, 70
var ax = [3]*int{&a, &b, &c} // 数组类型，其元素是 *int 类型

```

### 切片

- 切片（slice）与数组类型，但比数组灵活，可以在运行阶段动态地添加元素，在实际开发中用的比较多
- 切片类型的底层是通过数组来存储元素的。

#### 创建切片实例

```go
// 方式一
s := a[<L>, <H>] // 数组实例 a 中被提取的元素索引范围为 L <= index < H

// L 和 H 两个值省略，表示使用数组中的所有元素、


// 方式二，使用 make 函数
s := make([]byte, 30)

len(s) // 获取切片实例的长度，指切片中可以被访问的元素个数
cap(s) // 获取切片实例的容量，指应用程序为切片的基础数组所分配的空间，必须大于或等于长度

```

- 从同一个数组实例产生的所有切片实例都会共享数组中的元素，也就是说，当数组中的元素被更改，切片中对应的元素也会同步更新；反过来，如果切片中的元素被更改，数组中对应的元素也会同步更新。

## 映射和链表

### 映射

映射（map）是一种集合，它的每个元素都带有 key

- 同一个 map 对象中，元素的值可以重复出现
- key 必须是唯一的，可以是任意类型

```go
map[keyType]<valueType>

map[int]string // 元素类型为 string，key 类型为 int 的映射类型

```

### 双向链表

- 在双向链表中，每个元素都包含两个指针——分别指向前一个元素和后一个元素。
- 在双向链表中，随机取出一个元素都能找到它前面的或者后面的元素。
- 可以在双向链表的任意位置插入新元素
- 也可以在链表内部移动元素的位置

```go
type List struct {
    root Element // 此元素进作为占位符使用，在代码中不直接访问
    len int // 链表的长度，即包含元素的个数
}

type Element struct {
    // 指向前、后元素的指针
    next, prev *Element

    // 此元素所属的链表对象
    list  *List

    // 此元素中所存储的值
    Value interface {}

}
```

List 结构体公开方法：

- PushFront: 把新元素插入到链表的头部
- PushBack
- InsertBefore: 把新元素插入到指定元素的前面
- InsertAfter
- MoveBefore: 把一个元素移动到另一个元素的前面
- MoveAfter
- MoveToFront: 把某个元素移动到链表的首位
- MoveToBack
- Remove: 从链表中删除指定的元素
- Front: 获取链表中的第一个元素
- Back: 获取链表中的最后一个元素
- Len: 获取链表的长度
- PushFrontList: 复制另一个链表实例中的元素，并插入到当前链表的头部
- PushBackList

```go
var myList = list.New() // 创建链表实例
```

### 反射

反射技术可以在程序运行阶段获取对象实例的类型信息，也可以动态创建指定类型的实例。

- reflect 包

## 字符串处理

- Printf 通过格式控制符定制对象的输出形式
- Sprintf 用指定的格式控制符处理对象，并以字符串形式返回

### 控制符

- %s: 字符串出输出
- %d: 十进制数字输出
- %t: 支持将布尔类型的值转化为字符串“true”或“false”
- %T: 表示对象所属的类型名称
- %v: 使用默认的格式打印对象的值
    - %+v: 主要用于结构体对象。使用%v 只打印字段的值，若使用 %+v，则可以打印字段名称
    - %#v: 打印出来的对象值是一个有效的 Go 语言表达式

```go
type cat struct {
    name string
    age int
}

var c = cat{"Jim", 3}
fmt.Printf("%v", c) // {Jim 3}
fmt.Printf("%+v", c) // {name:Jim age：3}
fmt.Printf("%#v", c) // main.cat{name:"Jim",age:3}

```

### 设置除数内容的宽度

在格式控制符前加一个整数值，用于设置对象被格式化的文本长度

### 控制浮点数的精度

```go
var v = 13.1234567

fmt.Printf("精度为 2：% .2f", v) // 精度为 2：13.12

// 通过参数控制
var (
    width = 7
    prec = 2
)
fmt.Printf("% [1] * .[2] * f", width, prec, v)
```

### strings

```go
strings.Replace(s string, old string, new string, n int) string
strings.ReplaceAll(s string, old string, new string) string
strings.Split(s string, char string) string
strings.Joint(s string, char string) string
strings.Contains(s string, sub string) bool
strings.TrimSpace(s string) string // 去除字符串首位的空格
strings.ToUpper(s string) string // 转化为大写
strings.ToLower(s string) string // 转化为小写
```

strconv 包提供 API 可实现字符串与其他基础类型之间的转换

## 常用数学函数

```go
math.Abs
math.Max
math.Min
math.Sqrt // 开平方/立方根
...
```

### 大型数值

```go
// math/big 包
num := "22222222222222222222222222222"
var bigInt = new(big.Int)
bigInt.SetString(num, 10)
```

## 排序

```go
// sort 包，支持切片类型: []int、[]float64、[]string
sort.Ints
sort.Float64s
sort.Strings
sort.Slice(slice interface{}, less func(i, j int) bool) // 通过 less 参数所引用的自定义函数来实现排序

```

## 输入与输出

### 简单的内存缓冲区

使用 byte 类型的数组/切片

```go
var buffer = make([]byte, 0)
```

## 与输入/输出有关的接口类型

io 包提供了一组接口类型

- Reader: 实现从数据流中读取部分字节
- Writer: 实现将字节序列写入数据流中
- Closer: 当读写操作完成后关闭数据流，清除对象引用或清理内存
- Seeker: 可以修改当前位置。调用 Seek 方法后再调用 Read 或 Write 方法，就会从新设置的位置开始处理

## 文件与目录

与文件操作相关的 API 主要集中在两个包中：io/ioutil 和 os

```go
os.Create
os.Open
os.Rename
os.Stat // 获取文件的信息，例如 文件名、文件大小、修改时间等
```

## 加密与解密

### Base64 编码与解码

encoding/base64 提供 Base64

### DES 与 AES 算法

crypto/des 和 crypto/aes

DES（Data Encryption Standard，数据加密标准），是一种通过密钥来进行加密或解密的算法。此算法采用的是分块计算法，每个输入块为64位（即8字节为一组），计算后输出64位的密文。DES的密钥也是64位（实际使用56位）。

AES（Advanced Encryption Standard，高级加密标准），此算法用于替代DES算法。AES算法的分块大小为128位（即16字节），密钥长度可以是128位、192位或256位。

### RSA 算法

RSA 是一种公开密钥的加密体制——加密与解密使用不同的秘钥，crypto/rsa

## 协程

### 启动协程

在调用函数或方法时加上“go”关键词

### 通道

通道类型（channel，类型名称为 chan）既可用于协程之间的数据通信，也可以用于协程之间的同步

通道类型有以下几种表示方式：

- chan T：双向通道，既可以发送数据，也可以接受数据
- chan <- T：只能向通道发送数据
- <- chan T: 只能向通道接收数据

T 是通道中可存放的数据类型，例如 chan int

---

实例化通道

```go
var c = make(chan string)

var c2 = make(chan string, 0) // make 函数的第二个参数（size）标识通道对象的缓冲止，忽略此参数或设置为 0 表示所创建的通道实例不使用缓冲

c <- "hello" // 发送数据

<- c // 接收数据

close(c)

```

#### 数据缓冲

无缓冲的通道要求发送与接收操作同时进行——向通道发送数据的同时必须有另一个协程在接收。

### 互斥锁

sync 包公开的 Mutex 类型

```go
var locker = new(sync.Mutex)

locker.Lock()
locker.Unlock()
```

### WaitGroup 类型
