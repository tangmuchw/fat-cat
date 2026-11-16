[toc]

---

这段代码是在用**纯 Python 标准库**演示 Transformer 里的 **Multi-Head Attention（多头注意力）前向传播**。它 building 在 `simple_self_attention.py` 的单头缩放点积注意力之上。

你可以把它理解成：

> 单头注意力只有"一双眼睛"看序列；多头注意力派出多双眼睛，每双眼睛关注不同的关系（比如一个头看语法结构，一个头看指代关系），最后把所有眼睛看到的信息汇总起来。

这份文档按小白视角拆解，并深入对比单头与多头的差异。

---

# 代码实现分析

## 1. 整体流程一句话

输入 `X` 形状是 `[4, 8]`，表示 4 个词、每个词 8 维。设置 2 个头（`num_heads = 2`），所以每个头的维度是 `d_k = 8 / 2 = 4`。

完整流程分四步：

1. **独立投影**：每个头用自己的 `Wq/Wk/Wv` 把 `X` 投影成该头的 Q、K、V；
2. **逐头算注意力**：每个头内部做缩放点积注意力，得到该头的输出；
3. **拼接**：把 2 个头的输出按列拼起来，回到 8 维；
4. **输出投影**：再乘一个 `W_o` 矩阵融合各头信息，得到最终输出。

最终输出形状是 `[4, 8]`：4 个词，每个词仍是 8 维。

---

## 2. 核心概念：什么是"多头"？

### 2.1 单头的局限

单头自注意力里，所有词共享一套 `Wq/Wk/Wv`。这意味着：

- 只有一种"匹配标准"来判断词与词的相关性；
- 一个 6 维（或 8 维）的 Q/K 向量要同时编码各种关系。

但语言里的关系是多种并存的。比如这句话：

```text
小明 把 书 给了 小红，因为她 明天 要 考试
```

里面至少有三种关系：

- "她" 指代 "小红"（指代关系）
- "小明" 是 "给" 的主语（语法关系）
- "考试" 是 "书" 的用途（语义关系）

让一套 Q/K 同时擅长捕捉所有这些关系，是很困难的。

### 2.2 多头的做法

多头注意力的思路是：

> 把原本 8 维的表示空间**切成 2 份**（每份 4 维），每个头在自己的 4 维子空间里学一套独立的 Q/K/V 投影，各看各的。

这样：

- 头 0 可能学会关注指代关系；
- 头 1 可能学会关注语法结构；
- 各头互不干扰，并行计算。

最后把各头的结论拼起来，再融合一次，得到综合视角。

---

## 3. 逐段解释代码

### 3.1 `softmax(x)`

```python
def softmax(x: list[float]) -> list[float]:
    max_val = max(x)
    exp_x = [math.exp(v - max_val) for v in x]
    sum_exp = sum(exp_x)
    return [v / sum_exp for v in exp_x]
```

把一组分数变成概率分布：每个值在 0 到 1 之间，总和为 1。

减去最大值 `max_val` 是为了防止 `math.exp` 数值溢出，是标准写法，不改变结果。

在多头注意力里，每个头都用自己的分数做一次 Softmax，所以有 `num_heads` 套独立权重。

---

### 3.2 `matrix_multiply(a, b)`

```python
m = len(a)
n: int = len(b)
p = len(b[0])
result: Matrix = [[0.0 for _ in range(p)] for _ in range(m)]
for i in range(m):
    for j in range(p):
        for k in range(n):
            result[i][j] += a[i][k] * b[k][j]
```

标准矩阵乘法：`a[m,n] · b[n,p] = result[m,p]`。

三重循环就是结果第 `i` 行第 `j` 列 = `a` 第 `i` 行与 `b` 第 `j` 列逐项相乘再相加。

---

### 3.3 `transpose(matrix)`

```python
return [list(row) for row in zip(*matrix)]
```

矩阵转置：行变列，列变行。

算注意力分数时需要 `Q · Kᵀ`，因为只有这样才能得到 `[词数, 词数]` 的分数矩阵。转置的作用是把 K 的"行"变成"列"，让矩阵乘法能做"行 · 行"的点积。

---

