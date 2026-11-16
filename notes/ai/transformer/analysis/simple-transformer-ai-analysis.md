[toc]

---

这段代码是在用**纯 Python 标准库**（不依赖 PyTorch / NumPy）从零实现一个**简化的 Transformer**，并按 8 个步骤递进：

> 1. 层归一化 → 2. 自注意力（带掩码）→ 3. 多头注意力 → 4. FFN → 5. Transformer 层 → 6. 位置编码 → 7. 组装完整模型 → 8. 训练循环。

为了能真正训练，代码开头还实现了一个**极简的自动微分引擎（Tensor）**，让模型能自己算梯度、更新参数。最后脚本会在一个小型序列预测任务上训练，并打印损失下降与生成结果。

这份文档按小白视角拆解，并用一个**学生学写数字接龙**的比喻，贯穿解释"训练"和"最后的输出"到底是什么。

---

# 先讲清一个前提：学生只认识 8 个数字

把模型想成一个**刚开始学写数字接龙的学生**。

先说一个前提：这个学生手里只有 **8 张数字卡片**，上面写着 0 到 7。他只认识这 8 个数字，别的都不认识。

```text
卡片： [0] [1] [2] [3] [4] [5] [6] [7]
```

这就是代码里的 `vocab_size = 8`——词表只有 8 个 token（编号为 0~7）。

**为什么这很重要？** 因为模型处理输入时，第一步是把每个 token 变成 one-hot，也就是"从这 8 张卡片里抽出对应的那张"：

```text
输入数字 2 → 抽出 [2] 号卡片 → 变成 [0,0,1,0,0,0,0,0]
```

如果有人递给他一张写着"8"的纸条，他手里的卡片里根本没有 8 号，自然没法处理——这就是 `prompt=[8,9,10]` 报错的原因（详见文末附录第 5 条）。

## 主线比喻：学生怎么做题、怎么考试

前提清楚了，再看学习过程：

| 代码里的东西 | 比喻里的角色 |
|---|---|
| 训练数据（16 个样本） | 练习册上的 16 道题，都是"给 8 个数字，接着写 8 个" |
| 模型 `SimpleTransformer` | 这个学生 |
| 训练循环（前向→损失→反向→更新） | 学生做题 → 老师批改 → 学生订正 |
| 损失下降 | 作业错题越来越少 |
| 生成测试（最后的输出） | 闭卷考试：只给个开头，让学生自己往下接 |
| 提示词 `[0,1,2]` | 老师给的开头 |
| 生成结果 == 期望模式 | 学生写的答案和标准答案一致 → 真学会了 |

练习册上的题都藏着同一个规律：**数到 7 就回到 0**，即 `0,1,2,3,4,5,6,7,0,1,...`。

记住这张表，后面所有内容都能对上号。

---

# 代码实现分析

## 1. 整体流程一句话

程序分两大阶段：

**阶段一：搭建模型（步骤 1-7）**

```text
词向量 → +位置编码 → [Transformer 层 × 2] → 输出头 → logits
```

**阶段二：训练与考试（步骤 8）**

```text
练习册（16 道题）→ 反复做题订正 30 轮 → 损失下降
                 → 现场考试（给开头 [0,1,2]，让模型续写）
```

---

## 2. 为什么开头先写一个 autograd 引擎？

正常情况用 PyTorch，反向传播由框架自动完成。这里从零实现，所以必须先造一个"能自动求导的 Tensor"。

### 2.1 `Tensor` 是什么？

```python
class Tensor:
    def __init__(self, data, requires_grad=False, children=(), op=""):
        self.data = data          # 存的数值（二维矩阵）
        self.requires_grad = ...  # 是否需要求导
        self.grad = ...           # 梯度
        self._children = children # 计算图里的"上游节点"
        self._backward = ...      # 反向函数
```

每个 Tensor 不仅存**数值**，还记着**自己是怎么算出来的**（`children` 和 `op`）以及**怎么把梯度传回去**（`_backward`）。

这就是"计算图"：

