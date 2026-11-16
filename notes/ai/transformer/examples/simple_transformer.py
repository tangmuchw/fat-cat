"""从零实现简化 Transformer（仅依赖 Python 标准库）。

按 8 个步骤组织，每步都建立在前一步之上：
  1. 层归一化（LayerNorm）
  2. 自注意力（带因果掩码）
  3. 多头注意力
  4. 前馈网络（FFN）
  5. Transformer 层（Pre-LN 残差结构）
  6. 位置编码（正弦）
  7. 组装完整模型
  8. 训练循环（微型 autograd + SGD）

为了让第 8 步能真正训练，文件开头先实现一个极简的矩阵自动微分引擎。
运行脚本会在一个小型序列预测任务上训练，并打印损失下降与生成结果。
"""

import math
import random

Matrix = list[list[float]]


# ============================================================
# 基础矩阵运算（纯 Python）
# ============================================================

def shape(a: Matrix) -> tuple[int, int]:
    """返回二维矩阵的行数和列数。"""
    return len(a), len(a[0]) if a else 0


def zeros(rows: int, cols: int) -> Matrix:
    """创建指定形状的全零矩阵。"""
    return [[0.0 for _ in range(cols)] for _ in range(rows)]


def transpose(a: Matrix) -> Matrix:
    """矩阵转置：行变列、列变行。"""
    return [list(row) for row in zip(*a)]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    """矩阵乘法：a[m,n] 乘 b[n,p] 得到 [m,p]。"""
    ar, ac = shape(a)
    br, bc = shape(b)
    assert ac == br, f"形状不匹配: ({ar}, {ac}) 与 ({br}, {bc})"
    result = zeros(ar, bc)
    for i in range(ar):
        for k in range(ac):
            aik = a[i][k]
            if aik == 0.0:
                continue
            for j in range(bc):
                result[i][j] += aik * b[k][j]
    return result


def elem_add(a: Matrix, b: Matrix) -> Matrix:
    """逐元素相加，支持二维广播（行数为 1、列数为 1 或完全相同）。"""
    ar, ac = shape(a)
    br, bc = shape(b)
    rr, rc = max(ar, br), max(ac, bc)
    result = zeros(rr, rc)
    for i in range(rr):
        for j in range(rc):
            result[i][j] = a[i % ar][j % ac] + b[i % br][j % bc]
    return result


def elem_mul(a: Matrix, b: Matrix) -> Matrix:
    """逐元素相乘，支持二维广播。"""
    ar, ac = shape(a)
    br, bc = shape(b)
    rr, rc = max(ar, br), max(ac, bc)
    result = zeros(rr, rc)
    for i in range(rr):
        for j in range(rc):
            result[i][j] = a[i % ar][j % ac] * b[i % br][j % bc]
    return result


def unbroadcast(grad: Matrix, target: tuple[int, int]) -> Matrix:
    """把广播后的梯度还原到目标形状（对被广播的维度求和）。"""
    gr, gc = shape(grad)
    tr, tc = target
    if tr == 1 and gr > 1:
        grad = [[sum(col) for col in zip(*grad)]]
    if tc == 1 and gc > 1:
        grad = [[sum(row)] for row in grad]
    return grad


# ============================================================
# 微型自动微分引擎：Tensor
# ============================================================

