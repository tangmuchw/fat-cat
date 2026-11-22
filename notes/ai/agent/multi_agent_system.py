"""多 Agent 协作系统演示（类似 AutoGen / MetaGPT 风格）。

协调者把复杂任务拆解成子任务，分发给不同角色的 Agent 并行处理，
最后整合结果。LLM、工具、响应对象都用本地模拟实现，脚本可直接运行。
"""

import json
from dataclasses import dataclass, field


# ---------- 模拟基础设施 ----------

@dataclass
class LLMResponse:
    """LLM 的响应：要么是普通文本，要么是一次工具调用。"""

    content: str = ""
    needs_tool_call: bool = False
    tool_name: str = ""
    tool_input: str = ""


class MockLLM:
    """根据提示词关键词返回预设响应，代替真实大模型。"""

    def generate(self, prompt: str) -> LLMResponse:
        """按 prompt 里出现的关键词生成模拟响应。"""
        if "你的角色是研究员" in prompt:
            return LLMResponse(content="研究结果：2024 年 AI Agent 市场增长迅速。")
        if "你的角色是写作员" in prompt:
            return LLMResponse(content="初稿：AI Agent 是当下最热门的方向之一。")
        if "需要调用工具" in prompt:
            return LLMResponse(
                needs_tool_call=True, tool_name="calculator", tool_input="6 * 7"
            )
        if "分解为子任务" in prompt:
            return LLMResponse(
                content='{"researcher": "调研 Agent 市场", "writer": "撰写报告初稿"}'
            )
        if "整合以下 Agent 的执行结果" in prompt:
            return LLMResponse(content="最终报告：结合调研与初稿，Agent 市场前景广阔。")
        return LLMResponse(content="（默认响应）")

    def reset(self) -> None:
        """重置模型状态（模拟用，当前无状态可直接忽略）。"""
        return None


class Tool:  # pylint: disable=too-few-public-methods
    """工具基类，所有工具都实现 run 方法。

    作为抽象基类只需暴露 run 一个入口，故禁用 too-few-public-methods。
    """

    def __init__(self, name: str) -> None:
        self.name = name

    def run(self, tool_input: str) -> str:
        """执行工具，子类必须覆盖。"""
        raise NotImplementedError


class CalculatorTool(Tool):  # pylint: disable=too-few-public-methods
    """简易计算器工具，只处理形如 a*b 的整数乘法。

    工具类只需暴露 run 一个执行入口，故禁用 too-few-public-methods。
    """

    def __init__(self) -> None:
        super().__init__("calculator")

    def run(self, tool_input: str) -> str:
        """解析 a*b 并返回乘积。"""
        try:
            left, right = tool_input.split("*")
            return f"计算结果：{int(left) * int(right)}"
        except (ValueError, AttributeError):
            return f"无法计算：{tool_input}"


@dataclass
class Plan:
    """协调者产出的执行计划：角色 → 子任务。"""

    subtasks: dict[str, str] = field(default_factory=dict)

    @classmethod
    def parse(cls, response: LLMResponse) -> "Plan":
        """从 LLM 的 JSON 文本响应中解析出子任务字典。"""
        text = response.content.strip()
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1:
            return cls()
        return cls(subtasks=json.loads(text[start:end + 1]))

    def get(self, role: str) -> str:
        """按角色名取子任务，找不到返回空字符串。"""
        return self.subtasks.get(role, "")


# ---------- Agent 定义 ----------

