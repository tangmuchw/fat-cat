[toc]

---

这段代码是在用**纯 Python 标准库**演示 Transformer 里的**层归一化（Layer Normalization，简称 LayerNorm）**。

你可以把它理解成：

> 神经网络在训练时，每一层的数值可能越变越大或越变越小，导致训练不稳定。LayerNorm 就像给每一行数据做一次"标准化体检"——把均值拉回 0、方差拉回 1，让数值保持在健康范围，然后再用两个可学习参数微调回来。

这份文档按小白视角拆解代码，并深入对比 LayerNorm 与 BatchNorm、解释 gamma/beta 和 eps 的作用，还会讲清 Pre-Norm / Post-Norm 两种放置方式和 RMSNorm 简化版。

---

# 代码实现分析

## 1. 整体流程一句话

输入是 2 个样本、每个样本 4 维（`d_model = 4`）。流程分两步：

1. **逐行标准化**：对每一行独立算均值和方差，把这一行变成均值 0、方差 1；
2. **缩放平移**：用可学习参数 `gamma`（缩放）和 `beta`（平移）微调标准化后的结果。

输出形状仍是 `[2, 4]`：每个样本的数值分布被规范到稳定范围。

---

## 2. 核心概念：为什么要归一化？

### 2.1 问题：数值会"漂移"

神经网络一层层计算下来，每层的输出数值可能：

- 越来越大（梯度爆炸）；
- 越来越小（梯度消失）；
- 分布不断变化（内部协变量偏移）。

这会让训练变得很不稳定，需要小心调学习率、初始化等。

### 2.2 解法：把数值拉回标准范围

归一化的思路是：把数值变成**均值 0、方差 1** 的标准分布。

```text
原始：   [100, 200, 300, 400]      均值 250，方差 12500
标准化： [-1.34, -0.45, 0.45, 1.34] 均值 0，方差 1
```

这样不管原始数值多大，归一化后都在相似的范围内，训练更稳定。

### 2.3 为什么叫"层"归一化？

因为它是**在一个样本内部、沿着特征维度**做归一化：

```text
样本 0: [1, 2, 3, 4]       ← 对这 4 个数算均值方差，归一化这一行
样本 1: [100, 200, 300, 400] ← 独立地归一化这一行
```

每个样本各算各的，互不影响。这就是"Layer（层）"的含义——在特征这一层上做归一化。

---

## 3. 逐段解释代码

### 3.1 `mean(values)`

```python
return sum(values) / len(values)
```

算术平均数：所有数加起来除以个数。

```python
mean([1.0, 2.0, 3.0])  # 2.0
```

---

### 3.2 `variance(values)`

```python
avg = mean(values)
return sum((value - avg) ** 2 for value in values) / len(values)
```

**总体方差**（除以 n，不是 n-1）：每个数与均值之差的平方，再取平均。

```python
variance([1.0, 2.0, 3.0])
# 均值 2，差的平方分别是 1, 0, 1，平均 = 2/3 ≈ 0.6667
```

为什么除以 n 而不是 n-1？

- 统计学里样本方差除以 n-1（无偏估计）；
- 深度学习里归一化只是要一个尺度，除以 n 更简单，且 PyTorch 的 LayerNorm 也是这么做的。

---

### 3.3 `normalize_row(values, eps)` —— 标准化核心

```python
avg = mean(values)
standard_deviation = math.sqrt(variance(values) + eps)
return [(value - avg) / standard_deviation for value in values]
```

这就是标准化公式：

```text
normalized = (value - 均值) / 标准差
```

其中标准差 = `√(方差 + eps)`。

`eps`（默认 1e-5）是一个极小的常数，加在方差里防止除零。如果一行所有数都相同（方差为 0），没有 eps 就会除以 0 报错。

例子：

```python
normalize_row([1.0, 2.0, 3.0], 1e-5)
# 均值 2，标准差 ≈ 0.8165
# 结果 ≈ [-1.2247, 0.0, 1.2247]
```

标准化后：

- 均值变成 0（因为每个数都减去了均值）；
- 方差变成约 1（因为除以了标准差）。