### 3.4 `concat_columns(matrices)` —— 多头新增的工具函数

```python
return [
    [value for matrix in matrices for value in matrix[row]]
    for row in range(len(matrices[0]))
]
```

按列拼接多个矩阵。这是多头注意力特有的操作：把各头的输出横向拼起来。

例子（两个头输出等宽，都是 `[2, 2]`，拼成 `[2, 4]`）：

```python
concat_columns([
    [[1.0, 2.0], [3.0, 4.0]],   # 头 0 的输出：2 个词，每个 2 维
    [[5.0, 6.0], [7.0, 8.0]],   # 头 1 的输出：2 个词，每个 2 维
])
# [[1.0, 2.0, 5.0, 6.0], [3.0, 4.0, 7.0, 8.0]]   形状 [2, 4]
```

关键点：**同一个词在两个头的输出被拼成同一行**（词 0 是两个头各取第 0 行拼起来），所以拼接后维度是 `d_k × num_heads`，回到 `d_model`。

关键理解：**同一个词在各头的输出被拼成一行**。

- 头 0 贡献 4 维；
- 头 1 贡献 4 维；
- 拼完就是 8 维，回到原始 `d_model`。

---

### 3.5 `MultiHeadAttention.__init__`

```python
if d_model % num_heads != 0:
    raise ValueError("d_model 必须能被 num_heads 整除")

rng = random.Random(42)
self.d_model: int = d_model
self.num_heads: int = num_heads
self.d_k: int = d_model // num_heads
```

**整除校验**是第一步：`d_model = 8, num_heads = 2`，能整除，所以 `d_k = 4`。

如果不整除（比如 `d_model = 10, num_heads = 3`），就无法均匀切分，直接报错。

然后初始化权重：

```python
self.w_queries: list[Matrix] = [
    random_matrix(d_model, self.d_k) for _ in range(num_heads)
]
self.w_keys: list[Matrix] = [ ... ]
self.w_values: list[Matrix] = [ ... ]
self.w_output: Matrix = random_matrix(d_model, d_model)
```

注意 `w_queries` 是一个**列表**，里面有 `num_heads` 个矩阵：

```text
w_queries[0]  头 0 的查询权重，形状 [8, 4]
w_queries[1]  头 1 的查询权重，形状 [8, 4]
```

`w_keys`、`w_values` 同理。每个矩阵都是 `[d_model, d_k]`。

最后 `w_output` 是 `[d_model, d_model]` = `[8, 8]`，用于拼接后的融合。

---

### 3.6 `project(x)`

```python
queries = [matrix_multiply(x, weight) for weight in self.w_queries]
keys = [matrix_multiply(x, weight) for weight in self.w_keys]
values = [matrix_multiply(x, weight) for weight in self.w_values]
return queries, keys, values
```

对每个头分别做投影。用列表推导一次性算出所有头的 Q、K、V。

形状变化：

```text
X:         [4, 8]
每个 Wq:    [8, 4]
每个 Q:     [4, 4]
```

因为有 2 个头，所以得到：

```text
queries = [Q_head0, Q_head1]   每个 [4, 4]
keys    = [K_head0, K_head1]   每个 [4, 4]
values  = [V_head0, V_head1]   每个 [4, 4]
```

---

### 3.7 `forward(x)` —— 核心流程

```python
queries, keys, values = self.project(x)
scale_factor = math.sqrt(self.d_k)

attention_weights: list[Matrix] = []
head_outputs: list[Matrix] = []
for head_index in range(self.num_heads):
    scores = matrix_multiply(
        queries[head_index], transpose(keys[head_index])
    )
    scores_scaled = [
        [value / scale_factor for value in row] for row in scores
    ]
    weights: Matrix = [softmax(row) for row in scores_scaled]
    attention_weights.append(weights)
    head_outputs.append(matrix_multiply(weights, values[head_index]))

concatenated = concat_columns(head_outputs)
output = matrix_multiply(concatenated, self.w_output)
return output, attention_weights
```

这是一个循环，每个头内部就是完整的单头注意力公式：

```text
head_i = Softmax(Q_i · K_iᵀ / √d_k) · V_i
```

