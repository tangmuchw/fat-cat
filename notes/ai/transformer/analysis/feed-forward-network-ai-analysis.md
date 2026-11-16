[toc]

---

这段代码是在用**纯 Python 标准库**演示 Transformer 里**前馈网络（FFN, Feed-Forward Network）**的两种实现：

> 经典 **ReLU 版**（《Attention Is All You Need》原论文结构）和现代 **SwiGLU 版**（LLaMA、PaLM 等大模型常用结构）。

你可以把它理解成：

> 注意力层负责让词与词“交换信息”，FFN 负责对每个词“自己手里的向量”做一次深度加工：先升维到更宽的空间，过一道激活函数，再降维回来。

这份文档按小白视角拆解，并深入对比两种结构的差异。

---

# 代码实现分析

## 1. 整体流程一句话

输入 `X` 形状是 `[2, 4]`，表示 2 个词、每个词 4 维。两种 FFN 都做“升维 → 激活 → 降维”，但中间步骤不同：

**ReLU 版**三步：

1. `X · W1 + b1`：把 4 维升到 8 维；
2. `ReLU(...)`：把负数截断为 0；
3. `(...) · W2 + b2`：把 8 维降回 4 维。

**SwiGLU 版**四步：

1. `X · W_gate + b_gate`：升维，得到“门控”信号；
2. `X · W_up + b_up`：升维，得到“内容”信号；
3. `Swish(gate) ⊙ up`：用门控逐元素调节内容；
4. `(...) · W_down + b_down`：降回 4 维。

两版输出形状都是 `[2, 4]`：2 个词，每个词仍是 4 维。

---

## 2. 核心概念：FFN 是什么？为什么 Transformer 需要它？

Transformer 的每个 Block 里有两个主要子层：

- **注意力层（Attention）**：让不同词之间交换信息，是“词与词”的交互；
- **前馈网络（FFN）**：对每个位置的向量单独做变换，是“词内部”的加工。

FFN 有三个关键特点：

1. **逐位置（position-wise）**：对序列里每个词用同一套权重，但彼此独立计算，不混合信息；
2. **先升后降**：中间维度 `d_ff` 通常比 `d_model` 大（经典是 4 倍），像一个“扩建车间”；
3. **引入非线性**：激活函数让网络能拟合复杂关系，否则两层线性变换等价于一层。

代码里：

```python
d_model = 4   # 输入/输出维度
d_ff = 8      # 中间隐藏层维度，这里是 2 倍（演示用，经典是 4 倍）
```

---

## 3. 逐段解释代码

### 3.1 `matrix_multiply(a, b)`

```python
def matrix_multiply(a: Matrix, b: Matrix) -> Matrix:
    m = len(a)
    n: int = len(b)
    p = len(b[0])
    result: Matrix = [[0.0 for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                result[i][j] += a[i][k] * b[k][j]
    return result
```

标准矩阵乘法：`a` 是 `m×n`，`b` 是 `n×p`，输出 `m×p`。

结果第 `i` 行第 `j` 列 = `a` 第 `i` 行与 `b` 第 `j` 列逐项相乘再相加。

---

### 3.2 `matrix_add(a, b)`

```python
rows_b = b * len(a) if len(b) == 1 and len(a) > 1 else b
return [
    [left + right for left, right in zip(row_a, row_b)]
    for row_a, row_b in zip(a, rows_b)
]
```

逐元素相加。这里有个**广播（broadcast）**细节：

- 偏置 `b` 在代码里被写成**单行矩阵**，形状 `1×n`；
- 如果直接用 `zip(a, b)`，只会配对到 `a` 的第一行，输出也只剩一行；
- 所以先判断：当 `b` 只有 1 行而 `a` 有多行时，把 `b` 重复 `len(a)` 次，让它能加到每一行上。

例子：

```python
matrix_add([[1.0, 2.0], [3.0, 4.0]], [[0.5, 0.5]])
# [[1.5, 2.5], [3.5, 4.5]]
```

这就是把偏置 `[0.5, 0.5]` 加到了两行上。

---

### 3.3 `relu(x)`

```python
return [max(0.0, value) for value in x]
```

ReLU（Rectified Linear Unit）：负数变 0，正数不变。

```python
relu([-1.0, 0.0, 2.0])
# [0.0, 0.0, 2.0]
```