---

### 3.4 `LayerNormalization.__init__`

```python
self.d_model: int = d_model
self.eps: float = eps
self.gamma: list[float] = [1.0 for _ in range(d_model)]
self.beta: list[float] = [0.0 for _ in range(d_model)]
```

初始化两个**可学习参数**：

- `gamma`：每个维度的缩放系数，初始为 1（不改变尺度）；
- `beta`：每个维度的平移量，初始为 0（不改变位置）。

它们是**向量**，长度等于特征维度 `d_model`。也就是说，每个特征维度都有自己独立的缩放和平移。

为什么初始设成 1 和 0？因为这样一开始 `gamma × 标准化值 + beta` 就等于标准化值本身，不引入额外扰动，训练从"纯标准化"开始。

---

### 3.5 `normalize(x)` —— 逐行标准化

```python
return [normalize_row(row, self.eps) for row in x]
```

对每一行调用 `normalize_row`，得到标准化矩阵。

```text
输入 x:        [2, 4]
normalize(x):  [2, 4]   每行均值约 0、方差约 1
```

这一步还没有用到 gamma/beta。把它单独暴露出来，方便观察纯标准化的效果。

---

### 3.6 `forward(x)` —— 完整流程

```python
normalized = self.normalize(x)
return [
    [
        scale * value + shift
        for scale, shift, value in zip(self.gamma, self.beta, row)
    ]
    for row in normalized
]
```

先标准化，再对每个数做：

```text
output = gamma[i] × normalized_value + beta[i]
```

`zip(self.gamma, self.beta, row)` 把同一维度的 gamma、beta 和数值配成一组，逐元素处理。

完整公式：

```text
LayerNorm(x) = gamma ⊙ (x - μ) / √(σ² + eps) + beta
```

其中 `μ` 是均值，`σ²` 是方差，`⊙` 是逐元素相乘。

---

## 4. `main()` 里输入是什么？

```python
d_model = 4

x_input = [
    [1.0, 2.0, 3.0, 4.0],
    [100.0, 200.0, 300.0, 400.0],
]
```

特意构造了**两行数值尺度差异极大**的输入：

- 样本 0：均值 2.5，方差 1.25
- 样本 1：均值 250，方差 12500

这样能清楚地看到：无论原始数值多大，LayerNorm 都把它们标准化到同一分布。

实际运行输出：

```text
原始输入的每行统计量:
  样本 0: 均值=2.5000, 方差=1.2500
  样本 1: 均值=250.0000, 方差=12500.0000

标准化后（均值≈0，方差≈1）:
  样本 0: 均值=0.0000, 方差=1.0000
    数值: ['-1.3416', '-0.4472', '0.4472', '1.3416']
  样本 1: 均值=0.0000, 方差=1.0000
    数值: ['-1.3416', '-0.4472', '0.4472', '1.3416']
```

两行起点天差地别，标准化后**完全相同**——因为它们内部模式一样（都是等差递增）。

设置 `gamma=2, beta=0.5` 后：

```text
  样本 0: ['-2.1833', '-0.3944', '1.3944', '3.1833']
```

每个值都变成 `原值 × 2 + 0.5`，方差扩大到约 4，均值平移到 0.5。

---

## 5. 形状总表

| 变量 | 形状 | 含义 |
|---|---|---|
| `d_model` | 标量（4） | 特征维度 |
| `x` | `[2, 4]` | 输入，2 个样本各 4 维 |
| `gamma` / `beta` | `[4]` | 每维的缩放/平移参数 |
| `normalized` | `[2, 4]` | 标准化后的矩阵 |
| `output` | `[2, 4]` | 缩放平移后的最终输出 |

---

## 6. 这段代码演示了什么？

它完整演示了 LayerNorm 的公式：

```text
μ = mean(x)                          对每个样本（每行）独立计算
σ² = variance(x)
output = gamma ⊙ (x - μ) / √(σ² + eps) + beta
```

关键特性：

- **逐样本独立**：每行各算各的均值方差，不受其他样本影响；
- **形状不变**：输入输出都是 `[batch, d_model]`；
- **可学习微调**：gamma/beta 让网络能恢复被归一化"抹掉"的表达力。

