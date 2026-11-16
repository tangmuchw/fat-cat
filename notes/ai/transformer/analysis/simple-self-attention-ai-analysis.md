[toc]

---

这段代码是在用**纯 Python 标准库**演示 Transformer 里最核心的 **Self-Attention（自注意力）前向传播**。你可以把它理解成：

> 输入 4 个词向量，每个词都去“看看”序列里其他词，计算应该关注谁，然后根据关注程度把其他词的信息加权汇总，得到每个词的新表示。

下面按小白视角拆解。

---

# 代码实现分析

## 1. 整体流程一句话

输入矩阵 `X` 形状是 `[4, 8]`，表示 4 个词、每个词 8 维。经过三步：

1. 用三个权重矩阵把 `X` 投影成 `Q`、`K`、`V`；
2. 用 `Q` 和 `K` 算词与词之间的相关性分数，做缩放和 Softmax；
3. 用注意力权重对 `V` 加权求和，得到输出。

最终输出形状是 `[4, 6]`：4 个词，每个词变成 6 维的新向量。

---

## 2. 核心概念：Q、K、V 是什么？

自注意力里有三个角色：

- **Q：Query，查询**  
  当前词想“问”什么，想找什么样的信息。
- **K：Key，键**  
  每个词能提供什么信息，用来和 Q 匹配。
- **V：Value，值**  
  每个词真正包含的内容，最后被加权汇总。

代码里用三个权重矩阵：

```python
self.w_query
self.w_key
self.w_value
```

它们形状都是 `[d_model, d_k]`，这里是 `[8, 6]`。

输入 `X` 是 `[4, 8]`，所以：

```python
Q = X @ W_query   # [4,8] @ [8,6] = [4,6]
K = X @ W_key     # [4,6]
V = X @ W_value   # [4,6]
```

`@` 表示矩阵乘法。代码里用 `matrix_multiply` 实现。

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

Softmax 的作用：把一组任意实数变成**概率分布**，每个数在 0 到 1 之间，并且总和为 1。

比如：

```python
softmax([1, 2, 3])
```

会得到类似：

```python
[0.09, 0.24, 0.67]
```

代码里先减去最大值 `max_val`，是为了防止 `math.exp` 数值太大溢出，这是常见写法，不改变结果。

在自注意力里，Softmax 用来把“注意力分数”变成“注意力权重”。

---

### 3.2 `matrix_multiply(a, b)`

```python
def matrix_multiply(a: Matrix, b: Matrix) -> Matrix:
```

这是标准矩阵乘法：

- `a` 形状 `m × n`
- `b` 形状 `n × p`
- 输出形状 `m × p`

三重循环：

```python
for i in range(m):
    for j in range(p):
        for k in range(n):
            result[i][j] += a[i][k] * b[k][j]
```

就是结果第 `i` 行第 `j` 列，等于 `a` 的第 `i` 行和 `b` 的第 `j` 列逐项相乘再相加。

---

### 3.3 `transpose(matrix)`

```python
return [list(row) for row in zip(*matrix)]
```

矩阵转置：行变列，列变行。

比如：

```python
[[1, 2],
 [3, 4]]
```

转置后：

```python
[[1, 3],
 [2, 4]]
```

后面算 `Q · Kᵀ` 时要用到。

---

### 3.4 `SimpleSelfAttention.__init__`

```python
def __init__(self, d_model: int, d_k: int) -> None:
```

初始化三个权重矩阵：

```python
self.w_query
self.w_key
self.w_value
```

每个都是 `[d_model, d_k]`，即 `[8, 6]`。

权重用：

```python
rng = random.Random(42)
rng.normalvariate(0, 0.1)
```

生成均值为 0、标准差为 0.1 的随机小数。

`Random(42)` 表示固定随机种子 42，所以每次运行生成的权重都一样，方便复现实验结果。

---

### 3.5 `project(x)`

```python
def project(self, x: Matrix) -> tuple[Matrix, Matrix, Matrix]:
    q = matrix_multiply(x, self.w_query)
    k = matrix_multiply(x, self.w_key)
    v = matrix_multiply(x, self.w_value)
```

把输入 `x` 分别乘三个权重矩阵，得到：

```python
q: [4, 6]
k: [4, 6]
v: [4, 6]
```

代码会打印它们的形状。

---

