"""Transformer 前馈网络（FFN）的两种实现：ReLU 版与 SwiGLU 版。

ReLU 版是《Attention Is All You Need》的经典结构：两层线性变换，中间
接 ReLU 激活，即 FFN(x) = ReLU(x·W1 + b1)·W2 + b2。
SwiGLU 版是现代大模型的常见结构：门控投影经 Swish 激活后与上投影逐元素
相乘，再经下投影，即 (Swish(x·W_gate) ⊙ (x·W_up))·W_down。
仅依赖标准库实现，并对同一输入对比两种结构的输出。
"""

import math
import random

Matrix = list[list[float]]


def matrix_multiply(a: Matrix, b: Matrix) -> Matrix:
    """矩阵乘法：a 是 m×n，b 是 n×p，输出 m×p。

    Args:
        a: 左矩阵，形状为 m×n。
        b: 右矩阵，形状为 n×p，行数必须等于 a 的列数。

    Returns:
        乘积矩阵，形状为 m×p。

    Example:
        >>> matrix_multiply([[1.0, 2.0], [3.0, 4.0]], [[5.0, 6.0], [7.0, 8.0]])
        [[19.0, 22.0], [43.0, 50.0]]
    """
    m = len(a)
    n: int = len(b)
    p = len(b[0])
    result: Matrix = [[0.0 for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                result[i][j] += a[i][k] * b[k][j]
    return result


def matrix_add(a: Matrix, b: Matrix) -> Matrix:
    """矩阵逐元素相加，b 为单行矩阵时按行广播。

    Args:
        a: 被加矩阵，形状为 m×n。
        b: 加数矩阵，形状为 m×n 或 1×n（单行时广播到每一行）。

    Returns:
        相加后的矩阵，形状与 a 相同。

    Example:
        >>> matrix_add([[1.0, 2.0], [3.0, 4.0]], [[0.5, 0.5]])
        [[1.5, 2.5], [3.5, 4.5]]
    """
    rows_b = b * len(a) if len(b) == 1 and len(a) > 1 else b
    return [
        [left + right for left, right in zip(row_a, row_b)]
        for row_a, row_b in zip(a, rows_b)
    ]


def relu(x: list[float]) -> list[float]:
    """ReLU 激活：把负数截断为 0，正数保持不变。

    Args:
        x: 待激活的数值列表。

    Returns:
        与 x 等长的列表，每个元素为 max(0, value)。

    Example:
        >>> relu([-1.0, 0.0, 2.0])
        [0.0, 0.0, 2.0]
    """
    return [max(0.0, value) for value in x]


def swish(x: list[float]) -> list[float]:
    """Swish 激活：x · sigmoid(x)，平滑且允许负数有小幅输出。

    Args:
        x: 待激活的数值列表。

    Returns:
        与 x 等长的列表，每个元素为 value / (1 + exp(-value))。

    Example:
        >>> swish([0.0])
        [0.0]
        >>> round(swish([1.0])[0], 4)
        0.7311
    """
    return [value / (1.0 + math.exp(-value)) for value in x]


class FeedForwardReLU:
    """经典 FFN：两层线性变换，中间以 ReLU 激活。"""

    def __init__(self, d_model: int, d_ff: int) -> None:
        """初始化两层权重与偏置。

        Args:
            d_model: 输入与输出的维度。
            d_ff: 中间隐藏层的维度，通常取 4 倍 d_model。
        """
        rng = random.Random(42)

        def random_matrix(rows: int, cols: int) -> Matrix:
            return [[rng.uniform(-0.1, 0.1) for _ in range(cols)]
                    for _ in range(rows)]

        self.d_model: int = d_model
        self.d_ff: int = d_ff
        self.w1: Matrix = random_matrix(d_model, d_ff)
        self.b1: Matrix = [[0.0 for _ in range(d_ff)]]
        self.w2: Matrix = random_matrix(d_ff, d_model)
        self.b2: Matrix = [[0.0 for _ in range(d_model)]]

    def hidden(self, x: Matrix) -> Matrix:
        """计算第一层线性变换并施加 ReLU 激活。

        Args:
            x: 输入序列，形状为 [seq_len, d_model]。

        Returns:
            隐藏层输出，形状为 [seq_len, d_ff]。
        """
        linear = matrix_add(matrix_multiply(x, self.w1), self.b1)
        return [relu(row) for row in linear]

    def forward(self, x: Matrix) -> Matrix:
        """执行 ReLU 版 FFN 的完整前向传播。

        Args:
            x: 输入序列，形状为 [seq_len, d_model]。

        Returns:
            输出序列，形状为 [seq_len, d_model]。
        """
        hidden = self.hidden(x)
        return matrix_add(matrix_multiply(hidden, self.w2), self.b2)


class FeedForwardSwiGLU:
    """SwiGLU FFN：门控投影与上投影逐元素相乘后，经下投影输出。"""

    def __init__(self, d_model: int, d_ff: int) -> None:
        """初始化门控、上投影与下投影的权重和偏置。

        Args:
            d_model: 输入与输出的维度。
            d_ff: 中间隐藏层的维度。
        """
        rng = random.Random(42)

        def random_matrix(rows: int, cols: int) -> Matrix:
            return [[rng.uniform(-0.1, 0.1) for _ in range(cols)]
                    for _ in range(rows)]

        self.d_model: int = d_model
        self.d_ff: int = d_ff
        self.gate_up: list[Matrix] = [
            random_matrix(d_model, d_ff),
            random_matrix(d_model, d_ff),
        ]
        self.gate_up_bias: list[Matrix] = [
            [[0.0 for _ in range(d_ff)]],
            [[0.0 for _ in range(d_ff)]],
        ]
        self.w_down: Matrix = random_matrix(d_ff, d_model)
        self.b_down: Matrix = [[0.0 for _ in range(d_model)]]

    def gate_and_up(self, x: Matrix) -> tuple[Matrix, Matrix]:
        """计算门控投影与上投影。

        Args:
            x: 输入序列，形状为 [seq_len, d_model]。

        Returns:
            (gate, up) 两个矩阵，形状均为 [seq_len, d_ff]。
        """
        gate = matrix_add(matrix_multiply(x, self.gate_up[0]), self.gate_up_bias[0])
        up = matrix_add(matrix_multiply(x, self.gate_up[1]), self.gate_up_bias[1])
        return gate, up

    def forward(self, x: Matrix) -> Matrix:
        """执行 SwiGLU 版 FFN 的完整前向传播。

        Args:
            x: 输入序列，形状为 [seq_len, d_model]。

        Returns:
            输出序列，形状为 [seq_len, d_model]。
        """
        gate, up = self.gate_and_up(x)
        gated: Matrix = [
            [swish_gate * up_value for swish_gate, up_value
             in zip(swish(gate_row), up_row)]
            for gate_row, up_row in zip(gate, up)
        ]
        return matrix_add(matrix_multiply(gated, self.w_down), self.b_down)


def main() -> None:
    """运行对比演示：对同一输入分别计算 ReLU 版与 SwiGLU 版的输出。"""
    d_model = 4
    d_ff = 8

    x_input: Matrix = [
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
    ]

    print("=" * 50)
    print("Feed-Forward Network Demo")
    print("=" * 50)
    print(f"输入维度: {d_model}，隐藏层维度: {d_ff}，序列长度: {len(x_input)}")
    print()

    relu_ffn = FeedForwardReLU(d_model=d_model, d_ff=d_ff)
    relu_output = relu_ffn.forward(x_input)
    print("ReLU 版输出:")
    for word_index, row in enumerate(relu_output):
        print(f"  词 {word_index}: {[f'{val:.4f}' for val in row]}")

    swiglu_ffn = FeedForwardSwiGLU(d_model=d_model, d_ff=d_ff)
    swiglu_output = swiglu_ffn.forward(x_input)
    print()
    print("SwiGLU 版输出:")
    for word_index, row in enumerate(swiglu_output):
        print(f"  词 {word_index}: {[f'{val:.4f}' for val in row]}")


if __name__ == "__main__":
    main()