#### 步骤 1：每个头算分数

```python
scores = matrix_multiply(queries[head_index], transpose(keys[head_index]))
```

```text
Q_i:     [4, 4]
K_iᵀ:    [4, 4]
scores:  [4, 4]   4 个词 × 4 个词
```

第 `i` 行第 `j` 列 = 头 `head_index` 看来，第 i 个词对第 j 个词的关注分数。

#### 步骤 2：缩放

```python
scale_factor = math.sqrt(self.d_k)   # √4 = 2
scores_scaled = [[val / 2 for val in row] for row in scores]
```

除以 `√d_k` 防止点积数值过大导致 Softmax 饱和。

注意：这里 `d_k = 4`，比单头示例的 `d_k = 6` 小，所以缩放因子从 `√6 ≈ 2.45` 变成 `√4 = 2`。

#### 步骤 3：Softmax

```python
weights = [softmax(row) for row in scores_scaled]
```

对每一行做 Softmax，得到该头的注意力权重 `[4, 4]`，每行和为 1。

#### 步骤 4：加权求和（得到该头输出）

```python
head_outputs.append(matrix_multiply(weights, values[head_index]))
```

```text
weights: [4, 4]
V_i:     [4, 4]
head_i:  [4, 4]
```

每个头输出 4 维向量，而不是原来的 8 维。这正是"切分"的含义。

#### 步骤 5：拼接所有头

```python
concatenated = concat_columns(head_outputs)
```

```text
head_0:        [4, 4]
head_1:        [4, 4]
拼接后:        [4, 8]   回到 d_model
```

#### 步骤 6：输出投影

```python
output = matrix_multiply(concatenated, self.w_output)
```

```text
concatenated: [4, 8]
w_output:     [8, 8]
output:       [4, 8]
```

`w_output` 让模型学习"如何把各头的信息混合起来"，而不是简单拼接。

---

## 4. `main()` 里输入是什么？

```python
d_model = 8
num_heads = 2

x_input = [
    [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
]
```

4 个词，每个词 8 维。前 4 维是 one-hot，方便演示。

然后：

```python
attention = MultiHeadAttention(d_model=8, num_heads=2)
output, attention_weights = attention.forward(x_input)
```

打印每个头的注意力权重，以及融合后的最终输出。

实际运行的部分输出：

```text
头 0 的注意力权重:
  词 0: ['0.2512', '0.2501', '0.2490', '0.2497']
头 1 的注意力权重:
  词 0: ['0.2469', '0.2484', '0.2486', '0.2561']
```

两头的权重分布明显不同，说明它们确实从输入中学到了不同的关注模式。

---

## 5. 形状总表

| 变量 | 形状 | 含义 |
|---|---|---|
| `X` | `[4, 8]` | 输入：4 个词，每个 8 维 |
| `Wq/Wk/Wv`（每个头） | `[8, 4]` | 每头独立的投影权重，共 3×2 = 6 个 |
| `Q_i/K_i/V_i`（每个头） | `[4, 4]` | 该头投影后的 Q、K、V |
| `scores_i` | `[4, 4]` | 该头的原始注意力分数 |
| `scores_scaled_i` | `[4, 4]` | 除以 √4 = 2 后的分数 |
| `weights_i` | `[4, 4]` | Softmax 后权重，每行和为 1 |
| `head_i` | `[4, 4]` | 该头输出，每词 4 维 |
| `concatenated` | `[4, 8]` | 2 个头拼接，回到 d_model |
| `W_o` | `[8, 8]` | 输出投影权重 |
| `output` | `[4, 8]` | 最终输出 |

---

## 6. 这段代码演示了什么？

它完整演示了多头注意力的公式：

```text
MultiHead(Q, K, V) = Concat(head_1, ..., head_h) · W_o

其中：
head_i = Attention(Q_i, K_i, V_i)
       = Softmax(Q_i · K_iᵀ / √d_k) · V_i

Q_i = X · W_q^i,  K_i = X · W_k^i,  V_i = X · W_v^i
```

对应的代码结构：

