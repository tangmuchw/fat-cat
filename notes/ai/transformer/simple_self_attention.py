"""简化版 SelfAttention（自注意力）前向传播演示。

仅依赖标准库实现缩放点积注意力的完整流程：线性投影得到 Q/K/V、
计算注意力分数并缩放、Softmax 归一化、加权求和得到输出，
并以一个 4 词序列演示每一步的中间结果。
"""

import math
import random

Matrix = list[list[float]]


def softmax(x: list[float]) -> list[float]:
    """计算 Softmax：把一组数变成概率分布，总和为 1。

    Args:
        x: 待归一化的数值列表，如 [1.0, 2.0, 3.0]。

    Returns:
        与 x 等长的概率列表，每个元素都在 (0, 1) 之间且总和为 1。

    Example:
        >>> softmax([0.0, 0.0, 0.0, 0.0])
        [0.25, 0.25, 0.25, 0.25]
        >>> softmax([0.0, math.log(3.0)])
        [0.25, 0.75]
    """
    max_val = max(x)

    # math.exp(x) 返回 e 的 x 次幂‌，其中 e ≈ 2.718281 是自然对数的底数，即计算 (e^x)。‌‌
    exp_x = [math.exp(v - max_val) for v in x]
    sum_exp = sum(exp_x)
    return [v / sum_exp for v in exp_x]


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
                result[i][j] += a[i][k] * b[k][j]   # 注意：a、b 小写
    return result


def transpose(matrix: Matrix) -> Matrix:
    """矩阵转置：行变列、列变行。

    Args:
        matrix: 待转置的矩阵，形状为 m×n。

    Returns:
        转置后的矩阵，形状为 n×m。

    Example:
        >>> transpose([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
        [[1.0, 4.0], [2.0, 5.0], [3.0, 6.0]]
    """
    return [list(row) for row in zip(*matrix)]


class SimpleSelfAttention:
    """简化的自注意力模块：将输入序列映射为 Query、Key、Value 并计算注意力输出。"""

    def __init__(self, d_model: int, d_k: int) -> None:
        """初始化 Query、Key、Value 的投影权重。

        Args:
            d_model: 输入词向量的维度。
            d_k: 投影后 Query/Key/Value 的维度，同时用于注意力分数的缩放。
        """
        rng = random.Random(42)  # 局部随机生成器，避免重置全局随机状态

        self.d_model: int = d_model
        self.d_k: int = d_k

        # random.normalvariate(mu, sigma) 是 Python 内置 random 模块中用于生成正态分布（高斯分布）随机数的函数‌，
        # 它返回一个浮点数，mu 是均值，sigma 是标准差。‌‌
        # rng.normalvariate(0, 0.1) 生成一个均值为 0、标准差为 0.1 的随机数（标准正态分布）
        # w_query、w_key、w_value 是权重矩阵，形状为 [d_model, d_k]，用于将输入序列投影为 Query、Key、Value。
        self.w_query: Matrix = [[rng.normalvariate(0, 0.1) for _ in range(d_k)]
                                for _ in range(d_model)]
        self.w_key: Matrix = [[rng.normalvariate(0, 0.1) for _ in range(d_k)]
                              for _ in range(d_model)]
        self.w_value: Matrix = [[rng.normalvariate(0, 0.1) for _ in range(d_k)]
                                for _ in range(d_model)]
        print(f"初始化自注意力参数：\nW_query: {self.w_query}\nW_key: {self.w_key}\nW_value: {self.w_value}")

    def project(self, x: Matrix) -> tuple[Matrix, Matrix, Matrix]:
        """将输入序列线性投影为 Query、Key、Value 三个矩阵。

        Args:
            x: 输入序列，形状为 [seq_len, d_model]。

        Returns:
            (q, k, v) 三元组，每个矩阵形状均为 [seq_len, d_k]。
        """
        q = matrix_multiply(x, self.w_query)
        k = matrix_multiply(x, self.w_key)
        v = matrix_multiply(x, self.w_value)

        print("  q 的形状:", len(q), "×", len(q[0]))
        print("  k 的形状:", len(k), "×", len(k[0]))
        print("  v 的形状:", len(v), "×", len(v[0]))

        return q, k, v

    def forward(self, x: Matrix) -> tuple[Matrix, Matrix]:   # X → x
        """执行缩放点积自注意力的完整前向传播。

        Args:
            x: 输入序列，形状为 [seq_len, d_model]。

        Returns:
            (output, attention_weights)：output 为注意力加权求和的结果，
            形状为 [seq_len, d_k]；attention_weights 为归一化后的注意力
            权重，形状为 [seq_len, seq_len]。
        """
        # 步骤 1：计算 q, k, v
        q, k, v = self.project(x)

        # 步骤 2：注意力分数 q·kᵀ
        k_transposed = transpose(k)
        scores = matrix_multiply(q, k_transposed)

        print("\n  原始注意力分数:")
        for i, row in enumerate(scores):
            print(f"    第 {i} 行: {[f'{val:.4f}' for val in row]}")

        # 步骤 3：缩放
        scale_factor = math.sqrt(self.d_k)
        scores_scaled: Matrix = [[val / scale_factor for val in row] for row in scores]

        print("\n  缩放后的注意力分数:")
        for i, row in enumerate(scores_scaled):
            print(f"    第 {i} 行: {[f'{val:.4f}' for val in row]}")

        # 步骤 4：Softmax
        attention_weights: Matrix = [softmax(row) for row in scores_scaled]

        print("\n  注意力权重（Softmax 后）:")
        for i, row in enumerate(attention_weights):
            print(f"    第 {i} 行: {[f'{val:.4f}' for val in row]}")

        # 步骤 5：加权求和
        output = matrix_multiply(attention_weights, v)
        return output, attention_weights


def main() -> None:
    """运行自注意力演示：构造输入序列并打印各步骤的中间结果与最终输出。"""
    d_model = 8
    d_k = 6

    x_input: Matrix = [                    # X → x_input
        [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
    ]

    print("=" * 50)
    print("Self-Attention Demo")
    print("=" * 50)
    print(f"输入序列长度: {len(x_input)}")
    print(f"输入维度: {len(x_input[0])}")
    print()

    attn = SimpleSelfAttention(d_model=d_model, d_k=d_k)
    output, _ = attn.forward(x_input)

    print("\n" + "=" * 50)
    print("自注意力输出:")
    print("=" * 50)
    for i, row in enumerate(output):
        print(f"词 {i} 的输出: {[f'{val:.4f}' for val in row]}")


if __name__ == "__main__":
    main()