```text
a ─┐
   ├─→ c ─→ loss
b ─┘
```

反向传播时，从 `loss` 出发，沿着计算图逆序调用每个节点的 `_backward`，把梯度一路传回所有参数。

### 2.2 支持的操作

`Tensor` 重载了常用运算：

| 操作 | 前向 | 反向（`_backward` 做的事） |
|---|---|---|
| `+` | 逐元素相加 | 梯度原样传给两边（广播的要求和） |
| `*` | 逐元素相乘 | 梯度乘上对方的数值 |
| `@` | 矩阵乘法 | `dA = dC·Bᵀ`，`dB = Aᵀ·dC` |
| `**` | 逐元素幂 | `n·x^(n-1)·梯度` |
| `softmax` | 逐行归一化 | 雅可比矩阵乘法 |
| `relu` | 负数归零 | 正数处梯度通过，负数处截断 |
| `mean` | 求均值 | 梯度平均分给每个元素 |

### 2.3 比喻

这就像给学生配了一套**自动批改+自动定位错误**的工具：

> 学生每做一步，工具都记下"这一步用了什么、上一步是什么"。做错时，能顺着步骤倒推，精确指出"是第 3 步的那个系数该调大还是调小"。

---

## 3. 步骤 1-6：搭积木（各模块）

这 6 步在之前的独立示例里都详细讲过，这里只讲它们在完整模型里怎么配合。

### 步骤 1：层归一化 `LayerNorm`

```python
class LayerNorm(Module):
    def __call__(self, x):
        avg = x.mean(axis=1)
        centered = x - avg
        var = (centered * centered).mean(axis=1)
        std = (var + self.eps) ** 0.5
        return centered / std * self.gamma + self.beta
```

对每个样本（每行）独立归一化，再用可学习的 gamma/beta 微调。用的是 **Pre-LN**：先归一化，再送进子层。

### 步骤 2：自注意力（带因果掩码）

```python
def causal_mask(seq_len):
    data = [[-1e9 if j > i else 0.0 for j in range(seq_len)]
            for i in range(seq_len)]
    return Tensor(data)

def scaled_dot_product_attention(q, k, v, mask=None):
    scores = (q @ k.transposed()) * (1.0 / math.sqrt(d_k))
    if mask is not None:
        scores = scores + mask
    return scores.softmax() @ v
```

**因果掩码**是关键：上三角（未来位置）设为 -1e9，Softmax 后变成 0，保证模型预测第 `i` 个词时**看不到后面的词**。

对应比喻里的规则：**不许偷看答案**。

### 步骤 3：多头注意力

```python
class MultiHeadAttention(Module):
    def __call__(self, x, mask=None):
        q, k, v = self.wq(x), self.wk(x), self.wv(x)
        heads = []
        for head in range(self.num_heads):
            q_h = q.slice_cols(start, end)
            ...
            heads.append(scaled_dot_product_attention(q_h, k_h, v_h, mask))
        return self.wo(cat_columns(heads))
```

`slice_cols` / `cat_columns` 是 autograd 版本的切片和拼接，梯度能正确回传到对应列。

### 步骤 4：FFN

```python
class FeedForward(Module):
    def __call__(self, x):
        return self.w2(self.w1(x).relu())
```

两层线性 + ReLU，对每个位置独立加工。

### 步骤 5：Transformer 层（Pre-LN）

```python
class TransformerBlock(Module):
    def __call__(self, x, mask=None):
        x = x + self.attn(self.attn_norm(x), mask)   # 注意力子层
        x = x + self.ffn(self.ffn_norm(x))           # FFN 子层
        return x
```

Pre-LN 结构：先归一化再进子层，残差路径保持畅通，训练更稳定。

### 步骤 6：位置编码

```python
def positional_encoding(seq_len, d_model):
    for pos in range(seq_len):
        for dim in range(d_model):
            rate = 1.0 / (10000 ** (2 * (dim // 2) / d_model))
            row.append(math.sin(pos * rate) if dim % 2 == 0
                       else math.cos(pos * rate))
```