class Tensor:  # pylint: disable=protected-access
    """支持二维矩阵的极简 autograd，用于第 8 步训练。

    反向传播需在计算图节点间访问彼此的 `_backward` 与 `_children`，
    属于 autograd 的内部机制，故本类禁用 protected-access 告警。
    """

    def __init__(self, data, requires_grad: bool = False,
                 children: tuple = (), op: str = "") -> None:
        if not isinstance(data, list):
            data = [[float(data)]]
        elif data and not isinstance(data[0], list):
            data = [[float(v) for v in data]]
        self.data: Matrix = data
        self.shape: tuple[int, int] = shape(data)
        self.requires_grad: bool = requires_grad
        self.grad: Matrix = zeros(*self.shape)
        self._children = children
        self._op = op
        self._backward = lambda: None

    def __add__(self, other) -> "Tensor":
        other = other if isinstance(other, Tensor) else Tensor(other)
        out = Tensor(elem_add(self.data, other.data),
                     self.requires_grad or other.requires_grad, (self, other), "+")

        def _backward():
            if self.requires_grad:
                self.grad = elem_add(self.grad, unbroadcast(out.grad, self.shape))
            if other.requires_grad:
                other.grad = elem_add(other.grad, unbroadcast(out.grad, other.shape))
        out._backward = _backward
        return out

    __radd__ = __add__

    def __neg__(self) -> "Tensor":
        return self * -1.0

    def __sub__(self, other) -> "Tensor":
        return self + (-other if isinstance(other, Tensor) else -Tensor(other))

    def __rsub__(self, other) -> "Tensor":
        return Tensor(other) - self

    def __mul__(self, other) -> "Tensor":
        other = other if isinstance(other, Tensor) else Tensor(other)
        out = Tensor(elem_mul(self.data, other.data),
                     self.requires_grad or other.requires_grad, (self, other), "*")

        def _backward():
            if self.requires_grad:
                delta = elem_mul(out.grad, other.data)
                self.grad = elem_add(self.grad, unbroadcast(delta, self.shape))
            if other.requires_grad:
                delta = elem_mul(out.grad, self.data)
                other.grad = elem_add(other.grad, unbroadcast(delta, other.shape))
        out._backward = _backward
        return out

    __rmul__ = __mul__

    def __truediv__(self, other) -> "Tensor":
        other = other if isinstance(other, Tensor) else Tensor(other)
        return self * (other ** -1.0)

    def __pow__(self, exponent: float) -> "Tensor":
        data = [[v ** exponent for v in row] for row in self.data]
        out = Tensor(data, self.requires_grad, (self,), "**")

        def _backward():
            if self.requires_grad:
                delta = [
                    [exponent * (v ** (exponent - 1.0)) * g for v, g in zip(row, grow)]
                    for row, grow in zip(self.data, out.grad)
                ]
                self.grad = elem_add(self.grad, delta)
        out._backward = _backward
        return out

    def __matmul__(self, other: "Tensor") -> "Tensor":
        out = Tensor(matmul(self.data, other.data),
                     self.requires_grad or other.requires_grad, (self, other), "@")

        def _backward():
            if self.requires_grad:
                self.grad = elem_add(self.grad, matmul(out.grad, transpose(other.data)))
            if other.requires_grad:
                other.grad = elem_add(other.grad, matmul(transpose(self.data), out.grad))
        out._backward = _backward
        return out

    def transposed(self) -> "Tensor":
        """返回转置后的新 Tensor，梯度会转置回原形状。"""
        out = Tensor(transpose(self.data), self.requires_grad, (self,), "T")

        def _backward():
            if self.requires_grad:
                self.grad = elem_add(self.grad, transpose(out.grad))
        out._backward = _backward
        return out

    def relu(self) -> "Tensor":
        """逐元素 ReLU 激活：负数归零，正数保持不变。"""
        out = Tensor([[max(0.0, v) for v in row] for row in self.data],
                     self.requires_grad, (self,), "relu")

        def _backward():
            if self.requires_grad:
                delta = [[g if v > 0 else 0.0 for v, g in zip(row, grow)]
                         for row, grow in zip(self.data, out.grad)]
                self.grad = elem_add(self.grad, delta)
        out._backward = _backward
        return out

    def softmax(self) -> "Tensor":
        """逐行 Softmax（减去最大值防溢出）。"""
        data = []
        for row in self.data:
            max_val = max(row)
            exps = [math.exp(v - max_val) for v in row]
            total = sum(exps)
            data.append([v / total for v in exps])
        out = Tensor(data, self.requires_grad, (self,), "softmax")

        def _backward():
            if self.requires_grad:
                delta = []
                for y, g in zip(out.data, out.grad):
                    dot = sum(yi * gi for yi, gi in zip(y, g))
                    delta.append([yi * (gi - dot) for yi, gi in zip(y, g)])
                self.grad = elem_add(self.grad, delta)
        out._backward = _backward
        return out

    def mean(self, axis: int = 1) -> "Tensor":
        """axis=1 按行求均值，得到 [m, 1]；axis=0 按列求均值。"""
        rows, cols = self.shape
        if axis == 1:
            data = [[sum(row) / cols] for row in self.data]
        else:
            data = [[sum(col) / rows for col in zip(*self.data)]]
        out = Tensor(data, self.requires_grad, (self,), "mean")

        def _backward():
            if not self.requires_grad:
                return
            if axis == 1:
                delta = [[g[0] / cols for _ in range(cols)] for g in out.grad]
            else:
                delta = [[g[j] / rows for j in range(cols)] for _ in range(rows)
                         for g in out.grad]
                delta = delta[:rows]
            self.grad = elem_add(self.grad, delta)
        out._backward = _backward
        return out

    def slice_cols(self, start: int, end: int) -> "Tensor":
        """沿列切片，梯度写回对应列（多头拆分用）。"""
        data = [row[start:end] for row in self.data]
        out = Tensor(data, self.requires_grad, (self,), "slice")

        def _backward():
            if self.requires_grad:
                delta = zeros(*self.shape)
                for i in range(self.shape[0]):
                    for j in range(start, end):
                        delta[i][j] = out.grad[i][j - start]
                self.grad = elem_add(self.grad, delta)
        out._backward = _backward
        return out

    def backward(self) -> None:
        """反向传播：拓扑排序后逆序调用各节点的 _backward。"""
        topo: list[Tensor] = []
        visited: set[int] = set()

        def build(node: Tensor) -> None:
            if id(node) in visited:
                return
            visited.add(id(node))
            for child in node._children:
                build(child)
            topo.append(node)

        build(self)
        self.grad = [[1.0 for _ in range(self.shape[1])]
                     for _ in range(self.shape[0])]
        for node in reversed(topo):
            node._backward()