除了基础 LayerNorm，代码还演示了三项延伸：

1. **Pre-Norm vs Post-Norm**：`post_norm_block` 与 `pre_norm_block` 对比两种归一化放置方式；
2. **RMSNorm**：`RMSNormalization` 只算均方根、不减均值，只做缩放；
3. **归一化在 Block 中的位置**：通过两种 block 函数直观呈现。

---

## 7. 小白需要注意的点

1. **归一化的是"每个样本自己"，不是整个 batch**  
   这是 LayerNorm 与 BatchNorm 的核心区别（下文详述）。

2. **均值方差是按行算的**  
   代码里 `normalize_row(row, eps)` 对每一行独立处理，不会跨行统计。

3. **gamma/beta 是可学习参数**  
   它们在训练中会被梯度更新。代码里为了演示手动改了值，真实场景是优化器自动学习。

4. **eps 防止除零**  
   如果一行所有数相同，方差为 0，没有 eps 就会出错。

5. **标准化后均值方差是"约等于" 0 和 1**  
   因为加了 eps，方差会略小于 1，但可以忽略。

6. **LayerNorm 在 Transformer 里通常配合残差连接使用**  
   代码通过 `post_norm_block` / `pre_norm_block` 展示了两种放置方式，Pre-Norm 更稳定、是大模型主流。

---

## 总结

```text
输入 x [2, 4]
  ↓ 每行独立算均值和方差
标准化：均值→0，方差→1
  ↓ 逐个维度乘 gamma、加 beta
输出 [2, 4]
```

LayerNorm 把每个样本的特征分布规范到稳定范围，再用可学习参数恢复表达力，是 Transformer 稳定训练的关键组件。放到 Block 里有 Pre-Norm / Post-Norm 两种选择（主流是 Pre-Norm），简化版 RMSNorm 则只算均方根、不减均值。

---

# LayerNorm vs BatchNorm

## 1. 核心区别：在哪个维度上统计

这是最本质的差异：

| 对比项 | BatchNorm | LayerNorm |
|---|---|---|
| 统计维度 | 跨样本，对同一特征 | 单样本内，跨所有特征 |
| 依赖 batch | 是 | 否 |
| 归一化对象 | 每一列（特征） | 每一行（样本） |
| 推理时 | 用训练时的移动平均 | 直接用当前样本计算 |
| 典型场景 | CNN | Transformer / RNN |

用矩阵 `[batch, features]` 来看：

```text
BatchNorm：沿 batch 方向（竖着）算每一列的均值方差
LayerNorm：沿 features 方向（横着）算每一行的均值方差
```

## 2. 图示对比

假设输入是 2 个样本、4 个特征：

```text
        特征0  特征1  特征2  特征3
样本0  [  1,    2,    3,    4  ]  ← LayerNorm 对这一行归一化
样本1  [100,  200,  300,  400  ]  ← LayerNorm 对这一行归一化
          ↓      ↓      ↓      ↓
       BatchNorm 对每一列归一化（跨样本 0 和 1）
```

本代码的运行结果完美展示了差异：

```text
标准化后两行都是 [-1.34, -0.45, 0.45, 1.34]
```

- **LayerNorm 视角**：两行各自标准化，因为内部模式一样，结果一样；
- **BatchNorm 视角**：会对特征 0 的 [1, 100] 一起算均值方差，两行结果完全不同。

## 3. 为什么 Transformer 用 LayerNorm，不用 BatchNorm？

### 3.1 NLP 的 batch 不可靠

文本序列长度不一，batch 里的样本差异很大：

```text
样本 0：短句，3 个词
样本 1：长句，200 个词
```

BatchNorm 在 batch 上统计，会被长短不一的序列干扰，均值和方差不稳定。

### 3.2 推理时的问题

BatchNorm 训练时用 batch 统计量，推理时要用训练期间累计的移动平均。

对于 NLP 这种输入分布多变的任务，移动平均往往不准，导致训练和推理表现不一致。

