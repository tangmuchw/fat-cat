"""简化版 RNN 前向传播演示。

实现一个仅依赖标准库的 SimpleRNN 类，逐时间步计算
h_new = tanh(Wx·x + Wh·h_prev + b)，用于直观展示循环神经网络的前向传播原理，
并以一个 4 步向量序列演示隐藏状态的输出。
"""

import math
import random


class SimpleRNN:
    """简化的 RNN 实现，用于演示原理。"""

    def __init__(self, input_size: int, hidden_size: int):
        """初始化 RNN 参数。"""
        rng = random.Random(42)  # 局部随机生成器，避免重置全局随机状态

        # 输入到隐藏层的权重（input_size × hidden_size）
        self.wx: list[list[float]] = [
            [rng.uniform(-0.1, 0.1) for _ in range(hidden_size)]
            for _ in range(input_size)
        ]
        # 隐藏层到隐藏层的权重（hidden_size × hidden_size）
        self.wh: list[list[float]] = [
            [rng.uniform(-0.1, 0.1) for _ in range(hidden_size)]
            for _ in range(hidden_size)
        ]
        # 偏置，模型参数
        self.b: list[float] = [0.0 for _ in range(hidden_size)]
        print(f"初始化 RNN 参数：\nWx: {self.wx}\nWh: {self.wh}\nb: {self.b}")


    def step(self, x: list[float], h_prev: list[float]) -> list[float]:
        """单步 RNN：输入 x 和前一时刻隐藏状态 h_prev，输出新的隐藏状态。"""
        hidden_size = len(self.b)
        h_new: list[float] = [0.0 for _ in range(hidden_size)]

        # 点积（内积）的核心作用是：把两个向量“按对应分量相乘再相加”，从而得到一个标量，用来衡量它们的“方向关系”和“加权组合效果”。
        # h_new = tanh(Wx·x + Wh·h_prev + b)
        for i in range(hidden_size):
            wx_sum = sum(x[j] * self.wx[j][i] for j in range(len(x))) # 求 wx 点积
            wh_sum = sum(h_prev[j] * self.wh[j][i] for j in range(hidden_size)) # 求 wh 点积
            h_new[i] = math.tanh(wx_sum + wh_sum + self.b[i])

        return h_new

    def forward(self, sequence: list[list[float]]) -> list[list[float]]:
        """处理完整序列，返回每一步的隐藏状态。"""
        state_size = len(self.b)
        hidden_state: list[float] = [0.0 for _ in range(state_size)]
        states: list[list[float]] = []

        for x in sequence:
            hidden_state = self.step(x, hidden_state)
            states.append(hidden_state)

        return states


def main() -> None:
    """用简单的向量序列演示 RNN 前向传播。"""
    input_size = 4
    hidden_size = 3

    rnn = SimpleRNN(input_size, hidden_size)

    # 4 个词，每个词用 4 维 one-hot 向量表示
    sequence: list[list[float]] = [
        [1.0, 0.0, 0.0, 0.0],  # 词 1
        [0.0, 1.0, 0.0, 0.0],  # 词 2
        [0.0, 0.0, 1.0, 0.0],  # 词 3
        [0.0, 0.0, 0.0, 1.0],  # 词 4
    ]

    hidden_states = rnn.forward(sequence)

    print("简单 RNN 演示")
    print("=" * 40)
    for i, h in enumerate(hidden_states):
        print(f"第 {i + 1} 步隐藏状态: {[f'{v:.4f}' for v in h]}")


if __name__ == "__main__":
    main()

# 简单 RNN 演示
# ========================================
# 第 1 步隐藏状态: ['0.0204', '-0.0434', '0.0556']
# 第 2 步隐藏状态: ['-0.0061', '-0.0529', '0.0775']
# 第 3 步隐藏状态: ['0.0641', '-0.0409', '0.0655']
# 第 4 步隐藏状态: ['0.0143', '-0.0805', '0.0277']