def cat_columns(tensors: list[Tensor]) -> Tensor:
    """沿列拼接多个 Tensor（多头合并用）。"""
    rows = tensors[0].shape[0]
    data = []
    for i in range(rows):
        row: list[float] = []
        for tensor in tensors:
            row.extend(tensor.data[i])
        data.append(row)
    requires = any(t.requires_grad for t in tensors)
    out = Tensor(data, requires, tuple(tensors), "cat")
    offsets: list[int] = []
    cursor = 0
    for tensor in tensors:
        offsets.append(cursor)
        cursor += tensor.shape[1]

    def _backward():
        for tensor, offset in zip(tensors, offsets):
            if tensor.requires_grad:
                delta = [row[offset:offset + tensor.shape[1]] for row in out.grad]
                tensor.grad = elem_add(tensor.grad, delta)
    out._backward = _backward  # pylint: disable=protected-access
    return out


class Module:  # pylint: disable=too-few-public-methods
    """所有模块的基类，用于递归收集可训练参数。

    作为轻量基类只需提供 parameters 一个公开方法，故禁用
    too-few-public-methods 告警。
    """

    def parameters(self) -> list[Tensor]:
        """递归收集自身及子模块中所有 requires_grad 的 Tensor。"""
        params: list[Tensor] = []
        for value in vars(self).values():
            if isinstance(value, Tensor) and value.requires_grad:
                params.append(value)
            elif isinstance(value, Module):
                params.extend(value.parameters())
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, Module):
                        params.extend(item.parameters())
        return params