LayerNorm 不需要存移动平均，推理时直接用当前样本算，行为一致。

### 3.3 逐样本独立更适合序列

Transformer 对每个 token 独立处理，LayerNorm 的"逐样本归一化"天然契合这种设计。

## 4. CNN 为什么常用 BatchNorm？

图像任务里：

- 输入尺寸固定，batch 统计量稳定；
- 不同图片的同一通道（比如"边缘检测器"）统计特性相似，跨样本归一化有意义；
- BatchNorm 有轻微的正则化效果（因为引入了 batch 内的噪声）。

所以 CNN 里 BatchNorm 效果很好，而 Transformer 里 LayerNorm 更合适。

## 5. 对比表

| 场景 | 推荐 | 原因 |
|---|---|---|
| CNN 图像分类 | BatchNorm | 输入固定，batch 统计可靠 |
| Transformer / NLP | LayerNorm | 序列长度可变，不依赖 batch |
| RNN | LayerNorm | 时间步独立，batch 统计不适用 |
| 小 batch 训练 | LayerNorm / GroupNorm | BatchNorm 在小 batch 下失效 |
| 生成模型 | LayerNorm / InstanceNorm | 推理需确定性行为 |

一句话：

> **BatchNorm 相信"同一特征在不同样本间统计稳定"，LayerNorm 相信"一个样本内部的特征可以互相标准化"。Transformer 属于后者。**

---

# gamma 和 beta 有什么用？

## 1. 归一化"抹掉"了什么？

标准化把所有样本都变成均值 0、方差 1。这带来一个问题：

```text
原始两行：[1, 2, 3, 4] 和 [100, 200, 300, 400]
标准化后：完全相同的 [-1.34, -0.45, 0.45, 1.34]
```

两行的**尺度差异被抹掉了**。如果原始尺度本身携带信息（比如词频、信号强度），强行抹掉会损失表达力。

## 2. gamma/beta 的作用：恢复自由度

LayerNorm 引入两个可学习参数：

```text
output = gamma × normalized + beta
```

- `gamma`（缩放）：让网络决定每个维度要放大还是缩小；
- `beta`（平移）：让网络决定每个维度的中心位置。

网络可以通过学习：

- 把 `gamma` 学成某个值，恢复一部分原始尺度信息；
- 把 `beta` 学成某个值，调整分布中心。

极端情况下，如果 `gamma = 标准差`、`beta = 均值`，LayerNorm 就退化成恒等变换（什么都不做）。所以 LayerNorm **至少不会比不做归一化更差**。

## 3. 为什么每个维度一套参数？

代码里 `gamma` 和 `beta` 都是长度为 `d_model` 的向量：

```python
self.gamma = [1.0 for _ in range(d_model)]
self.beta = [0.0 for _ in range(d_model)]
```

因为不同特征维度可能需要不同的调整：

- 有些维度对尺度敏感，需要放大；
- 有些维度需要平移到正值区间；
- 各维度独立学习，互不干扰。

如果只用单个标量，所有维度被迫一起缩放，灵活性不足。

## 4. 代码里的直观演示

```python
layer_norm.gamma = [2.0] * d_model
layer_norm.beta = [0.5] * d_model
scaled = layer_norm.forward(x_input)
```

输出从：

```text
[-1.3416, -0.4472, 0.4472, 1.3416]
```

变成：

```text
[-2.1833, -0.3944, 1.3944, 3.1833]
```

每个值都是 `原值 × 2 + 0.5`，方差扩大、均值上移。

这就是 gamma/beta 的效果：在标准化的基础上，让网络自由调整输出分布。

## 5. 参数量

gamma 和 beta 各 `d_model` 个参数，总计 `2 × d_model`。

以 `d_model = 768`（BERT-base）为例，LayerNorm 只有 1536 个参数，相对于整个模型可以忽略不计，但作用关键。

---

## 总结表

| 参数 | 初值 | 作用 | 学成极端值会怎样 |
|---|---|---|---|
| `gamma` | 1.0 | 逐维缩放 | 学成标准差 → 恢复原始尺度 |
| `beta` | 0.0 | 逐维平移 | 学成均值 → 恢复原始中心 |