优点：计算极快、梯度简单（正数区间梯度恒为 1）。  
缺点：**Dying ReLU 问题**——一旦输出为负，梯度为 0，这个神经元可能永远“死掉”不再更新。

---

### 3.4 `swish(x)`

```python
return [value / (1.0 + math.exp(-value)) for value in x]
```

Swish（也叫 SiLU）：`Swish(x) = x · sigmoid(x)`。

```python
swish([0.0])   # [0.0]
swish([1.0])   # 约 0.7311
swish([-1.0])  # 约 -0.2689
```

对比 ReLU：

- ReLU 在负数区间直接给 0；
- Swish 在负数区间给一个**很小但非零**的值，且曲线平滑可导。

这意味着负输入仍能有梯度，神经元不容易“死亡”。

---

### 3.5 `FeedForwardReLU.__init__`

```python
rng = random.Random(42)

self.w1: Matrix = random_matrix(d_model, d_ff)   # [4, 8]
self.b1: Matrix = [[0.0 for _ in range(d_ff)]]   # [1, 8]
self.w2: Matrix = random_matrix(d_ff, d_model)   # [8, 4]
self.b2: Matrix = [[0.0 for _ in range(d_model)]]# [1, 4]
```

初始化两层参数：

- `W1` 负责升维（4 → 8），`W2` 负责降维（8 → 4）；
- 偏置用 `uniform(-0.1, 0.1)` 的小随机数初始化；
- `random.Random(42)` 是局部随机生成器，固定种子保证每次运行结果一致，且不会污染全局随机状态。

---

### 3.6 `hidden(x)`

```python
linear = matrix_add(matrix_multiply(x, self.w1), self.b1)
return [relu(row) for row in linear]
```

第一层：`X · W1 + b1`，再逐行过 ReLU。

形状变化：

```text
X:       [2, 4]
W1:      [4, 8]
linear:  [2, 8]
hidden:  [2, 8]
```

把每个词的 4 维向量扩展到 8 维，高维空间里能表达更丰富的特征组合。

---

### 3.7 `forward(x)`（ReLU 版）

```python
hidden = self.hidden(x)
return matrix_add(matrix_multiply(hidden, self.w2), self.b2)
```

第二层：把 8 维隐藏表示乘 `W2` 降回 4 维，加偏置输出。

```text
hidden: [2, 8]
W2:     [8, 4]
output: [2, 4]
```

完整公式：

```text
FFN(x) = ReLU(x · W1 + b1) · W2 + b2
```

---

### 3.8 `FeedForwardSwiGLU.__init__`

```python
self.gate_up: list[Matrix] = [
    random_matrix(d_model, d_ff),   # W_gate
    random_matrix(d_model, d_ff),   # W_up
]
self.gate_up_bias: list[Matrix] = [
    [[0.0 for _ in range(d_ff)]],
    [[0.0 for _ in range(d_ff)]],
]
self.w_down: Matrix = random_matrix(d_ff, d_model)   # [8, 4]
self.b_down: Matrix = [[0.0 for _ in range(d_model)]]
```

SwiGLU 有**三组**权重（门控、上投影、下投影），比 ReLU 版多了 `W_gate` 这一组。

代码把 `W_gate` 和 `W_up` 打包进 `gate_up` 列表：

- `self.gate_up[0]` 是门控权重；
- `self.gate_up[1]` 是上投影权重。

这样既保持了逻辑清晰，也避免了属性过多。

---

### 3.9 `gate_and_up(x)`

```python
gate = matrix_add(matrix_multiply(x, self.gate_up[0]), self.gate_up_bias[0])
up   = matrix_add(matrix_multiply(x, self.gate_up[1]), self.gate_up_bias[1])
return gate, up
```

一次算出两个 `[2, 8]` 的矩阵：

- **gate（门控）**：决定“每条特征要放行多少信息”；
- **up（上投影）**：提供真正要被传递的内容。

---

### 3.10 `forward(x)`（SwiGLU 版）

```python
gate, up = self.gate_and_up(x)
gated: Matrix = [
    [swish_gate * up_value for swish_gate, up_value
     in zip(swish(gate_row), up_row)]
    for gate_row, up_row in zip(gate, up)
]
return matrix_add(matrix_multiply(gated, self.w_down), self.b_down)
```

逐元素处理：

1. 对 `gate` 的每一行过 Swish；
2. 与 `up` 对应位置**逐元素相乘**（`⊙`）；
3. 结果乘 `W_down` 降回 4 维。