def rand_matrix(rows: int, cols: int, rng: random.Random, scale: float = 0.1) -> Matrix:
    """用给定随机源生成指定形状的均匀随机矩阵（-scale 到 scale）。"""
    return [[rng.uniform(-scale, scale) for _ in range(cols)] for _ in range(rows)]


class Linear(Module):
    """线性层：y = x @ W + b。"""

    def __init__(self, in_features: int, out_features: int,
                 rng: random.Random) -> None:
        self.weight = Tensor(rand_matrix(in_features, out_features, rng),
                             requires_grad=True)
        self.bias = Tensor(zeros(1, out_features), requires_grad=True)

    def __call__(self, x: Tensor) -> Tensor:
        return x @ self.weight + self.bias


# ============================================================
# 步骤 1：层归一化
# ============================================================

class LayerNorm(Module):
    """对每个样本（行）独立归一化，再用 gamma/beta 缩放平移。"""

    def __init__(self, d_model: int) -> None:
        self.gamma = Tensor([[1.0 for _ in range(d_model)]], requires_grad=True)
        self.beta = Tensor([[0.0 for _ in range(d_model)]], requires_grad=True)
        self.eps = Tensor(1e-5)

    def __call__(self, x: Tensor) -> Tensor:
        avg = x.mean(axis=1)
        centered = x - avg
        var = (centered * centered).mean(axis=1)
        std = (var + self.eps) ** 0.5
        return centered / std * self.gamma + self.beta


# ============================================================
# 步骤 2：自注意力（带因果掩码）
# ============================================================

def causal_mask(seq_len: int) -> Tensor:
    """上三角（未来位置）设为 -1e9，Softmax 后近似为 0。"""
    data = [[-1e9 if j > i else 0.0 for j in range(seq_len)]
            for i in range(seq_len)]
    return Tensor(data)


def scaled_dot_product_attention(q: Tensor, k: Tensor, v: Tensor,
                                 mask: Tensor | None = None) -> Tensor:
    """缩放点积注意力：Softmax(QKᵀ/√d_k) · V。"""
    d_k = q.shape[1]
    scores = (q @ k.transposed()) * (1.0 / math.sqrt(d_k))
    if mask is not None:
        scores = scores + mask
    weights = scores.softmax()
    return weights @ v


# ============================================================
# 步骤 3：多头注意力
# ============================================================

class MultiHeadAttention(Module):
    """多个头并行做注意力，拼接后用 Wo 融合。"""

    def __init__(self, d_model: int, num_heads: int,
                 rng: random.Random) -> None:
        assert d_model % num_heads == 0
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        self.wq = Linear(d_model, d_model, rng)
        self.wk = Linear(d_model, d_model, rng)
        self.wv = Linear(d_model, d_model, rng)
        self.wo = Linear(d_model, d_model, rng)

    def __call__(self, x: Tensor, mask: Tensor | None = None) -> Tensor:
        q, k, v = self.wq(x), self.wk(x), self.wv(x)
        heads: list[Tensor] = []
        for head in range(self.num_heads):
            start = head * self.d_k
            end = start + self.d_k
            q_h = q.slice_cols(start, end)
            k_h = k.slice_cols(start, end)
            v_h = v.slice_cols(start, end)
            heads.append(scaled_dot_product_attention(q_h, k_h, v_h, mask))
        return self.wo(cat_columns(heads))


# ============================================================
# 步骤 4：前馈网络（FFN）
# ============================================================

class FeedForward(Module):
    """两层线性变换，中间 ReLU 激活。"""

    def __init__(self, d_model: int, d_ff: int, rng: random.Random) -> None:
        self.w1 = Linear(d_model, d_ff, rng)
        self.w2 = Linear(d_ff, d_model, rng)

    def __call__(self, x: Tensor) -> Tensor:
        return self.w2(self.w1(x).relu())


# ============================================================
# 步骤 5：Transformer 层（Pre-LN）
# ============================================================

