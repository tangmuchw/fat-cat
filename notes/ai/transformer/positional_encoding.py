"""正弦位置编码（Sinusoidal Positional Encoding）实现演示。

出自《Attention Is All You Need》：用不同频率的正弦/余弦函数为序列中每个
位置生成唯一的向量，偶数维度取 sin、奇数维度取 cos，再逐元素加到词向量上，
从而为不含循环与卷积结构的 Transformer 注入顺序信息。
仅依赖标准库实现，并演示位置编码本身及叠加后的结果。
"""

import math

Matrix = list[list[float]]


def position_angle_rates(d_model: int) -> list[float]:
    """计算各维度的角速率 1 / 10000^(2i/d_model)。

    Args:
        d_model: 位置编码的维度，须为正偶数。

    Returns:
        长度为 d_model 的角速率列表，每两个相邻维度共享同一速率。

    Example:
        >>> position_angle_rates(4)
        [1.0, 1.0, 0.01, 0.01]
    """
    return [
        math.pow(10000.0, -2 * (index // 2) / d_model)
        for index in range(d_model)
    ]


class PositionalEncoding:
    """正弦位置编码器：生成位置向量并叠加到词向量上。"""

    def __init__(self, d_model: int) -> None:
        """初始化位置编码器。

        Args:
            d_model: 位置编码与词向量的维度，须为正偶数。
        """
        self.d_model: int = d_model
        self.rates: list[float] = position_angle_rates(d_model)

    def encode(self, seq_len: int) -> Matrix:
        """生成 seq_len 个位置的编码向量。

        Args:
            seq_len: 序列长度（即需要编码的位置数量）。

        Returns:
            形状为 [seq_len, d_model] 的位置编码矩阵，偶数维度取 sin，
            奇数维度取 cos。

        Example:
            >>> PositionalEncoding(4).encode(1)
            [[0.0, 1.0, 0.0, 1.0]]
        """
        return [
            [
                math.sin(position * rate) if dimension % 2 == 0
                else math.cos(position * rate)
                for dimension, rate in enumerate(self.rates)
            ]
            for position in range(seq_len)
        ]

    def add_to(self, x: Matrix) -> Matrix:
        """把位置编码逐元素加到输入序列上。

        Args:
            x: 词向量序列，形状为 [seq_len, d_model]。

        Returns:
            叠加位置信息后的序列，形状与 x 相同。

        Example:
            >>> PositionalEncoding(4).add_to([[1.0, 2.0, 3.0, 4.0]])
            [[1.0, 3.0, 3.0, 5.0]]
        """
        encoding = self.encode(len(x))
        return [
            [value + offset for value, offset in zip(row, encoding_row)]
            for row, encoding_row in zip(x, encoding)
        ]


def main() -> None:
    """运行正弦位置编码演示：打印各位置的编码向量及叠加后的结果。"""
    d_model = 8
    seq_len = 4

    encoder = PositionalEncoding(d_model)
    encoding = encoder.encode(seq_len)

    print("=" * 50)
    print("Sinusoidal Positional Encoding Demo")
    print("=" * 50)
    print(f"编码维度: {d_model}，序列长度: {seq_len}")
    print()

    for position, row in enumerate(encoding):
        print(f"位置 {position}: {[f'{val:.4f}' for val in row]}")

    word_vectors: Matrix = [
        [0.1 * (index + 1) for _ in range(d_model)]
        for index in range(seq_len)
    ]
    combined = encoder.add_to(word_vectors)

    print()
    print("=" * 50)
    print("词向量 + 位置编码（前 2 个位置）:")
    print("=" * 50)
    for position in range(2):
        print(f"位置 {position}: {[f'{val:.4f}' for val in combined[position]]}")


if __name__ == "__main__":
    main()