```text
输入 X
  ↓ 每个头各自投影
Q_i、K_i、V_i
  ↓ 每个头各自算注意力
head_i
  ↓ 按列拼接
Concat(head_1, ..., head_h)
  ↓ 输出投影
最终输出
```

---

## 7. 小白需要注意的点

1. **这不是完整 Transformer**  
   没有位置编码、残差连接、LayerNorm、FFN，只有多头注意力本身。

2. **输入 4 个词没有顺序信息**  
   注意力本身不知道词序，实际 Transformer 会加位置编码（见 `positional_encoding.py`）。

3. **权重是随机初始化的**  
   输出没有实际语义，只是演示计算流程。固定种子 42 保证结果可复现。

4. **`d_model` 必须能被 `num_heads` 整除**  
   否则无法均匀切分，代码会抛 `ValueError`。

5. **每头输出维度是 `d_k`，不是 `d_model`**  
   这是多头和单头最直观的区别。多头只是把 8 维拆成 2 个 4 维。

6. **注意力权重有 `num_heads` 套**  
   返回值是列表 `attention_weights`，每个元素是一个 `[4, 4]` 矩阵，对应一个头。

7. **权重接近 0.25 是因为随机初始化**  
   4 个词均匀分布就是 0.25。这里权重接近均匀，是因为初始化值很小、序列短、输入是 one-hot。真实训练后，各头会学到明显不同的、尖锐的分布。

---

## 总结

```text
输入 X [4, 8]
  ↓ 每个头用独立 Wq/Wk/Wv 投影
2 组 Q、K、V，每组 [4, 4]
  ↓ 各自算缩放点积注意力
2 个 head 输出，每个 [4, 4]
  ↓ 按列拼接
Concat [4, 8]
  ↓ W_o 输出投影
最终输出 [4, 8]
```

多头注意力把"一双眼睛"变成"多双眼睛"，每个头在更小的子空间里学不同的关系，最后汇总。它保持了输入输出维度不变，方便接入残差连接。

---

# 为什么要做多头？

## 1. 单头的问题：一种标准看所有关系

单头注意力的 Q/K 是一个高维向量，比如 8 维。它要同时负责：

- 判断"她"指代谁；
- 判断主谓关系；
- 判断语义关联。

这些关系的"匹配标准"可能相互冲突。一个向量要同时编码所有标准，能力受限。

## 2. 多头的解法：分而治之

多头注意力把 8 维切成 2 个 4 维子空间：

```text
原本：一个 8 维 Q，学所有关系
多头：两个 4 维 Q，各学各的关系
```

每个头的参数更少，但更专注。这像是一个专家团队：

- 单头 = 一个通才，什么都懂一点；
- 多头 = 多个专家，各有所长，最后开会汇总。

## 3. 各头真的学到了不同的东西吗？

在这段代码里可以看到端倪：

```text
头 0 词 0: [0.2512, 0.2501, 0.2490, 0.2497]
头 1 词 0: [0.2469, 0.2484, 0.2486, 0.2561]
```

虽然都接近均匀（因为随机初始化、未训练），但分布形态已经不同。

在真实训练的模型里，研究者发现不同头确实会特化：

- 有的头关注相邻词；
- 有的头关注句法上的主谓宾；
- 有的头关注指代关系；
- 有的头关注特殊标记（如 `[CLS]`）。

## 4. 为什么不直接增加单头维度？

一个自然的问题：与其切 2 个 4 维头，不如用 1 个 8 维头，表达力不是更强吗？

理论上单头能表达的东西，多头也能表达（多头是单头的特例，只要权重合适）。但实践中：

- **优化更容易**：多个低维子空间比一个高维空间更容易学出清晰的分工；
- **计算效率相近**：同样的参数量和计算量，多头通常效果更好；
- **结构先验**："从不同角度看问题"这个先验对自然语言特别有效。

## 5. 头数越多越好吗？

不是。头数越多，每个头的维度 `d_k = d_model / num_heads` 越小：

| `d_model` | `num_heads` | `d_k` | 评价 |
|---|---|---|---|
| 8 | 2 | 4 | 本例 |
| 512 | 8 | 64 | BERT-base |
| 4096 | 32 | 128 | LLaMA-7B |