class Agent:
    """基础 Agent：有自己的角色、工具和执行逻辑。"""

    def __init__(self, role: str, llm: MockLLM, tools: list[Tool]) -> None:
        """初始化 Agent。

        Args:
            role: 角色名称，如 researcher / writer。
            llm: 关联的语言模型。
            tools: 可用工具列表。
        """
        self.role = role
        self.llm = llm
        self.tools = tools

    def execute(self, task: str, context: str = "") -> str:
        """执行任务：构建提示词 → 调用 LLM → 必要时调用工具。"""
        prompt = self.build_prompt(task, context)
        response = self.llm.generate(prompt)
        if response.needs_tool_call:
            return self.execute_tool(response)
        return response.content

    def build_prompt(self, task: str, context: str) -> str:
        """构建带角色设定的提示词。"""
        return (
            f"你的角色是{self.role}\n任务：{task}\n上下文：{context}\n"
            "如需工具请在回复中说明。"
        )

    def execute_tool(self, response: LLMResponse) -> str:
        """根据 LLM 的工具调用请求执行对应工具。"""
        tool = self.get_tool(response.tool_name)
        if tool is None:
            return f"工具不存在：{response.tool_name}"
        return tool.run(response.tool_input)

    def get_tool(self, name: str) -> Tool | None:
        """按名称查找工具，找不到返回 None。"""
        return next((tool for tool in self.tools if tool.name == name), None)


class CoordinatorAgent:
    """协调者 Agent：负责任务分解与结果整合。"""

    def __init__(self, llm: MockLLM) -> None:
        self.llm = llm

    def decompose(self, task: str) -> Plan:
        """分析任务，决定需要哪些角色及其子任务。"""
        prompt = f"分解为子任务：{task}"
        response = self.llm.generate(prompt)
        return Plan.parse(response)

    def integrate(self, results: dict[str, str]) -> str:
        """整合多个 Agent 的结果，生成最终回答。"""
        prompt = f"整合以下 Agent 的执行结果：{results}"
        return self.llm.generate(prompt).content


class MultiAgentSystem:
    """多 Agent 协作系统：管理多个 Agent 之间的协作。"""

    def __init__(self, agents: list[Agent], coordinator: CoordinatorAgent) -> None:
        self.agents: dict[str, Agent] = {agent.role: agent for agent in agents}
        self.coordinator = coordinator

    def solve(self, task: str) -> str:
        """解决复杂任务：分解 → 分发 → 整合。"""
        plan = self.coordinator.decompose(task)
        results = self.dispatch(plan)
        return self.coordinator.integrate(results)

    def dispatch(self, plan: Plan) -> dict[str, str]:
        """把子任务分发给对应角色的 Agent，收集执行结果。"""
        results: dict[str, str] = {}
        for role, subtask in plan.subtasks.items():
            agent = self.agents.get(role)
            if agent is None:
                results[role] = f"未找到角色：{role}"
            else:
                results[role] = agent.execute(subtask)
        return results

    def list_roles(self) -> list[str]:
        """列出系统中所有可用角色。"""
        return list(self.agents)


def main() -> None:
    """构建多 Agent 系统并演示一次任务求解。"""
    llm = MockLLM()
    researcher = Agent("研究员", llm, [])
    writer = Agent("写作员", llm, [CalculatorTool()])
    coordinator = CoordinatorAgent(llm)
    system = MultiAgentSystem([researcher, writer], coordinator)

    print("可用角色：", system.list_roles())
    print("求解任务：写一篇 AI Agent 市场报告")
    print("最终结果：", system.solve("写一篇 AI Agent 市场报告"))

    print("\n工具调用演示：")
    print(writer.execute_tool(LLMResponse(
        needs_tool_call=True, tool_name="calculator", tool_input="6 * 7"
    )))


# ============================================================
# 测试用例与运行结果
# ------------------------------------------------------------
# 输入：无外部输入，直接运行 `python3 multi_agent_system.py`。
#
# 输出：
#   可用角色： ['研究员', '写作员']
#   求解任务：写一篇 AI Agent 市场报告
#   最终结果： 最终报告：结合调研与初稿，Agent 市场前景广阔。
#
#   工具调用演示：
#   计算结果：42
#
# 流程：协调者把任务拆成「研究员调研 + 写作员撰写」，分发给两个 Agent
#   各自执行，再由协调者整合结果；末尾单独演示一次工具调用。
# ============================================================

if __name__ == "__main__":
    main()
