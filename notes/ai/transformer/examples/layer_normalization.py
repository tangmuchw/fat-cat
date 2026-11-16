"""层归一化（Layer Normalization）实现演示。

与 Batch Normalization 不同，LayerNorm 在每个样本内部、沿特征维度计算
均值和方差，对每个样本独立归一化，不依赖 batch 里的其他样本。
Transformer 里广泛使用，配合残差连接稳定训练。
仅依赖标准库实现，并演示归一化前后统计量的变化及 gamma/beta 的作用。
"""

import math

Matrix = list[list[float]]


def mean(values: list[float]) -> float:
    """计算一组数值的均值。

    Args:
        values: 数值列表，不能为空。

    Returns:
        所有数值的算术平均数。

    Example:
        >>> mean([1.0, 2.0, 3.0])
        2.0
    """
    return sum(values) / len(values)


def variance(values: list[float]) -> float:
    """计算一组数值的总体方差（除以 n）。

    Args:
        values: 数值列表，不能为空。

    Returns:
        各数值与均值之差的平方的平均数。

    Example:
        >>> round(variance([1.0, 2.0, 3.0]), 4)
        0.6667
    """
    avg = mean(values)
    return sum((value - avg) ** 2 for value in values) / len(values)


def normalize_row(values: list[float], eps: float) -> list[float]:
    """把一行数值标准化为均值约 0、方差约 1 的分布。

    Args:
        values: 待标准化的一行数值。
        eps: 加在方差上的小常数，防止除以 0。

    Returns:
        标准化后的数值列表，长度与 values 相同。

    Example:
        >>> [round(value, 4) for value in normalize_row([1.0, 2.0, 3.0], 1e-5)]
        [-1.2247, 0.0, 1.2247]
    """
    avg = mean(values)
    standard_deviation = math.sqrt(variance(values) + eps)
    return [(value - avg) / standard_deviation for value in values]


class LayerNormalization:
    """层归一化模块：逐行标准化后，用可学习的 gamma 和 beta 缩放平移。"""

    def __init__(self, d_model: int, eps: float = 1e-5) -> None:
        """初始化缩放与平移参数。

        Args:
            d_model: 特征维度，即每行向量的长度。
            eps: 防止除零的小常数，默认 1e-5。
        """
        self.d_model: int = d_model
        self.eps: float = eps
        self.gamma: list[float] = [1.0 for _ in range(d_model)]
        self.beta: list[float] = [0.0 for _ in range(d_model)]

    def normalize(self, x: Matrix) -> Matrix:
        """对每一行独立标准化，不涉及 gamma/beta。

        Args:
            x: 输入矩阵，形状为 [batch, d_model]。

        Returns:
            标准化后的矩阵，形状与 x 相同，每行均值约 0、方差约 1。
        """
        return [normalize_row(row, self.eps) for row in x]

    def forward(self, x: Matrix) -> Matrix:
        """执行完整层归一化：标准化后逐元素缩放和平移。

        Args:
            x: 输入矩阵，形状为 [batch, d_model]。

        Returns:
            输出矩阵，形状与 x 相同。
        """
        normalized = self.normalize(x)
        return [
            [
                scale * value + shift
                for scale, shift, value in zip(self.gamma, self.beta, row)
            ]
            for row in normalized
        ]


def matrix_add(a: Matrix, b: Matrix) -> Matrix:
    """两个同形矩阵逐元素相加。

    Example:
        >>> matrix_add([[1.0, 2.0]], [[3.0, 4.0]])
        [[4.0, 6.0]]
    """
    return [
        [left + right for left, right in zip(row_a, row_b)]
        for row_a, row_b in zip(a, b)
    ]


def rms_norm_row(values: list[float], gamma: list[float], eps: float) -> list[float]:
    """RMSNorm：只算均方根，不减均值，即 gamma ⊗ (x / RMS(x))。

    Args:
        values: 待处理的一行数值。
        gamma: 每维的缩放系数。
        eps: 加在均方里防止除零的小常数。

    Returns:
        与 values 等长的列表。

    Example:
        >>> [round(v, 4) for v in rms_norm_row([1.0, 2.0, 3.0], [1.0] * 3, 1e-5)]
        [0.4629, 0.9258, 1.3887]
    """
    rms = math.sqrt(sum(value ** 2 for value in values) / len(values) + eps)
    return [scale * value / rms for scale, value in zip(gamma, values)]


class RMSNormalization:  # pylint: disable=too-few-public-methods
    """RMSNorm 模块：去均值、去平移，只按均方根缩放。

    轻量归一化模块只需 forward 一个公开入口，故禁用
    too-few-public-methods 告警。
    """

    def __init__(self, d_model: int, eps: float = 1e-5) -> None:
        """初始化每维缩放系数 gamma。

        Args:
            d_model: 特征维度，即每行向量的长度。
            eps: 防止除零的小常数，默认 1e-5。
        """
        self.d_model: int = d_model
        self.eps: float = eps
        self.gamma: list[float] = [1.0 for _ in range(d_model)]

    def forward(self, x: Matrix) -> Matrix:
        """对每一行做 RMSNorm，输出形状与 x 相同。"""
        return [rms_norm_row(row, self.gamma, self.eps) for row in x]