正弦位置编码，给注意力注入顺序信息（否则模型分不清"0,1,2"和"2,1,0"）。

---

## 4. 步骤 7：组装完整模型

```python
class SimpleTransformer(Module):
    def __init__(self, vocab_size, d_model, num_heads,
                 num_layers, d_ff, max_seq_len, rng):
        self.embed = Linear(vocab_size, d_model, rng)   # one-hot → 词向量
        self.pos = positional_encoding(max_seq_len, d_model)
        self.blocks = [TransformerBlock(...) for _ in range(num_layers)]
        self.final_norm = LayerNorm(d_model)
        self.head = Linear(d_model, vocab_size, rng)    # 输出词表 logits
        self.mask = causal_mask(max_seq_len)

    def __call__(self, token_ids):
        x = self.embed(one_hot(token_ids, vocab_size))
        x = x + 位置编码
        for block in self.blocks:
            x = block(x, mask)
        return self.head(self.final_norm(x))
```

完整的数据流：

```text
token ids [seq]
  ↓ one-hot
[seq, vocab_size]
  ↓ embed
[seq, d_model]          词向量
  ↓ + 位置编码
[seq, d_model]          带位置的词向量
  ↓ TransformerBlock ×2
[seq, d_model]          深层语义表示
  ↓ final_norm + head
[seq, vocab_size]       logits（每个位置对词表的打分）
```

`logits` 的每一行是一个概率分布（过 Softmax 后），表示"这个位置下一个词最可能是哪个 token"。

---

## 5. 步骤 8：训练循环

### 5.1 数据：周期性序列

```python
def build_dataset(vocab_size, seq_len):
    tokens = list(range(vocab_size)) * 3   # [0,1,2,...,7, 0,1,2,...,7, 0,1,...]
    for start in range(len(tokens) - seq_len):
        x = tokens[start:start + seq_len]
        y = tokens[start + 1:start + seq_len + 1]
        samples.append((x, y))
```

任务是**给定 8 个 token，预测后 8 个 token**。数据规律是数到 7 就回到 0。

对应比喻：**练习册上的 16 道题，都是同一套找规律题**。

### 5.2 训练四步曲

```python
for epoch in range(epochs):
    for x_ids, y_ids in samples:
        optimizer.zero_grad()      # ① 清空旧梯度
        logits = model(x_ids)      # ② 前向：学生做题
        loss = cross_entropy(logits, y_ids)  # ③ 算损失：老师批改
        loss.backward()            # ④ 反向：定位哪里错了
        optimizer.step()           # ⑤ 更新：学生订正
```

- **前向**：模型读 8 个输入 token，输出对下一个词的预测；
- **损失**：交叉熵，衡量预测分布和真实答案的差距；
- **反向**：autograd 自动算出每个参数该怎么调整；
- **更新**：SGD 按梯度微调所有参数。

对应比喻：

> 学生做题（前向）→ 老师批改打分（损失）→ 定位错误步骤（反向）→ 订正（更新参数）。重复 30 轮，错题越来越少。

### 5.3 损失下降的实际输出

```text
第  1 轮，平均损失: 1.9929
第  5 轮，平均损失: 0.0105
第 30 轮，平均损失: 0.0006
```

损失从约 2.0 降到 0.0006，说明模型在练习册上的表现越来越好。

但这里埋着一个疑问，下一节揭晓。

---

## 6. 最后的输出：结业考试

这是用户最容易困惑的部分。三行输出：

```text
提示词: [0, 1, 2]
生成结果: [0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2]
期望模式: [0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2]
```

### 6.1 为什么损失够了还要考试？

回到学生比喻：

> 损失下降只说明**练习册上的错题越来越少**。但有个疑点：学生可能是把这 16 道题的答案**全背下来了**，并不是真懂"数到 7 回到 0"的规律。光看作业成绩，分不清他是真懂还是死记。

所以需要一场**闭卷考试**：

> 老师不翻练习册，直接给一个开头 "0 1 2"，让学生当场往下接 8 个数——这道题他没练过，背不到答案，只能靠真本事推算。

