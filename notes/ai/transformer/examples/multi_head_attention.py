"""简化版 MultiHeadAttention（多头注意力）前向传播演示。

在缩放点积自注意力（见 simple_self_attention.py）的基础上，将输入投影到
多个独立的子空间：每个头各自计算 Query/Key/Value 与注意力权重，再把各头
输出按列拼接并经输出投影融合，展示多头注意力如何并行捕捉不同关系。
仅依赖标准库实现，并以一个 4 词序列演示各头权重与最终输出。
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
                result[i][j] += a[i][k] * b[k][j]
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


def concat_columns(matrices: list[Matrix]) -> Matrix:
    """按列拼接多个等行数的矩阵，用于合并各头的输出。

    Args:
        matrices: 矩阵列表，每个矩阵形状为 m×n_i，行数必须相同。

    Returns:
        拼接后的矩阵，形状为 m×(n_1 + n_2 + ...)。

    Example:
        两个头各输出 [2,2]，按列拼成 [2,4]（同一个词的两头输出排在同一行）：
        >>> concat_columns([[[1.0, 2.0], [3.0, 4.0]], [[5.0, 6.0], [7.0, 8.0]]])
        [[1.0, 2.0, 5.0, 6.0], [3.0, 4.0, 7.0, 8.0]]
    """
    return [
        [value for matrix in matrices for value in matrix[row]]
        for row in range(len(matrices[0]))
    ]


class MultiHeadAttention:
    """简化的多头注意力模块：多个头并行计算注意力，拼接后投影融合。"""

    def __init__(self, d_model: int, num_heads: int) -> None:
        """初始化各头独立的投影权重，以及拼接后的输出投影权重。

        Args:
            d_model: 输入词向量的维度，必须能被 num_heads 整除。
            num_heads: 注意力头的数量。

        Raises:
            ValueError: 当 d_model 不能被 num_heads 整除时抛出。
        """
        if d_model % num_heads != 0:
            raise ValueError("d_model 必须能被 num_heads 整除")

        rng = random.Random(42)  # 局部随机生成器，避免重置全局随机状态
        self.d_model: int = d_model
        self.num_heads: int = num_heads
        self.d_k: int = d_model // num_heads

        def random_matrix(rows: int, cols: int) -> Matrix:
            return [[rng.normalvariate(0, 0.1) for _ in range(cols)]
                    for _ in range(rows)]

        self.w_queries: list[Matrix] = [
            random_matrix(d_model, self.d_k) for _ in range(num_heads)
        ]
        self.w_keys: list[Matrix] = [
            random_matrix(d_model, self.d_k) for _ in range(num_heads)
        ]
        self.w_values: list[Matrix] = [
            random_matrix(d_model, self.d_k) for _ in range(num_heads)
        ]
        self.w_output: Matrix = random_matrix(d_model, d_model)

    def project(self, x: Matrix) -> tuple[list[Matrix], list[Matrix], list[Matrix]]:
        """为每个注意力头分别计算 Query、Key、Value 矩阵。

        Args:
            x: 输入序列，形状为 [seq_len, d_model]。

        Returns:
            (queries, keys, values) 三个列表，每个列表含 num_heads 个矩阵，
            每个矩阵形状均为 [seq_len, d_k]。
        """
        queries = [matrix_multiply(x, weight) for weight in self.w_queries]
        keys = [matrix_multiply(x, weight) for weight in self.w_keys]
        values = [matrix_multiply(x, weight) for weight in self.w_values]
        return queries, keys, values

    def forward(self, x: Matrix) -> tuple[Matrix, list[Matrix]]:
        """执行多头注意力的完整前向传播。

        Args:
            x: 输入序列，形状为 [seq_len, d_model]。

        Returns:
            (output, attention_weights)：output 为拼接并经输出投影融合后的
            结果，形状为 [seq_len, d_model]；attention_weights 为各头的注意
            力权重列表，每个矩阵形状为 [seq_len, seq_len]。
        """
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


def main() -> None:
    """运行多头注意力演示：构造输入序列并打印各头权重与融合后的输出。"""
    d_model = 8
    num_heads = 2

    x_input: Matrix = [
        [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
    ]

    print("=" * 50)
    print("Multi-Head Attention Demo")
    print("=" * 50)
    print(f"输入序列长度: {len(x_input)}")
    print(f"输入维度: {len(x_input[0])}")
    print(f"注意力头数: {num_heads}，每头维度: {d_model // num_heads}")
    print()

    attention = MultiHeadAttention(d_model=d_model, num_heads=num_heads)
    output, attention_weights = attention.forward(x_input)

    for head_index, weights in enumerate(attention_weights):
        print(f"头 {head_index} 的注意力权重:")
        for row_index, row in enumerate(weights):
            print(f"  词 {row_index}: {[f'{val:.4f}' for val in row]}")
        print()

    print("=" * 50)
    print("多头融合后的输出:")
    print("=" * 50)
    for word_index, row in enumerate(output):
        print(f"词 {word_index} 的输出: {[f'{val:.4f}' for val in row]}")


# ============================================================
# 执行 main() 的输入与输出
# ------------------------------------------------------------
# 输入：d_model=8, num_heads=2（每头 d_k=4），x_input 为 4 词、每词 8 维的 one-hot 序列。
# 输出（打印）：两个头各自的注意力权重（均为 4×4，每行和为 1），
#   例如头 0 词 0: ['0.2512', '0.2501', '0.2490', '0.2497']；
#   头 1 词 0: ['0.2469', '0.2484', '0.2486', '0.2561']（两头分布不同）。
#   最后是多头拼接并经 W_o 融合后的 8 维输出，例如：
#   词 0: ['0.0223', '0.0126', '0.0024', '0.0054', '0.0045', '-0.0251', '-0.0056', '-0.0214']
# ============================================================

if __name__ == "__main__":
    main()