### 3.6 `forward(x)`：自注意力完整流程

这是最核心的方法。

#### 步骤 1：计算 Q、K、V

```python
q, k, v = self.project(x)
```

#### 步骤 2：计算注意力分数

```python
scores = matrix_multiply(q, transpose(k))
```

公式是：

```text
scores = Q · Kᵀ
```

形状变化：

```text
Q:      [4, 6]
Kᵀ:     [6, 4]
scores: [4, 4]
```

`[4, 4]` 的含义是：4 个词，每个词对 4 个词都有一个分数。

第 `i` 行第 `j` 列表示：

> 第 i 个词对第 j 个词的关注分数。

分数越大，表示越相关。

#### 步骤 3：缩放

```python
scale_factor = math.sqrt(self.d_k)
scores_scaled = [[val / scale_factor for val in row] for row in scores]
```

这里 `d_k = 6`，所以除以：

```text
sqrt(6) ≈ 2.449
```

为什么要缩放？  
因为 Q 和 K 点积后数值可能变大，Softmax 会变得很“尖锐”，训练不稳定。除以 `sqrt(d_k)` 是标准做法，叫**缩放点积注意力**。

#### 步骤 4：Softmax

```python
attention_weights = [softmax(row) for row in scores_scaled]
```

对每一行做 Softmax。

原来 `scores_scaled` 是 `[4, 4]`，Softmax 后仍然是 `[4, 4]`，但每一行变成概率：

```text
第 i 行：第 i 个词对所有词的注意力权重，总和为 1
```

比如某一行可能是：

```text
[0.2, 0.3, 0.1, 0.4]
```

表示当前词把 20% 注意力给词 0，30% 给词 1，10% 给词 2，40% 给词 3。

#### 步骤 5：加权求和

```python
output = matrix_multiply(attention_weights, v)
```

形状：

```text
attention_weights: [4, 4]
v:                 [4, 6]
output:            [4, 6]
```

含义：

> 每个词的新向量，等于所有词的 V 向量按注意力权重加权平均。

比如词 0 的输出：

```text
output[0] = w00 * v[0] + w01 * v[1] + w02 * v[2] + w03 * v[3]
```

其中 `w00 + w01 + w02 + w03 = 1`。

---

## 4. `main()` 里输入是什么？

```python
d_model = 8
d_k = 6
```

输入：

```python
x_input = [
    [1, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0],
]
```

这是 4 个词，每个词 8 维。前 4 维是 one-hot 形式，方便演示。

然后：

```python
attn = SimpleSelfAttention(d_model=8, d_k=6)
output, _ = attn.forward(x_input)
```

得到输出 `output`，形状 `[4, 6]`。

最后打印每个词的新输出。

---

## 5. 形状总表

| 变量 | 形状 | 含义 |
|---|---|---|
| `X` | `[4, 8]` | 4 个词，每个词 8 维 |
| `W_query/W_key/W_value` | `[8, 6]` | 投影权重 |
| `Q/K/V` | `[4, 6]` | 投影后的查询、键、值 |
| `scores` | `[4, 4]` | 词与词的原始注意力分数 |
| `scores_scaled` | `[4, 4]` | 缩放后的分数 |
| `attention_weights` | `[4, 4]` | Softmax 后的注意力权重，每行和为 1 |
| `output` | `[4, 6]` | 每个词的新表示 |

---

## 6. 这段代码演示了什么？

它完整演示了缩放点积自注意力的公式：

```text
Attention(Q, K, V) = Softmax(QKᵀ / sqrt(d_k)) · V
```

对应代码：

```python
scores = Q @ Kᵀ
scores_scaled = scores / sqrt(d_k)
attention_weights = Softmax(scores_scaled)
output = attention_weights @ V
```

---

## 7. 小白需要注意的点

1. **这不是完整 Transformer**  
   没有多头注意力、位置编码、残差连接、LayerNorm、前馈网络等，只是单头自注意力前向传播。

2. **输入 4 个词没有顺序信息**  
   自注意力本身不知道词序，实际 Transformer 会加位置编码。

3. **权重是随机初始化的**  
   所以输出数值没有实际语义，只是演示计算流程。固定种子 42 保证每次结果一样。

4. **注意力权重每一行和为 1**  
   这表示每个词把 100% 的注意力分配给序列里的各个词。