def demo_sublayer(x: Matrix) -> Matrix:
    """模拟 Transformer 的子层（注意力/FFN）：放大 1.5 倍再加 0.1。"""
    return [[1.5 * value + 0.1 for value in row] for row in x]


def post_norm_block(x: Matrix, sublayer, norm) -> Matrix:
    """Post-Norm：子层 → 残差 → 归一化（原始 Transformer）。"""
    return norm.forward(matrix_add(x, sublayer(x)))


def pre_norm_block(x: Matrix, sublayer, norm) -> Matrix:
    """Pre-Norm：归一化 → 子层 → 残差（现在主流，训练更稳定）。"""
    return matrix_add(x, sublayer(norm.forward(x)))


def main() -> None:
    """运行层归一化演示：对比统计量、gamma/beta、Pre/Post-Norm 与 RMSNorm。"""
    d_model = 4

    x_input: Matrix = [
        [1.0, 2.0, 3.0, 4.0],
        [100.0, 200.0, 300.0, 400.0],
    ]

    print("=" * 50)
    print("Layer Normalization Demo")
    print("=" * 50)
    print(f"特征维度: {d_model}，样本数: {len(x_input)}")
    print()

    print("原始输入的每行统计量:")
    for row_index, row in enumerate(x_input):
        print(f"  样本 {row_index}: 均值={mean(row):.4f}, 方差={variance(row):.4f}")

    layer_norm = LayerNormalization(d_model)
    normalized = layer_norm.normalize(x_input)

    print()
    print("标准化后（均值≈0，方差≈1）:")
    for row_index, row in enumerate(normalized):
        print(f"  样本 {row_index}: 均值={mean(row):.4f}, 方差={variance(row):.4f}")
        print(f"    数值: {[f'{value:.4f}' for value in row]}")

    output = layer_norm.forward(x_input)

    print()
    print("默认 gamma=1, beta=0 时 forward 输出（应与标准化结果相同）:")
    for row_index, row in enumerate(output):
        print(f"  样本 {row_index}: {[f'{value:.4f}' for value in row]}")

    layer_norm.gamma = [2.0 for _ in range(d_model)]
    layer_norm.beta = [0.5 for _ in range(d_model)]
    scaled = layer_norm.forward(x_input)

    print()
    print("设置 gamma=2, beta=0.5 后的输出（放大 2 倍再上移 0.5）:")
    for row_index, row in enumerate(scaled):
        print(f"  样本 {row_index}: {[f'{value:.4f}' for value in row]}")

    fresh_norm = LayerNormalization(d_model)
    post_output = post_norm_block(x_input, demo_sublayer, fresh_norm)
    pre_output = pre_norm_block(x_input, demo_sublayer, fresh_norm)

    print()
    print("=" * 50)
    print("Pre-Norm vs Post-Norm（同一个子层 + 残差）")
    print("=" * 50)
    print("Post-Norm: 子层 → 残差 → 归一化:")
    for row_index, row in enumerate(post_output):
        print(f"  样本 {row_index}: {[f'{value:.4f}' for value in row]}")
    print("Pre-Norm: 归一化 → 子层 → 残差:")
    for row_index, row in enumerate(pre_output):
        print(f"  样本 {row_index}: {[f'{value:.4f}' for value in row]}")
    print("Pre-Norm 训练更稳定，现在的大模型几乎都用它。")

    rms_norm = RMSNormalization(d_model)
    rms_output = rms_norm.forward(x_input)

    print()
    print("=" * 50)
    print("RMSNorm: gamma ⊗ (x / RMS(x))，不减均值")
    print("=" * 50)
    for row_index, row in enumerate(rms_output):
        print(f"  样本 {row_index}: {[f'{value:.4f}' for value in row]}")


# ============================================================
# 执行 main() 的输入与输出
# ------------------------------------------------------------
# 输入：d_model=4，x_input 为两行尺度差异极大的样本：
#   [[1, 2, 3, 4], [100, 200, 300, 400]]
# 输出（打印）：
#   - 原始统计量：样本 0 均值 2.5 / 方差 1.25，样本 1 均值 250 / 方差 12500；
#   - 标准化后两行都变成 均值≈0、方差≈1，数值均为
#     ['-1.3416', '-0.4472', '0.4472', '1.3416']；
#   - gamma=2, beta=0.5 后：['-2.1833', '-0.3944', '1.3944', '3.1833']；
#   - Post-Norm 输出被压回标准分布 [-1.3416, ...]，Pre-Norm 保留输入尺度；
#     例如样本 1 的 Pre-Norm 输出：['98.0875', '199.4292', '300.7708', '402.1125']；
#   - RMSNorm 输出：['0.3651', '0.7303', '1.0954', '1.4606']（不减均值）。
# ============================================================

if __name__ == "__main__":
    main()