一句话：

> **标准化负责"稳"，gamma/beta 负责"活"——先拉回标准分布，再让网络自己决定要什么分布。**

---

# eps 为什么必不可少？

## 1. 防止除零

标准化公式里要除以标准差：

```text
output = (x - mean) / sqrt(variance + eps)
```

如果一行所有数完全相同：

```text
[5.0, 5.0, 5.0, 5.0]
均值 = 5，方差 = 0，标准差 = 0
```

没有 eps 就会除以 0，程序崩溃（或产生 NaN/Inf）。

加上 eps 后：

```text
标准差 = sqrt(0 + 1e-5) ≈ 0.00316
输出 = (5 - 5) / 0.00316 = 0
```

结果是全 0，安全且合理——常数向量标准化后确实应该是 0。

## 2. eps 的取值

代码用默认的 `1e-5`：

```python
def __init__(self, d_model: int, eps: float = 1e-5) -> None:
```

常见取值：

| 框架/模型 | eps 默认值 |
|---|---|
| 本例 / PyTorch LayerNorm | 1e-5 |
| TensorFlow | 1e-3 |
| 一些大模型 | 1e-6 |

eps 太大会让标准化"打折"（方差明显小于 1），太小则数值不稳定。1e-5 是广泛验证的折中。

## 3. eps 加在哪里？

代码里加在**方差**上，再加平方根：

```python
standard_deviation = math.sqrt(variance(values) + eps)
```

这是标准写法。也有人加在标准差上（`sqrt(var) + eps`），但前者更常见。

## 4. 对结果的影响有多大？

对于正常数据（方差远大于 1e-5），eps 几乎没影响：

```text
方差 = 1.25，加 1e-5 后 = 1.25001
标准差从 1.11803 变成 1.11804，差异可忽略
```

只有当方差接近 0 时，eps 才真正起作用。

---

一句话：

> **eps 是"安全阀"：平时几乎不影响结果，但在方差为 0 的极端情况下防止除零崩溃。**

---

# Pre-Norm vs Post-Norm

层归一化有两种放法：

- **Post-Norm**：子层 → 残差 → 归一化（原始 Transformer）
- **Pre-Norm**：归一化 → 子层 → 残差（现在主流）

Pre-Norm 训练更稳定，现在的大模型几乎都用它。

## 1. 两种放置方式

**Post-Norm（原始 Transformer）**：先过子层，再残差相加，最后归一化。

```text
output = LayerNorm(x + Sublayer(x))
```

流程：子层 → 残差 → 归一化。

**Pre-Norm（现在主流）**：先归一化，再送入子层，最后残差相加。

```text
output = x + Sublayer(LayerNorm(x))
```

流程：归一化 → 子层 → 残差。

## 2. 为什么 Pre-Norm 更稳定？

| 对比项 | Post-Norm | Pre-Norm |
|---|---|---|
| 流程 | 子层 → 残差 → 归一化 | 归一化 → 子层 → 残差 |
| 训练稳定性 | 需要 warmup，较脆弱 | 更稳定 |
| 深层模型 | 深层梯度可能失衡 | 深层表现更好 |
| 代表模型 | 原始 Transformer | GPT-2、LLaMA 等大模型 |

Pre-Norm 的主要优势：**残差路径上没有归一化**，梯度可以直接从深层传到浅层，训练更稳定。

## 3. 本代码的实现

`layer_normalization.py` 里提供了两个直观的对比函数，共用同一个子层和归一化模块：

```python
def post_norm_block(x, sublayer, norm):
    """Post-Norm：子层 → 残差 → 归一化"""
    return norm.forward(matrix_add(x, sublayer(x)))

def pre_norm_block(x, sublayer, norm):
    """Pre-Norm：归一化 → 子层 → 残差"""
    return matrix_add(x, sublayer(norm.forward(x)))
```

运行结果（同一个子层、同一输入）：