5. **输出每个词都融合了全序列信息**  
   因为每个词的输出都是所有词 V 的加权和。

---

## 总结

这段代码用非常直观的方式实现了：

```text
输入 X
  ↓ 线性投影
Q、K、V
  ↓ Q 和 K 点积
注意力分数
  ↓ 除以 sqrt(d_k)
缩放分数
  ↓ Softmax
注意力权重
  ↓ 对 V 加权求和
输出
```

它把自注意力中最关键的公式和每一步中间结果都打印出来了，非常适合小白理解 Self-Attention 的计算过程。

---


# 为什么 Q · Kᵀ 是 注意力分数？

## 1. 从形状上看：为什么必须是 `Q · Kᵀ`

你的设定：

```text
Q:  [4, 6]   4 个词，每个词 6 维 query
K:  [4, 6]   4 个词，每个词 6 维 key
```

注意力分数要表达的是：

> 第 i 个词对第 j 个词的关注分数

所以分数矩阵应该是 `[4, 4]`：4 个词 × 4 个词。

矩阵乘法规则：

```text
[m, n] · [n, p] = [m, p]
```

要得到 `[4, 4]`，只有两种可能：

```text
Q · Kᵀ : [4, 6] · [6, 4] = [4, 4]   ✅ 正确
Kᵀ · Q : [6, 4] · [4, 6] = [6, 6]   ❌ 形状不对
```

`Kᵀ · Q` 得到的是 `[6, 6]`，它的行列含义是“6 个特征维度之间的关系”，不是“4 个词之间的关系”，所以不能当注意力分数。

**所以第一层原因：只有 `Q · Kᵀ` 的形状才是 `[词数, 词数]`。**

---

## 2. 从矩阵乘法元素上看：`Q · Kᵀ` 到底算的是什么

矩阵乘法 `C = A · B` 的定义是：

```text
C[i][j] = A 的第 i 行 · B 的第 j 列
```

现在令 `A = Q`，`B = Kᵀ`：

```text
Q 的第 i 行       = q_i     （第 i 个词的 query 向量）
Kᵀ 的第 j 列      = K 的第 j 行 = k_j  （第 j 个词的 key 向量）
```

所以：

```text
scores[i][j] = q_i · k_j
```

也就是：

> **第 i 个词的 query 向量，和第 j 个词的 key 向量，做点积。**

这就是“第 i 个词对第 j 个词的注意力分数”。

---

## 3. 为什么点积能表示“注意力/相关性”？

点积的几何意义：

```text
q · k = |q| · |k| · cos(θ)
```

其中 `θ` 是 `q` 和 `k` 的夹角。

- 两个向量**方向越接近**，`cos(θ)` 越接近 1，点积越大；
- 两个向量**方向越垂直**，`cos(θ)` 接近 0，点积接近 0；
- 两个向量**方向相反**，点积为负。

所以点积大，表示：

> 第 i 个词想找的信息（query），和第 j 个词能提供的信息（key），**匹配度高**。

注意力机制就是：

> 用 query 去“匹配”所有 key，匹配度高的词，获得更高的注意力权重。

这就是为什么用点积：**它天然衡量两个向量的相似度，而且可以用矩阵乘法一次算完所有词对。**

---

## 4. 转置到底做了什么？

`K` 原本是：

```text
K 的第 0 行 = k_0
K 的第 1 行 = k_1
K 的第 2 行 = k_2
K 的第 3 行 = k_3
```

转置后 `Kᵀ`：

```text
Kᵀ 的第 0 列 = k_0
Kᵀ 的第 1 列 = k_1
Kᵀ 的第 2 列 = k_2
Kᵀ 的第 3 列 = k_3
```

矩阵乘法 `Q · Kᵀ` 时：

```text
结果第 i 行第 j 列 = Q 的第 i 行 · Kᵀ 的第 j 列
                   = q_i · k_j
```

**转置的目的，就是把 K 的“行”变成“列”，让矩阵乘法能够做“行 · 行”的点积。**

如果不转置，`Q · K` 是 `[4,6] · [4,6]`，形状不合法，根本乘不了。

---

## 5. 如果反过来写 `Kᵀ · Q` 会怎样？

```text
Kᵀ · Q : [6, 4] · [4, 6] = [6, 6]
```

结果第 `a` 行第 `b` 列是：