如果 `d_k` 太小（比如 1 或 2），每个头的信息容量不足，效果反而下降。工程上常把 `d_k` 控制在 64~128。

---

## 总结表

| 对比项 | 单头 | 多头 |
|---|---|---|
| 投影矩阵套数 | 1 | `num_heads` 套 |
| 每头 Q/K/V 维度 | `d_model` | `d_model / num_heads` |
| 注意力权重矩阵 | 1 个 | `num_heads` 个 |
| 输出 | 直接是结果 | 拼接后再投影 |
| 关注关系种类 | 一种综合标准 | 多种并行标准 |
| 参数量 | 相当 | 相当（见下文） |

一句话：

> **多头不是"更大的注意力"，而是"多个小的注意力并行"，用同样的预算换来看问题的多个视角。**

---

# `d_k = d_model / num_heads` 是怎么来的？

## 1. 为什么必须整除？

代码开头就做了校验：

```python
if d_model % num_heads != 0:
    raise ValueError("d_model 必须能被 num_heads 整除")
```

因为多头的核心操作是**把 `d_model` 维均匀切成 `num_heads` 份**：

```text
d_model = 8, num_heads = 2  →  d_k = 4  ✅
d_model = 10, num_heads = 3 →  10/3 = 3.33  ❌ 切不开
```

如果不整除，要么有余数维度无法分配，要么各头维度不一致，拼接后对不上 `d_model`。

## 2. 各头维度为什么要变小？

这是关键设计：**总预算不变**。

```text
单头：1 个头 × 8 维 = 8 维
多头：2 个头 × 4 维 = 8 维
```

如果每个头还是 8 维，2 个头拼完就是 16 维，参数量和计算量翻倍，这就不公平了。

所以多头的做法是"切蛋糕"：把原来的 8 维蛋糕切成 2 块 4 维的，每块给一个头。

## 3. 缩放因子也跟着变

代码里：

```python
scale_factor = math.sqrt(self.d_k)
```

单头示例 `d_k = 6`，除以 `√6 ≈ 2.45`；  
多头这里 `d_k = 4`，除以 `√4 = 2`。

为什么用 `d_k` 而不是 `d_model`？因为点积发生在 Q 和 K 之间，它们的维度是 `d_k`。点积的项数是 `d_k`，所以标准差随 `√d_k` 增长，缩放因子就该用 `√d_k`。

## 4. 如果 `d_k` 太小会怎样？

`d_k` 太小（比如 1），每个头只能看到 1 维信息，表达力严重不足。所以工程上会保证 `d_k` 至少在 32 以上，常见 64~128。

反过来，如果 `d_model` 固定而头数增加，`d_k` 就会下降：

```text
d_model = 8:
  num_heads = 2 → d_k = 4
  num_heads = 4 → d_k = 2
  num_heads = 8 → d_k = 1  ← 太小了
```

## 5. 一个常见误区

有人以为多头是"把输入复制 `num_heads` 份，每份还是 `d_model` 维"。

不是的。多头是**切分维度**，不是复制数据：

```text
错误理解：X(8维) × 2 份 = 两个 8 维
正确做法：X(8维) 切成两个 4 维子空间，各配一套投影
```

不过要注意：这里每个头仍然接收完整的 `X`（8 维），只是投影矩阵的输出是 4 维。所以更精确的说法是：

> **每个头都看到完整输入，但被投影到一个更小的子空间（4 维）里。**

---

## 总结

| 问题 | 回答 |
|---|---|
| 为什么 `d_model % num_heads == 0`？ | 要能均匀切分维度 |
| 为什么 `d_k = d_model / num_heads`？ | 保持总参数量与单头相当 |
| 缩放因子用哪个维度？ | `√d_k`，因为点积项数是 `d_k` |
| `d_k` 是不是越小越好？ | 不是，太小表达力不足，常见 64~128 |

一句话：

> **`d_k` 是"切蛋糕"的每块大小：切成几块由 `num_heads` 决定，但蛋糕总大小 `d_model` 不变。**

---

# 拼接与输出投影有什么用？

## 1. 为什么要拼接？

每个头输出一个 `[4, 4]` 的矩阵（4 个词，每个 4 维）。2 个头就有 2 个这样的矩阵。