class TransformerBlock(Module):
    """Pre-LN 结构：先归一化再进子层，残差路径保持畅通。"""

    def __init__(self, d_model: int, num_heads: int, d_ff: int,
                 rng: random.Random) -> None:
        self.attn_norm = LayerNorm(d_model)
        self.attn = MultiHeadAttention(d_model, num_heads, rng)
        self.ffn_norm = LayerNorm(d_model)
        self.ffn = FeedForward(d_model, d_ff, rng)

    def __call__(self, x: Tensor, mask: Tensor | None = None) -> Tensor:
        x = x + self.attn(self.attn_norm(x), mask)
        x = x + self.ffn(self.ffn_norm(x))
        return x


# ============================================================
# 步骤 6：位置编码
# ============================================================

def positional_encoding(seq_len: int, d_model: int) -> Tensor:
    """正弦位置编码，无训练参数。"""
    data: Matrix = []
    for pos in range(seq_len):
        row: list[float] = []
        for dim in range(d_model):
            rate = 1.0 / (10000 ** (2 * (dim // 2) / d_model))
            row.append(math.sin(pos * rate) if dim % 2 == 0
                       else math.cos(pos * rate))
        data.append(row)
    return Tensor(data)


# ============================================================
# 步骤 7：组装完整模型
# ============================================================

def one_hot(ids: list[int], vocab_size: int) -> Tensor:
    """把 token id 列表转成形状 [len(ids), vocab_size] 的 one-hot 矩阵。"""
    data = zeros(len(ids), vocab_size)
    for i, token_id in enumerate(ids):
        data[i][token_id] = 1.0
    return Tensor(data)


class SimpleTransformer(Module):
    """极简 decoder-only Transformer，用于 next-token 预测。"""

    # 模型配置需要 7 个入参，属合理的构造参数集合
    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(self, vocab_size: int, d_model: int, num_heads: int,
                 num_layers: int, d_ff: int, max_seq_len: int,
                 rng: random.Random) -> None:
        """按超参数组装 embedding、位置编码、若干 Transformer 层与输出头。"""
        self.d_model = d_model
        self.embed = Linear(vocab_size, d_model, rng)
        self.pos = positional_encoding(max_seq_len, d_model)
        self.blocks = [
            TransformerBlock(d_model, num_heads, d_ff, rng)
            for _ in range(num_layers)
        ]
        self.final_norm = LayerNorm(d_model)
        self.head = Linear(d_model, vocab_size, rng)
        self.mask = causal_mask(max_seq_len)

    def __call__(self, token_ids: list[int]) -> Tensor:
        seq_len = len(token_ids)
        x = self.embed(one_hot(token_ids, self.embed.weight.shape[0]))
        x = x + Tensor([row[:] for row in self.pos.data[:seq_len]])
        mask = Tensor([row[:seq_len] for row in self.mask.data[:seq_len]])
        for block in self.blocks:
            x = block(x, mask)
        return self.head(self.final_norm(x))

    def generate(self, start_ids: list[int], max_new_tokens: int) -> list[int]:
        """自回归生成：每次取最后一个 token 的 logits 预测下一个。"""
        ids = list(start_ids)
        for _ in range(max_new_tokens):
            logits = self(ids[-self.mask.shape[0]:])
            last = logits.data[-1]
            next_id = last.index(max(last))
            ids.append(next_id)
        return ids


# ============================================================
# 步骤 8：训练循环
# ============================================================

def cross_entropy(logits: Tensor, targets: list[int]) -> Tensor:
    """交叉熵损失，内部构造带梯度的 loss 节点。"""
    probs = logits.softmax()
    n = len(targets)
    loss_value = -sum(math.log(probs.data[i][t] + 1e-12)
                      for i, t in enumerate(targets)) / n
    loss = Tensor(loss_value, requires_grad=logits.requires_grad,
                  children=(logits,), op="cross_entropy")

    def _backward() -> None:
        if logits.requires_grad:
            delta = [row[:] for row in probs.data]
            for i, t in enumerate(targets):
                delta[i][t] -= 1.0
            delta = [[v / n for v in row] for row in delta]
            logits.grad = elem_add(logits.grad, delta)
    loss._backward = _backward  # pylint: disable=protected-access
    return loss


class SGD:
    """最简随机梯度下降优化器。"""

    def __init__(self, params: list[Tensor], lr: float) -> None:
        self.params = params
        self.lr = lr

    def zero_grad(self) -> None:
        """把所有参数的梯度清零。"""
        for param in self.params:
            param.grad = zeros(*param.shape)

    def step(self) -> None:
        """按 SGD 规则用当前梯度更新所有参数。"""
        for param in self.params:
            param.data = [
                [v - self.lr * g for v, g in zip(row, grow)]
                for row, grow in zip(param.data, param.grad)
            ]


def build_dataset(vocab_size: int, seq_len: int) -> list[tuple[list[int], list[int]]]:
    """构造周期性序列数据，任务是预测下一个 token。"""
    tokens = list(range(vocab_size)) * 3
    samples = []
    for start in range(len(tokens) - seq_len):
        x = tokens[start:start + seq_len]
        y = tokens[start + 1:start + seq_len + 1]
        samples.append((x, y))
    return samples


def train() -> None:  # pylint: disable=too-many-locals
    """完整训练流程：前向 → 损失 → 反向 → 更新。

    用局部变量集中展示超参数，便于教学阅读，故禁用 too-many-locals 告警。
    """
    rng = random.Random(42)
    vocab_size = 8
    d_model = 16
    num_heads = 2
    num_layers = 2
    d_ff = 32
    seq_len = 8
    max_seq_len = 16
    epochs = 30
    lr = 0.5

    model = SimpleTransformer(vocab_size, d_model, num_heads,
                              num_layers, d_ff, max_seq_len, rng)
    optimizer = SGD(model.parameters(), lr)
    samples = build_dataset(vocab_size, seq_len)

    print("=" * 50)
    print("简化 Transformer 训练演示")
    print("=" * 50)
    print(f"词表大小={vocab_size}, d_model={d_model}, 头数={num_heads}, "
          f"层数={num_layers}, 序列长度={seq_len}")
    print(f"样本数={len(samples)}, 训练轮数={epochs}, 学习率={lr}")
    print()

    for epoch in range(epochs):
        total_loss = 0.0
        for x_ids, y_ids in samples:
            optimizer.zero_grad()
            logits = model(x_ids)
            loss = cross_entropy(logits, y_ids)
            loss.backward()
            optimizer.step()
            total_loss += loss.data[0][0]
        avg_loss = total_loss / len(samples)
        if epoch == 0 or (epoch + 1) % 5 == 0:
            print(f"第 {epoch + 1:2d} 轮，平均损失: {avg_loss:.4f}")

    print()
    print("=" * 50)
    print("生成测试")
    print("=" * 50)
    prompt = [0, 1, 2]
    generated = model.generate(prompt, max_new_tokens=8)
    print(f"提示词: {prompt}")
    print(f"生成结果: {generated}")
    print(f"期望模式: {[i % vocab_size for i in range(len(generated))]}")


# ============================================================
# 执行 train() 的输入与输出
# ------------------------------------------------------------
# 输入：词表大小=8、d_model=16、头数=2、层数=2、d_ff=32、序列长度=8；
#   训练集为周期性序列（模式 0,1,2,...,7,0,1,...）的 16 个滑动窗口样本，
#   任务是给定 8 个 token 预测后 8 个 token；训练 30 轮，学习率 0.5。
# 输出（打印）：
#   - 每轮平均损失，例如第 1 轮 1.9929 → 第 30 轮 0.0006（损失持续下降）；
#   - 生成测试：提示词 [0, 1, 2]，生成结果
#     [0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2]，
#     与期望模式 [0,1,2,3,4,5,6,7,0,1,2] 完全一致。
# ============================================================

if __name__ == "__main__":
    train()
