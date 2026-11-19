"""简单 Agent 演示：感知 → 决策 → 行动的循环，支持天气查询与算术计算。"""

import re

# 模拟天气数据
WEATHER_DATA = {
    "北京": "晴，25℃",
    "上海": "多云，23℃",
    "广州": "小雨，28℃",
    "深圳": "晴，29℃"
}

# 短期记忆：保存对话历史
history = []


# 感知模块：读取输入
def perceive():
    """读取用户输入的一行文字，并去掉首尾空白。"""
    return input("您：").strip()


# 决策模块：识别任务类型
def make_decision(message):
    """根据消息内容识别任务类型：exit / weather / calculator / chat。"""
    if message.lower() in ("退出", "exit", "quit"):
        return "exit"

    if "天气" in message:
        return "weather"

    if "计算" in message or re.search(
        r"\d\s*[\+\-\*/]\s*\d", message
    ):
        return "calculator"

    return "chat"


# 天气工具：返回模拟数据
def get_weather(message):
    """从消息中提取城市名，返回对应的模拟天气数据。"""
    for city, weather in WEATHER_DATA.items():
        if city in message:
            return f"{city}天气：{weather}（模拟数据）"

    return "请输入北京、上海、广州或深圳进行查询。"


# 计算器工具
def calculator(message):
    """解析并执行两个数字的加减乘除算式，出错时返回提示文字。"""
    # 只识别两个数字组成的简单算式
    pattern = (
        r"(-?\d+(?:\.\d+)?)"
        r"\s*([\+\-\*/])\s*"
        r"(-?\d+(?:\.\d+)?)"
    )

    match = re.search(pattern, message)

    if not match:
        return "请输入算式，例如：计算 10 + 5"

    a = float(match.group(1))
    op = match.group(2)
    b = float(match.group(3))

    if op == "+":
        result = a + b
    elif op == "-":
        result = a - b
    elif op == "*":
        result = a * b
    elif op == "/":
        if b == 0:
            return "计算错误：除数不能为 0"
        result = a / b
    else:
        return "不支持的运算符"

    return f"计算结果：{result:g}"


# 行动模块：调用对应工具
def execute_action(decision, message):
    """根据决策类型调用相应的工具并返回结果。"""
    if decision == "weather":
        return get_weather(message)

    if decision == "calculator":
        return calculator(message)

    return "暂时无法处理该指令，请尝试天气查询或计算。"


# 保存对话历史
def save_history(role, content):
    """把一条对话（角色与内容）追加到全局历史列表。"""
    history.append({
        "role": role,
        "content": content
    })


# Agent 主循环
def run_agent():
    """启动交互式循环：持续感知、决策、执行，退出时打印对话历史。"""
    print("简单 Agent 已启动")
    print("支持天气查询、算术计算")
    print("输入\"退出\"结束程序\n")

    while True:
        try:
            message = perceive()
        except (EOFError, KeyboardInterrupt):
            print("\n程序已结束")
            break

        if not message:
            continue

        # 识别任务
        decision = make_decision(message)

        if decision == "exit":
            print("Agent：再见！")
            break

        # 保存用户输入
        save_history("user", message)

        # 执行操作
        response = execute_action(decision, message)

        # 输出结果
        print("Agent：", response)

        # 保存 Agent 回复
        save_history("assistant", response)

    # 显示本次对话历史
    print("\n本次对话历史：")

    for item in history:
        print(f"{item['role']}：{item['content']}")


# ============================================================
# 测试用例与运行结果
# ------------------------------------------------------------
# 输入（依次输入三行，可通过管道或手动输入）：
#   北京天气
#   计算 10 + 5
#   退出
#
# 输出：
#   简单 Agent 已启动
#   支持天气查询、算术计算
#   输入"退出"结束程序
#
#   您：Agent： 北京天气：晴，25℃（模拟数据）
#   您：Agent： 计算结果：15
#   您：Agent：再见！
#
#   本次对话历史：
#   user：北京天气
#   assistant：北京天气：晴，25℃（模拟数据）
#   user：计算 10 + 5
#   assistant：计算结果：15
# ============================================================

if __name__ == "__main__":
    run_agent()
