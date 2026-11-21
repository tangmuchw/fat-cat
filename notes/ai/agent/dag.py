"""DAG 工作流的简化定义（类似 LangGraph 风格）。

演示用 LangGraph 把一条数据处理流水线编排成 DAG：
提取 → 清洗 → 分析 → 生成报告。
所有外部依赖（数据库、LLM）都用本地模拟实现，脚本可直接运行。
"""

from typing import TypedDict

from langgraph.graph import END, StateGraph

# 模拟原始日志数据（代替数据库）
MOCK_LOGS = [
    "INFO user=alice action=login",
    "ERROR user=bob action=pay",
    "INFO user=alice action=login",
    "WARN user=carol action=view",
    "ERROR user=bob action=pay",
]


class PipelineState(TypedDict):
    """节点间传递的数据对象，必须用 TypedDict 供 LangGraph 校验。"""

    raw_data: list[str]      # 原始输入数据
    cleaned_data: list[str]  # 清洗后的数据
    analysis_result: dict    # 分析结果
    final_report: str        # 最终报告


# ---------- 模拟外部依赖 ----------

def query_database(sql: str) -> list[str]:
    """模拟数据库查询：返回预置的日志列表。"""
    print(f"  [数据库] 执行: {sql}")
    return list(MOCK_LOGS)


def preprocess(raw_data: list[str]) -> list[str]:
    """清洗数据：去重并过滤掉 WARN 级别。"""
    unique = list(dict.fromkeys(raw_data))
    return [line for line in unique if not line.startswith("WARN")]


def statistical_analysis(cleaned_data: list[str]) -> dict:
    """统计分析：统计总条数与各级别出现次数。"""
    levels = ["INFO", "WARN", "ERROR"]
    return {
        "total": len(cleaned_data),
        "by_level": {
            level: sum(1 for line in cleaned_data if line.startswith(level))
            for level in levels
        },
    }


def generate_report(analysis: dict) -> str:
    """模拟 LLM 生成报告：按分析结果拼一段文字。"""
    by_level = analysis["by_level"]
    return (
        f"数据分析报告：共 {analysis['total']} 条清洗后日志，"
        f"其中 INFO {by_level['INFO']} 条、ERROR {by_level['ERROR']} 条。"
    )


# ---------- 定义 DAG 节点 ----------
# 每个节点接收当前状态，只返回自己负责更新的字段（字典）

def extract_data(state: PipelineState) -> dict:  # pylint: disable=unused-argument
    """节点1：从数据库提取原始数据。

    作为入口节点不需要读取 state，但 LangGraph 要求节点函数接收 state 参数。
    """
    print("节点1：提取数据")
    return {"raw_data": query_database("SELECT * FROM logs")}


def clean_data(state: PipelineState) -> dict:
    """节点2：清洗数据（去重、过滤）。"""
    print("节点2：清洗数据")
    return {"cleaned_data": preprocess(state["raw_data"])}


def analyze(state: PipelineState) -> dict:
    """节点3：统计分析。"""
    print("节点3：分析数据")
    return {"analysis_result": statistical_analysis(state["cleaned_data"])}


def report(state: PipelineState) -> dict:
    """节点4：生成最终报告。"""
    print("节点4：生成报告")
    return {"final_report": generate_report(state["analysis_result"])}


# ---------- 构建 DAG：定义节点和边（数据流向）----------

workflow = StateGraph(PipelineState)
workflow.add_node("extract", extract_data)
workflow.add_node("clean", clean_data)
workflow.add_node("analyze", analyze)
workflow.add_node("report", report)

# 定义边：extract → clean → analyze → report → END
workflow.add_edge("extract", "clean")
workflow.add_edge("clean", "analyze")
workflow.add_edge("analyze", "report")
workflow.add_edge("report", END)
workflow.set_entry_point("extract")

# ---------- 编译并运行 ----------

app = workflow.compile()
result = app.invoke({})
print("\n最终报告：", result["final_report"])

# ============================================================
# 测试用例与运行结果
# ------------------------------------------------------------
# 输入：无外部输入，直接运行 `python3 dag.py`。
#
# 输出：
#   节点1：提取数据
#     [数据库] 执行: SELECT * FROM logs
#   节点2：清洗数据
#   节点3：分析数据
#   节点4：生成报告
#
#   最终报告： 数据分析报告：共 2 条清洗后日志，其中 INFO 1 条、ERROR 1 条。
# ============================================================