完整公式：

```text
SwiGLU(x) = (Swish(x · W_gate + b_gate) ⊙ (x · W_up + b_up)) · W_down + b_down
```

这里的 `⊙` 是 Hadamard 积（逐元素相乘），不是矩阵乘法。

---

## 4. `main()` 里输入是什么？

```python
d_model = 4
d_ff = 8

x_input = [
    [1.0, 0.0, 0.0, 0.0],
    [0.0, 1.0, 0.0, 0.0],
]
```

2 个词、每个词 4 维，用 one-hot 形式方便观察。

然后对同一输入分别跑两版：

```python
relu_ffn   = FeedForwardReLU(d_model=4, d_ff=8)
swiglu_ffn = FeedForwardSwiGLU(d_model=4, d_ff=8)

relu_output   = relu_ffn.forward(x_input)
swiglu_output = swiglu_ffn.forward(x_input)
```

打印两版输出，直接对比差异。

---

## 5. 形状总表

| 变量 | ReLU 版形状 | SwiGLU 版形状 | 含义 |
|---|---|---|---|
| `X` | `[2, 4]` | `[2, 4]` | 输入：2 个词，每个 4 维 |
| `W1` / `W_gate` / `W_up` | `[4, 8]` | `[4, 8]`（`W_gate`、`W_up` 各一个） | 升维权重 |
| `b1` / `b_gate` / `b_up` | `[1, 8]` | `[1, 8]`（各一个） | 升维偏置，按行广播 |
| `linear` / `gate` / `up` | `[2, 8]` | `[2, 8]` | 升维后的中间结果 |
| `hidden` / `gated` | `[2, 8]` | `[2, 8]` | 激活/门控后的隐藏表示 |
| `W2` / `W_down` | `[8, 4]` | `[8, 4]` | 降维权重 |
| `output` | `[2, 4]` | `[2, 4]` | 输出：回到原始维度 |

---

## 6. 这段代码演示了什么？

它完整演示了两种 FFN 的前向公式：

```text
ReLU 版：  FFN(x) = ReLU(x·W1 + b1)·W2 + b2

SwiGLU 版：FFN(x) = (Swish(x·W_gate + b_gate) ⊙ (x·W_up + b_up))·W_down + b_down
```

关键区别：

- ReLU 版是“**升维 → 截断 → 降维**”；
- SwiGLU 版是“**两条升维路径 → 门控相乘 → 降维**”。

---

## 7. 小白需要注意的点

1. **这不是完整 Transformer Block**  
   没有注意力、残差连接、LayerNorm，只有 FFN 本身。真实 Block 里 FFN 前面还有注意力子层。

2. **FFN 不混合词与词的信息**  
   每个词独立经过同一套权重。词间交互由注意力层负责。

3. **权重是随机初始化的**  
   输出数值没有实际语义，只是演示计算流程。固定种子 42 保证每次结果一样。

4. **SwiGLU 参数更多**  
   因为它有三组矩阵（gate、up、down），而 ReLU 版只有两组。为控制参数量，实际模型会把 SwiGLU 的 `d_ff` 调小。

5. **演示里 `d_ff = 8` 只是示意**  
   经典 Transformer 用 `d_ff = 4 × d_model`；SwiGLU 常用 `d_ff ≈ 8/3 × d_model` 再向上取整。

---

## 总结

```text
输入 X [2, 4]
   │
   ├─ ReLU 版 ── 升维 [2,8] ── ReLU ── 降维 [2,4] ── 输出
   │
   └─ SwiGLU 版 ── 升维出 gate/up 两路 [2,8]
                    ── Swish(gate) ⊙ up ── 降维 [2,4] ── 输出
```

两版都完成了“升维加工再降维”，但 SwiGLU 用**门控机制**让网络自己决定每条信息放行多少，表达力更强，是现代大模型的默认选择。

---

# ReLU 版 vs SwiGLU 版：到底差在哪？

## 1. 公式对比

| 版本 | 公式 | 激活/门控 |
|---|---|---|
| ReLU FFN | `ReLU(xW1 + b1)W2 + b2` | 单层 ReLU 截断 |
| SwiGLU FFN | `(Swish(xW_gate) ⊙ (xW_up))W_down` | Swish 门控 × 上投影 |

---

## 2. 结构差异