拼接的目的：把所有头的信息整合回一个统一的表示，且维度回到 `d_model`。

```text
head_0: [4, 4]
head_1: [4, 4]
拼成:   [4, 8]   正好是 d_model
```

代码用 `concat_columns` 实现，保证**同一个词的各头输出排在同一行**。

## 2. 为什么还要 `W_o` 输出投影？

拼接只是把信息放在一起，还没有"融合"。`W_o` 的作用是学习各头信息之间的关系：

```python
output = matrix_multiply(concatenated, self.w_output)
```

`W_o` 形状 `[8, 8]`，把拼接后的 8 维再做一次线性变换。

如果没有 `W_o`：

- 各头的信息只是简单并列；
- 模型无法学习"头 0 的结论和头 1 的结论如何组合"；
- 头之间没有交互。

有了 `W_o`，模型可以学出类似"头 0 看语法、头 1 看指代，当两者冲突时以头 0 为准"这样的组合策略。

## 3. 为什么 `W_o` 是 `[d_model, d_model]`？

因为：

```text
输入：拼接结果 [seq_len, d_model] = [4, 8]
输出：最终结果 [seq_len, d_model] = [4, 8]
```

所以变换矩阵必须是 `[8, 8]`。

保持输入输出同维很重要，因为 Transformer Block 里有残差连接：

```text
output = LayerNorm(x + Attention(x))
```

`x` 是 8 维，注意力输出也必须是 8 维，才能相加。

## 4. 拼接 vs 平均

有人会问：为什么不把各头输出**平均**起来，而要拼接？

因为平均会丢失信息：

```text
平均：(4维 + 4维) / 2 → 还是 4 维，两头信息混在一起分不开
拼接：[4维, 4维] → 8 维，两头信息各自保留
```

拼接保留了各头的独立性，让后续的 `W_o` 自己决定如何组合。

---

## 总结表

| 操作 | 输入形状 | 输出形状 | 作用 |
|---|---|---|---|
| 各头输出 | - | `[4, 4]` × 2 | 每个头独立得出结论 |
| `concat_columns` | `[4, 4]` × 2 | `[4, 8]` | 汇总，回到 `d_model` |
| `W_o` 投影 | `[4, 8]` | `[4, 8]` | 学习各头信息的组合方式 |

一句话：

> **拼接是"把各头的报告装订成册"，`W_o` 是"读完报告后写综合结论"。**

---

# 单头 vs 多头：参数量与计算量对比

## 1. 参数量计算

以本例 `d_model = 8, num_heads = 2, d_k = 4` 计算（忽略偏置）：

**多头版**：

```text
w_queries: num_heads × (d_model × d_k) = 2 × (8 × 4) = 64
w_keys:    2 × (8 × 4) = 64
w_values:  2 × (8 × 4) = 64
w_output:  d_model × d_model = 8 × 8 = 64
总计: 64 + 64 + 64 + 64 = 256
```

**单头版**（假设也带输出投影，`d_k = 8`）：

```text
w_query:  d_model × d_k = 8 × 8 = 64
w_key:    8 × 8 = 64
w_value:  8 × 8 = 64
w_output: 8 × 8 = 64
总计: 256
```

**结论：参数量完全相同。**

这是多头设计最精妙的地方：把 8 维切成 2 个 4 维，每套权重变小一半，但有 2 套，正好抵消。

## 2. 计算量对比

主要计算是矩阵乘法，设序列长度为 `n`：

| 运算 | 单头（`d_k=8`） | 多头（2 头，每头 `d_k=4`） |
|---|---|---|
| Q/K/V 投影 | `3 × n × 8 × 8` | `3 × n × 8 × 4 × 2` = `3 × n × 8 × 8` |
| 分数 `QKᵀ` | `n² × 8` | `n² × 4 × 2` = `n² × 8` |
| 加权求和 `·V` | `n² × 8` | `n² × 4 × 2` = `n² × 8` |
| 输出投影 | `n × 8 × 8` | `n × 8 × 8` |

**计算量也基本相同。**

## 3. 那多头的"额外成本"是什么？