### 6.2 三行输出的含义

| 输出 | 含义 | 比喻 |
|---|---|---|
| 提示词 `[0,1,2]` | 给模型的开头 | 老师给的开头 |
| 生成结果 | 模型自己续写的序列 | 学生现场写的答案 |
| 期望模式 | 按规律应有的正确答案 | 标准答案 |

两者完全一致 → 模型真的学会了规律，不是背答案。

### 6.3 `generate()` 是怎么生成的

```python
def generate(self, start_ids, max_new_tokens):
    ids = list(start_ids)
    for _ in range(max_new_tokens):
        logits = self(ids[-self.mask.shape[0]:])  # 把当前序列喂给模型
        last = logits.data[-1]                    # 取最后一个位置的预测
        next_id = last.index(max(last))           # 取概率最大的 token
        ids.append(next_id)                       # 接到末尾，继续下一轮
    return ids
```

这是**自回归**生成，一次只预测一个词：

```text
[0,1,2]         → 预测 3
[0,1,2,3]       → 预测 4
[0,1,2,3,4]     → 预测 5
...
[0,1,2,3,4,5,6] → 预测 7
[0,1,2,3,4,5,6,7] → 预测 0（周期回到开头）
```

三条规则保证考试公平：

1. **写一个才能写下一个**（自回归）——对应"一步步推算"；
2. **不许看后面的**（因果掩码）——对应"不许偷看答案"；
3. **不能翻练习册**（模型只靠学到的规律）——对应"闭卷"。

### 6.4 一句话总结这段输出

> **损失是"平时作业分"，生成测试是"闭卷现场考"。只有现场把没见过的开头接对了，才能确认模型真的学会了，而不是死记硬背。**

---

## 7. 完整流程总表

| 步骤 | 代码 | 作用 |
|---|---|---|
| 0 | `Tensor` + autograd | 让模型能自动求导、更新参数 |
| 1 | `LayerNorm` | 稳定数值，配合残差 |
| 2 | `causal_mask` + 注意力 | 让每个词看前文，不偷看后文 |
| 3 | `MultiHeadAttention` | 多头并行，拼接融合 |
| 4 | `FeedForward` | 逐位置深度加工 |
| 5 | `TransformerBlock` | Pre-LN 残差，堆出深度 |
| 6 | `positional_encoding` | 注入顺序信息 |
| 7 | `SimpleTransformer` | 组装成完整模型 |
| 8 | `train` + `generate` | 训练（做题订正）+ 考试（现场生成） |

---

# 深入专题

## 专题一：什么是"自回归"？

### 1. 定义

自回归（autoregressive）= **用自己的输出作为下一步的输入**。

```text
输入 [0,1,2] → 输出 3 → 新输入 [0,1,2,3] → 输出 4 → ...
```

像接龙：每接一个词，整句话就变长一点，下一次基于更长的句子继续接。

### 2. 为什么必须一个一个来？

因为要预测第 `i` 个词，需要知道前面所有词。而第 `i+1` 个词的预测又依赖第 `i` 个词。所以只能串行生成。

（训练时可以并行：因为知道完整答案，能一次性算所有位置的损失。）

### 3. 比喻

> 像学生做数列题：写出第 3 个数，才能推第 4 个；不能跳过直接写第 8 个。

---

## 专题二：因果掩码到底在防什么？

### 1. 不用掩码会怎样？

注意力默认让每个位置看到所有位置。预测第 3 个词时，如果它能看到第 4、5、6 个词，那就是**偷看答案**：

```text
输入: 0 1 2 ? 4 5 6 7
            ↑ 预测这个，却能看到后面的 4,5,6,7
```

这样训练时损失会很低（因为答案就在眼前），但考试时没有后面的词，模型就傻了。

### 2. 掩码怎么做？

上三角设为 -1e9：

```text
位置 i 能看到的位置 j：
j ≤ i → 0（允许）
j > i → -1e9（禁止）
```

Softmax 里 `exp(-1e9) ≈ 0`，未来位置的权重变成 0，模型看不见它们。