```text
Kᵀ 的第 a 行 · Q 的第 b 列
= K 的第 a 列 · Q 的第 b 列
```

这算的是“K 的第 a 个特征维度”和“Q 的第 b 个特征维度”之间的关系，**不是词与词之间的关系**，所以没有注意力含义。

---

## 6. 顺便说：为什么要除以 `sqrt(d_k)`

点积是 `d_k` 个数相乘再相加。维度越大，点积的数值波动越大，方差大约和 `d_k` 成正比。

如果不缩放，Softmax 容易变得非常“尖锐”，几乎变成 one-hot，梯度很小，训练不稳定。

所以标准做法是：

```text
scores = Q · Kᵀ / sqrt(d_k)
```

这就是“缩放点积注意力”名字的由来。

---

## 总结

| 问题 | 回答 |
|---|---|
| 代码里是 `Kᵀ · Q` 吗？ | 不是，是 `Q · Kᵀ` |
| 为什么必须 `Q · Kᵀ`？ | 只有它的形状是 `[词数, 词数]` |
| `Q · Kᵀ` 的元素是什么？ | `scores[i][j] = q_i · k_j` |
| 为什么点积能当分数？ | 点积衡量两个向量方向相似度，越大越相关 |
| 转置的作用？ | 把 K 的行变成列，使矩阵乘法能做“行·行”点积 |
| 为什么除以 `sqrt(d_k)`？ | 防止点积随维度变大导致 Softmax 过尖锐 |

一句话：

> **`Q · Kᵀ` 的第 i 行第 j 列，就是第 i 个词的 query 和第 j 个词的 key 的点积，点积越大表示越匹配，所以它就是注意力分数。**

---

一句话答案：

> 因为 `Q·Kᵀ` 的每个元素是 `d_k` 个数相乘再相加，**维度越大，数值波动越大**；除以 `√d_k` 是为了把方差拉回和维度无关的水平，防止 Softmax 变得过“尖锐”，导致梯度消失、训练不稳定。

下面拆开讲。

---

## 1. 先看 `Q·Kᵀ` 的元素是什么

对第 `i` 个词和第 `j` 个词：

```text
score[i][j] = q_i · k_j = q_i1*k_j1 + q_i2*k_j2 + ... + q_i,d_k*k_j,d_k
```

一共 `d_k` 项相加。

你的代码里 `d_k = 6`，所以是 6 项相加。如果 `d_k = 512`，就是 512 项相加。

**项数越多，和的波动越大**，这是关键。

---

## 2. 方差推导：为什么是 `√d_k`

假设 `q` 和 `k` 的每个分量都是独立同分布，均值 0，方差 1（实际初始化大致如此）。

单看一项 `q_i * k_j`：

```text
E[q_i * k_j] = E[q_i] * E[k_j] = 0
Var(q_i * k_j) = E[q_i²] * E[k_j²] - 0 = 1 * 1 = 1
```

所以每一项的方差是 1。

现在有 `d_k` 项独立相加：

```text
Var(score) = d_k * 1 = d_k
```

标准差：

```text
std(score) = √d_k
```

也就是说：

> **点积的标准差随 `√d_k` 增长。**

`d_k = 6` 时，标准差约 `2.45`；`d_k = 512` 时，标准差约 `22.6`。

除以 `√d_k` 后：

```text
Var(score / √d_k) = d_k / d_k = 1
```

**方差重新变成 1，和维度无关。** 这就是 `√d_k` 的来源——不是拍脑袋，是让缩放后的分数方差稳定在 1 左右。

---

## 3. 不缩放会怎样？Softmax 会“饱和”

Softmax 的定义：

```text
softmax(x_i) = exp(x_i) / Σ exp(x_j)
```

如果输入数值很大，比如：

```text
[10, 1, 0, 0]
```

Softmax 后：

```text
[0.9999, 0.0001, 0.0000, 0.0000]
```

几乎变成 **one-hot**，所有注意力都压在一个词上。

这有两个问题：

**问题一：梯度消失**

Softmax 在输入很大时，输出接近 0 或 1，导数接近 0：

```text
∂softmax/∂x ≈ 0
```

反向传播时梯度几乎传不回去，参数学不动。

**问题二：训练不稳定**

`d_k` 越大，分数波动越大，Softmax 越容易饱和，模型越难训练。