既然参数和计算都一样，为什么不是所有模型都用很多头？

- **头数太多会让 `d_k` 变小**，每头表达力不足；
- **并行度问题**：理论上各头并行，但实际实现中头数过多会增加内存访问开销；
- **收益递减**：头数从 1 到 8 提升明显，从 32 到 64 提升很小。

所以头数是效果与工程成本的权衡。

## 4. 对比表

| 维度 | 单头（`d_k=8`） | 多头（2 头，`d_k=4`） |
|---|---|---|
| Q/K/V 权重 | 1 套 `[8,8]` | 2 套 `[8,4]` |
| 单套权重大小 | 64 | 32 |
| 权重套数 | 1 | 2 |
| `QKᵀ` 缩放因子 | `√8 ≈ 2.83` | `√4 = 2` |
| 注意力权重矩阵 | 1 个 `[n,n]` | 2 个 `[n,n]` |
| 输出 | 直接 | 拼接 + `W_o` |
| 总参数量 | 256 | 256 |
| 关注视角 | 1 种 | 2 种 |

一句话：

> **多头注意力是"免费升级"：参数量和计算量不变，但获得了多个并行的观察视角。**

---

# 附：容易忽略的细节

## 1. 代码用"独立投影"而非"大矩阵切分"

标准 Transformer 的常见实现是：

```text
用一个大矩阵 W_q [d_model, d_model] 投影
然后按列切成 num_heads 份
```

本代码用的是：

```text
num_heads 个小矩阵 W_q^i [d_model, d_k]
各自投影
```

**两者数学上等价**——把大矩阵按列切开，就是这些小矩阵。代码用列表 `w_queries` 更直观地表达了"每个头有自己的权重"。

## 2. 为什么 `attention_weights` 要返回出来？

虽然 `forward` 的核心输出是 `output`，但代码也返回了 `attention_weights` 列表。

原因：

- 方便观察每个头学到了什么；
- 实际应用中，注意力权重常用于可视化（比如看模型关注了哪些词）；
- 教学代码里，把这些中间结果暴露出来便于理解。

`main()` 里正是用它来打印每个头的权重矩阵。

## 3. 为什么缩放用 `self.d_k` 而不是 `self.d_model`？

因为点积发生在 Q 和 K 之间，它们的维度是 `d_k`（本例 4），不是输入维度 `d_model`（本例 8）。

点积是 `d_k` 项相乘再相加，其方差随 `d_k` 增长，所以缩放因子必须是 `√d_k`。

## 4. 各头的随机权重会不会相同？

不会。虽然都用 `random.Random(42)`，但同一个 `rng` 实例被连续调用，每次生成不同的数：

```python
self.gate_queries = [random_matrix(...) for _ in range(num_heads)]
```

列表推导里 2 次调用 `random_matrix`，用的是同一个 `rng` 的顺序输出，所以 `w_queries[0]` 和 `w_queries[1]` 不同。这保证各头从不同的随机初始化出发，有机会学到不同的模式。

## 5. 这个多头模块如何接入完整 Transformer？

真实 Transformer Block 的结构：

```text
输入 x
  ↓
多头注意力(x)              ← 本代码实现的部分
  ↓ 残差连接 + LayerNorm
FFN(x)                     ← feed_forward_network.py 实现的部分
  ↓ 残差连接 + LayerNorm
输出
```

本代码加上 `positional_encoding.py`（位置编码）和 `feed_forward_network.py`（FFN），就凑齐了 Transformer Block 的主要组件。

## 6. 为什么没有 mask？

真实 Transformer 里还有掩码机制：

- **Padding mask**：屏蔽填充位；
- **Causal mask**：Decoder 里屏蔽未来词（防止偷看答案）。

这份代码是纯演示，输入没有 padding，也不做生成任务，所以不需要 mask。实际使用时要在 Softmax 之前把被屏蔽位置的分数设为极小值。

---

一句话总结全文：

> **多头注意力把输入投影到多个低维子空间，每个头独立做缩放点积注意力，再拼接并用 `W_o` 融合；它在参数量和计算量与单头相当的前提下，让模型同时从多个视角理解序列。**