### 3. 比喻

> 老师把练习册后半部分折起来，学生只能看到题目开头，逼着他真的学会推算。

---

## 专题三：为什么用 Pre-LN？

```python
x = x + self.attn(self.attn_norm(x), mask)
```

先归一化再进子层，残差相加时不再归一化。好处：

- **梯度直通**：残差路径上没有归一化，梯度能从深层直接传回浅层；
- **训练稳定**：不需要小心调学习率和 warmup；
- **大模型默认**：GPT-2、LLaMA 等都用它。

比喻：

> 相当于给每一步加工前先"整理桌面"（归一化），但保留原始草稿（残差）不受干扰，避免越改越乱。

---

## 专题四：这个模型离真实 Transformer 还差什么？

| 缺失的部分 | 影响 |
|---|---|
| 真正的分词器（BPE 等） | 用 one-hot 代替，只能处理固定词表 |
| 可学习的 embedding | 用 one-hot + 线性层代替 |
| Dropout | 没有正则化 |
| 更大规模数据与参数 | 只在玩具数据上验证 |
| 位置编码用 RoPE 等现代方案 | 用的是基础正弦编码 |

但**核心机制都在**：自注意力、多头、因果掩码、FFN、残差、LayerNorm、位置编码、训练与生成。这也是它作为教学示例的价值。

---

## 附：容易忽略的细节

### 1. 为什么 `Tensor.T()` 改成了 `transposed()`？

Python 方法名规范要求 snake_case，`T` 不符合，所以重命名为 `transposed()`（Pylint 要求）。

### 2. 为什么有 `unbroadcast()`？

偏置 `b` 形状是 `[1, d]`，加法时会广播到 `[batch, d]`。反向传播时梯度也要"反广播"回 `[1, d]`（对被广播的维度求和），否则形状对不上。

### 3. 为什么 `generate` 里用 `last.index(max(last))`？

取概率最大的 token。原来用 `max(..., key=lambda...)` 会触发 Pylint 的循环变量告警，改用 `index(max())` 更简洁。

### 4. 为什么模型规模这么小？

`d_model=16, 2 头, 2 层` 是为了纯 Python 能快速跑完。真实模型（如 LLaMA-7B）是 `d_model=4096, 32 头, 32 层`，但结构原理相同。

### 5. 为什么 `prompt = [8, 9, 10]` 会报错？

模型配置 `vocab_size = 8`，合法的 token id 只有 **0 到 7**。`[8, 9, 10]` 超出了词表范围，在 `one_hot()` 这行越界：

```python
data[i][token_id] = 1.0   # token_id=8 时，长度为 8 的行没有索引 8
```

报错信息是 `IndexError: list assignment index out of range`，调用链是：

```text
generate([8,9,10]) → self(ids) → one_hot(token_ids, 8) → data[i][8] 💥 越界
```

**比喻**：模型手里只有开篇说的那 **8 张数字卡片（0~7）**。处理输入时，它要"抽出对应编号的卡片"变成 one-hot。现在你递给它写着 8、9、10 的纸条——它翻遍手里的卡片也找不到这几张，自然没法处理，于是报错。

> 这跟学生聪不聪明没关系，纯粹是"手里的卡片里没有这个数字"。想处理 8、9、10，就得先多做几张卡片（扩大 `vocab_size`）并重新训练。

**解决方式**：本例采用方式一——使用合法范围内的 prompt，比如代码里的 `prompt = [0, 1, 2]`。若确实需要更大的 id（如 10），得把 `vocab_size` 改成大于 10 并重新训练（数据周期和词表都会变）。

（另一种做法是在 `generate()` 入口加参数校验，抛更友好的 `ValueError`。本例为了保持代码简洁，未加该校验。）

---

一句话总结全文：

> **这段代码从零搭出一个能训练的极简 Transformer：前 7 步造模型（注意力、多头、FFN、归一化、位置编码），第 8 步用"做题—批改—订正"的方式训练，最后用"闭卷现场考"验证模型是真学会了规律，而不是背下了答案。**