除以 `√d_k` 后，分数保持在合理范围，Softmax 输出比较“平滑”，梯度更健康。

---

## 4. 数值例子对比

假设某一行缩放前的分数是：

```text
[10, 2, 1, 0]
```

**不缩放**，Softmax：

```text
exp(10)=22026, exp(2)=7.39, exp(1)=2.72, exp(0)=1
总和 ≈ 22037
输出 ≈ [0.9995, 0.00034, 0.00012, 0.00005]
```

几乎 one-hot，梯度极小。

**除以 `√d_k`**，假设 `√d_k = 3`：

```text
[3.33, 0.67, 0.33, 0]
```

Softmax：

```text
exp(3.33)=27.9, exp(0.67)=1.95, exp(0.33)=1.39, exp(0)=1
总和 ≈ 32.2
输出 ≈ [0.866, 0.061, 0.043, 0.031]
```

分布更平滑，梯度更健康。

---

## 5. 结合你的代码

```python
scale_factor = math.sqrt(self.d_k)
scores_scaled = [[val / scale_factor for val in row] for row in scores]
```

你的 `d_k = 6`，所以：

```text
√6 ≈ 2.449
```

每个分数除以 2.449。

如果 `d_k` 是 64，就除以 8；如果 `d_k` 是 512，就除以约 22.6。

**维度越大，除得越多**，正好抵消点积方差随维度增长的趋势。

---

## 6. 常见误解澄清

**误解一：除以 `d_k` 不是更好吗？**

除以 `d_k` 会让方差变成 `1/d_k`，维度越大分数越小，Softmax 会变得太“平”，注意力区分度不够。`√d_k` 是让方差稳定在 1，不多不少。

**误解二：这是不是某种归一化？**

不是 LayerNorm 那种归一化。它只是一个**固定的缩放常数**，不依赖具体数据，目的是控制数值范围。

**误解三：为什么不是 `√(d_model)`？**

因为点积发生在 `Q` 和 `K` 之间，它们的维度是 `d_k`，不是输入维度 `d_model`。缩放因子跟点积的项数有关，所以用 `d_k`。

---

## 7. 总结

| 问题 | 回答 |
|---|---|
| 点积为什么波动大？ | `d_k` 项相加，方差 ≈ `d_k`，标准差 ≈ `√d_k` |
| 除以 `√d_k` 后？ | 方差变回 1，和维度无关 |
| 不缩放会怎样？ | Softmax 饱和成 one-hot，梯度消失，训练不稳定 |
| 为什么不是 `d_k`？ | 除 `d_k` 会让方差太小，注意力太平均 |
| 这个操作的名称？ | 缩放点积注意力（Scaled Dot-Product Attention） |

一句话：

> **`√d_k` 是点积标准差的理论值，除以它把分数方差拉回 1，让 Softmax 工作在梯度健康的区间。**

---

# d_model 与 d_k 的关系？

一句话答案：

> **数学上两者没有强制约束，`d_k` 可以大于、等于或小于 `d_model`；但工程惯例是 `d_k ≤ d_model`，标准 Transformer 里 `d_k = d_model / num_heads`。**

下面把两者的关系讲清楚。

---

## 1. 形状上的关系

你的代码里：

```python
self.w_query: [d_model, d_k]
self.w_key:    [d_model, d_k]
self.w_value:  [d_model, d_k]
```

投影：

```text
X:      [seq_len, d_model]
Q/K/V:  [seq_len, d_k]
```

所以：

| 参数 | 作用 | 出现的位置 |
|---|---|---|
| `d_model` | 输入词向量的维度 | `X` 的列数，权重矩阵的**行数** |
| `d_k` | 投影后 Q/K/V 的维度 | Q/K/V 的列数，权重矩阵的**列数** |

**`d_model` 是“入口宽度”，`d_k` 是“出口宽度”。**  
权重矩阵 `[d_model, d_k]` 就是一个线性变换，把 `d_model` 维映射到 `d_k` 维。

---

## 2. 数学上没有强制约束

矩阵乘法要求：

```text
[seq_len, d_model] · [d_model, d_k] = [seq_len, d_k]
```

**只要 `d_model` 是权重矩阵的行数，就能乘。**  
`d_k` 比 `d_model` 大、小、相等，都不影响形状合法性。

所以：