ReLU 版是一条直线：

```text
x ── W1 ── ReLU ── W2 ── output
```

SwiGLU 版是两条路径汇合：

```text
        ┌── W_gate ── Swish ──┐
x ──────┤                      ├── ⊙ ── W_down ── output
        └── W_up ─────────────┘
```

`⊙` 表示逐元素相乘。门控路径像一道“闸门”，控制上投影路径里每条信息能通过多少。

---

## 3. 参数量对比

以本例 `d_model = 4, d_ff = 8` 计算（忽略偏置）：

| 版本 | 矩阵 | 参数量 |
|---|---|---|
| ReLU | `W1: 4×8` + `W2: 8×4` | `32 + 32 = 64` |
| SwiGLU | `W_gate: 4×8` + `W_up: 4×8` + `W_down: 8×4` | `32 + 32 + 32 = 96` |

SwiGLU 是 ReLU 的 **1.5 倍**（因为多了 1 组升维矩阵）。

这也是为什么实际模型用 SwiGLU 时会把 `d_ff` 缩小：三组矩阵要跟两组矩阵参数量相当，中间的 `d_ff` 要乘以 `2/3`。

---

## 4. 为什么 SwiGLU 更强？

### 4.1 门控机制：动态调节信息流

ReLU 是固定的“截断”：负数一律变 0。

SwiGLU 的门控是**输入相关的**：

```text
输出 = Swish(门控信号) × 内容信号
```

门控信号由输入自己算出来，意味着网络能根据当前词动态决定：

- 哪些特征放行；
- 哪些特征压制；
- 放行多少（连续值，不是硬开关）。

这比 ReLU 的固定截断灵活得多。

### 4.2 Swish 避免神经元死亡

ReLU 在负区间梯度为 0：

```text
ReLU(-1) = 0，导数 = 0
```

一旦某个神经元长期输出负值，它的权重就不再更新，彻底“死亡”。

Swish 在负区间有小的非零输出和梯度：

```text
Swish(-1) ≈ -0.2689，导数 ≠ 0
```

所以神经元仍有恢复的机会，训练更稳定。

### 4.3 平滑性

ReLU 在 0 点不可导（折点）；Swish 处处光滑可导。平滑的损失函数通常更利于优化。

---

## 5. 数值例子对比

同一输入经过两种激活：

| 输入值 | ReLU | Swish |
|---|---|---|
| `-2.0` | `0.0000` | `-0.2384` |
| `-1.0` | `0.0000` | `-0.2689` |
| `0.0` | `0.0000` | `0.0000` |
| `1.0` | `1.0000` | `0.7311` |
| `2.0` | `2.0000` | `1.7616` |

可以看出：

- 正数区间 Swish 比 ReLU 略小（有轻微压缩）；
- 负数区间 Swish 保留小幅负值，ReLU 全部归零；
- 这正是“软门控”的效果。

---

## 6. 为什么现代大模型偏爱 SwiGLU？

| 模型 | FFN 激活 |
|---|---|
| Transformer（原论文） | ReLU |
| BERT | GELU |
| LLaMA / PaLM / Qwen | SwiGLU |

主要原因是：在同等参数量下，SwiGLU 的门控结构通常能带来更好的表达力和训练稳定性，已经被大量实验验证。

---

## 总结表

| 对比项 | ReLU 版 | SwiGLU 版 |
|---|---|---|
| 公式 | `ReLU(xW1+b1)W2+b2` | `(Swish(xW_gate)⊙(xW_up))W_down` |
| 权重矩阵数 | 2 | 3 |
| 激活函数 | ReLU（硬截断） | Swish（软门控） |
| 负区间梯度 | 0（可能死神经元） | 非零（更稳） |
| 参数量（本例） | 64 | 96 |
| 表达力 | 基础 | 更强（门控动态调节） |
| 使用场景 | 经典 Transformer、教学 | 现代大模型 |

一句话：

> **ReLU 版是“固定截断”，SwiGLU 版是“按需放行”；后者用多一组矩阵的代价，换来更强、更稳的表达能力。**

---

# 为什么 FFN 要先升维再降维？

## 1. 从形状上看

```text
x:      [seq_len, d_model]   例如 [2, 4]
W1:     [d_model, d_ff]      例如 [4, 8]
hidden: [seq_len, d_ff]      例如 [2, 8]
W2:     [d_ff, d_model]      例如 [8, 4]
output: [seq_len, d_model]   例如 [2, 4]
```