```text
Post-Norm: 子层 → 残差 → 归一化:
  样本 0: ['-1.3416', '-0.4472', '0.4472', '1.3416']
  样本 1: ['-1.3416', '-0.4472', '0.4472', '1.3416']

Pre-Norm: 归一化 → 子层 → 残差:
  样本 0: ['-0.9125', '1.4292', '3.7708', '6.1125']
  样本 1: ['98.0875', '199.4292', '300.7708', '402.1125']
```

Post-Norm 在最后归一化，输出被压回标准分布；Pre-Norm 在残差之后不再归一化，所以输出保留了输入尺度。

---

一句话：

> **Pre-Norm 把归一化放在子层之前，让残差路径保持"畅通"，训练更稳定，是大模型的默认选择。**

---

# RMS Norm

RMS Norm 是层归一化的简化版，**只算均方根，不减均值**：

```text
RMS(x)      = sqrt(mean(x²))
RMSNorm(x)  = γ ⊗ (x / RMS(x))
```

其中 `⊗` 表示逐元素相乘，`γ` 是每维的缩放系数。

## 1. 与 LayerNorm 的区别

```text
LayerNorm: gamma × (x - μ) / √(σ² + eps) + beta
RMSNorm:   gamma × x / √(mean(x²) + eps)
```

RMSNorm 去掉了两件事：

- **不减均值**：不做 `x - μ` 的中心化；
- **不做平移**：没有 `beta` 项，只有缩放 `γ`。

它只做缩放（RMS = Root Mean Square，均方根）。

## 2. 为什么 RMSNorm 流行？

- **更快**：少算均值、少一次减法；
- **效果相当**：大量实验表明性能与 LayerNorm 接近；
- **现代大模型采用**：LLaMA、Qwen、Gemma 等都用它。

## 3. 本代码的实现

```python
def rms_norm_row(values, gamma, eps):
    rms = math.sqrt(sum(value ** 2 for value in values) / len(values) + eps)
    return [scale * value / rms for scale, value in zip(gamma, values)]

class RMSNormalization:
    def forward(self, x):
        return [rms_norm_row(row, self.gamma, self.eps) for row in x]
```

运行结果（输入与 LayerNorm 示例相同）：

```text
样本 0: ['0.3651', '0.7303', '1.0954', '1.4606']
样本 1: ['0.3651', '0.7303', '1.0954', '1.4606']
```

因为不减均值，输出不再是零均值，而是保留了原始数值的相对大小，只做了整体缩放。

---

## 附：容易忽略的细节

### 1. 这是一维行向量还是二维矩阵？

`normalize_row` 接收一维列表（一行），`LayerNormalization.normalize` 接收二维矩阵并逐行处理。真实框架里 LayerNorm 可以处理任意形状，只对最后一个维度归一化，本例简化为二维。

### 2. 方差用总体（除以 n）还是样本（除以 n-1）？

代码用总体方差（除以 n），与 PyTorch 的 LayerNorm 一致。归一化只需要一个尺度，除以 n 更直接。

### 3. gamma/beta 会梯度更新吗？

会。它们是可训练参数，本例为了演示直接手动赋值，真实场景由优化器根据梯度自动更新。

### 4. LayerNorm 在每个 Block 里都有吗？

是的。标准 Transformer Block 通常有 2 个 LayerNorm（注意力子层后一个，FFN 子层后一个），本例只实现了单个 LayerNorm 模块。

### 5. 这个模块如何接入完整 Transformer？

```text
词向量 + 位置编码              ← positional_encoding.py
  ↓
多头注意力                     ← multi_head_attention.py
  ↓
LayerNorm                      ← 本例（Pre-LN 时在此处）
  ↓ 残差连接
FFN                            ← feed_forward_network.py
  ↓
LayerNorm                      ← 本例
  ↓ 残差连接
输出
```

LayerNorm 与残差连接配合，是 Transformer 能训练深层网络的关键。

---

一句话总结全文：

> **LayerNorm 对每个样本独立地做"均值归零、方差归一"，再用可学习的 gamma/beta 恢复表达力；放到 Block 里主流用 Pre-Norm（归一化 → 子层 → 残差，训练更稳定），简化版 RMSNorm 只算均方根、不减均值，被大模型广泛采用。**