```python
d_model = 8, d_k = 6   # 降维，合法
d_model = 8, d_k = 8   # 等维，合法
d_model = 4, d_k = 8   # 升维，合法
```

三种都能跑，代码不会报错。

---

## 3. 但表达力受 `min(d_model, d_k)` 限制

矩阵乘法有个性质：

```text
rank(X · W) ≤ min(rank(X), rank(W)) ≤ min(d_model, d_k)
```

所以 `Q/K/V` 的秩最多是：

```text
min(seq_len, d_model, d_k)
```

含义：

- 如果 `d_k > d_model`，多出来的维度是**线性相关的冗余维度**，不会增加信息量（上一轮已经讲过）；
- 如果 `d_k < d_model`，是在**降维**，会损失一部分信息，但这是主动选择，通常是为了减少计算量或分头。

**真正决定“能表达多少信息”的，是 `min(d_model, d_k)`，不是单独某一个。**

---

## 4. 工程惯例：`d_k ≤ d_model`

标准 Transformer 里：

```text
d_k = d_model / num_heads
```

所以：

```text
d_k ≤ d_model
```

例子：

| 模型 | `d_model` | `num_heads` | `d_k` |
|---|---|---|---|
| BERT-base | 768 | 12 | 64 |
| GPT-3 | 12288 | 96 | 128 |
| 你的代码 | 8 | 1（单头） | 6 |

为什么这样设计？

- 多头注意力把 `d_model` **切分**成 `num_heads` 份，每份是 `d_k`；
- 所有头的输出拼起来，总维度还是 `d_model`；
- 所以 `d_k` 天然 ≤ `d_model`。

你的代码是**单头**，没有切分，所以 `d_k` 可以自由设。但让它大于 `d_model` 没有收益，通常取 `d_k ≤ d_model`。

---

## 5. 两者各自影响什么？

### `d_model` 影响：

- 输入词向量的维度；
- 权重矩阵的行数；
- **输入信息量的上限**；
- 投影的计算量（`seq_len × d_model × d_k`）。

### `d_k` 影响：

- Q/K/V 的维度；
- 点积的项数，从而影响缩放因子 `√d_k`；
- 注意力分数的数值波动；
- **输出维度**（这段代码输出是 `[seq_len, d_k]`）；
- 点积的计算量（`seq_len² × d_k`）。

---

## 6. 这段代码的一个特殊之处：没有输出投影

标准 Transformer 的自注意力输出会再乘一个输出投影矩阵：

```text
output = Attention(Q, K, V) · W_o
W_o: [d_k, d_model]
```

这样输出维度会**回到 `d_model`**，方便后面接残差连接和 LayerNorm。

但你的代码里：

```python
output = matrix_multiply(attention_weights, v)
# output: [seq_len, d_k]
```

**没有 `W_o`，输出停在 `d_k` 维。**  
所以在这段代码里，`d_k` 直接决定了最终输出的维度。

如果要补完整，可以加：

```python
self.w_output: Matrix = [[rng.normalvariate(0, 0.1) for _ in range(d_model)]
                         for _ in range(d_k)]
# 然后 output = matrix_multiply(output, self.w_output)  # [seq_len, d_model]
```

---

## 7. 用一个比喻总结

把输入 `X` 想成 **`seq_len` 个人，每人有 `d_model` 条信息**。

- `W_query/W_key/W_value` 是**三个翻译官**，把每个人的 `d_model` 条信息翻译成 `d_k` 条；
- `d_k` 是翻译后的“信息条数”：
  - `d_k < d_model`：压缩翻译，损失一些细节；
  - `d_k = d_model`：等量翻译；
  - `d_k > d_model`：多翻译出一些条目，但多出来的都是原文的线性组合，不是新信息。

---

## 8. 总结表

| 关系 | 是否合法 | 效果 | 推荐 |
|---|---|---|---|
| `d_k < d_model` | ✅ | 降维，减少计算，标准多头做法 | 推荐 |
| `d_k = d_model` | ✅ | 等维，单头常见 | 可以 |
| `d_k > d_model` | ✅ | 升维但秩不变，冗余维度，浪费参数 | 不推荐 |

一句话：

> **`d_model` 是输入宽度，`d_k` 是投影后宽度；数学上无约束，但有效表达力受 `min(d_model, d_k)` 限制。标准做法是 `d_k = d_model / num_heads ≤ d_model`。**