先扩到更宽的空间，再压回来。输入和输出维度相同，方便接残差连接。

---

## 2. 升维的意义

在低维空间里，特征组合方式有限。升到高维后：

- 能组合出更多特征模式；
- 非线性激活在高维空间里能表达更复杂的关系；
- 相当于“把问题摊开到一个更大的工作台处理”。

如果直接 `d_model → d_model`，中间不升维，表达力会明显不足。

---

## 3. `d_ff` 为什么通常是 4 倍？

原论文取 `d_ff = 4 × d_model`，这是一个经验上的平衡点：

- 太小：中间层信息容量不足；
- 太大：参数量和计算量暴涨，收益递减。

例子：

| 模型 | `d_model` | `d_ff` | 倍数 |
|---|---|---|---|
| Transformer-base | 512 | 2048 | 4 |
| BERT-base | 768 | 3072 | 4 |
| 本例 | 4 | 8 | 2（演示用） |

---

## 4. SwiGLU 为什么要调整 `d_ff`？

SwiGLU 有 3 组矩阵，若仍用 `d_ff = 4 × d_model`，参数量会比 ReLU 版多 50%。

为保持参数量相当，实践中取：

```text
d_ff = (8/3) × d_model
```

再向上取整到 64 的倍数（便于 GPU 对齐）。

例如 LLaMA-7B：

```text
d_model = 4096
d_ff ≈ 8/3 × 4096 ≈ 10922.7
向上取整到 64 的倍数 → 11008
```

---

## 5. 一个比喻

把 FFN 想成一条**加工流水线**：

- 升维：把原料摊到更大的工作台上；
- 激活：工人对每件半成品做筛选/加工；
- 降维：把成品打包回标准箱子，送去下一站。

工作台太小（升维不足），施展不开；太大（升维过度），场地浪费。4 倍是经验上的“黄金尺寸”。

---

## 总结

| 问题 | 回答 |
|---|---|
| 为什么要升维？ | 高维空间表达力更强，能组合更多特征 |
| 为什么再降维？ | 保持输入输出同维，方便残差连接 |
| `d_ff` 一般多大？ | ReLU 版常取 `4×d_model` |
| SwiGLU 为什么不同？ | 三组矩阵，需把 `d_ff` 缩到约 `8/3×d_model` 以平衡参数量 |

一句话：

> **升维是“展开问题”，降维是“收拢答案”；`d_ff` 控制展开的幅度，是效果与成本之间的权衡。**

---

# 附：代码里几个容易忽略的细节

## 1. 偏置为什么写成 `[[0.0, ...]]` 而不是 `[0.0, ...]`？

因为 `matrix_add` 接收的是矩阵（`list[list[float]]`）。把偏置写成**单行矩阵** `[1, d_ff]`，可以复用广播逻辑加到序列每一行上。如果写成一维列表，形状对不上。

## 2. `Random(42)` 为什么是局部的？

如果用 `random.seed(42)` 会重置**全局**随机状态，影响程序里其他用到随机的地方。用 `rng = random.Random(42)` 只影响这个实例，互不干扰。

## 3. 两个类的随机种子都是 42，会不会生成相同权重？

不会完全相同。因为两个类的 `__init__` 各自创建了独立的 `Random(42)`，初始化顺序和调用次数不同，生成的数值序列会有差异。这也让两版输出的对比更有意义。

## 4. `gate_up` 为什么用列表打包？

如果用 `self.w_gate`、`self.w_up`、`self.w_down` 等独立属性，加上维度属性会超过 7 个，触发 Pylint 的 `too-many-instance-attributes`。用列表打包既保持了逻辑清晰，又通过了检查。

## 5. 为什么 `hidden()` / `gate_and_up()` 要做成公开方法？

除了让 `forward()` 更清晰，还为了每个类有至少 2 个公开方法，避免 Pylint 的 `too-few-public-methods` 警告。教学代码里，把中间步骤单独暴露出来也方便调试和观察。

---

一句话总结全文：

> **这段代码实现并对比了 Transformer FFN 的两种形态：ReLU 版用“升维—截断—降维”的经典结构，SwiGLU 版用“双路升维—门控相乘—降维”的现代结构；后者以更多参数为代价，换来更强、更稳定的表达能力。**
