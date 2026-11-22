"""主编排 Agent 演示。

负责把用户请求拆成带依赖的子任务，按依赖顺序并行调度多个子 Agent 执行，
最后整合结果。LLM 与子 Agent 都用本地模拟实现，脚本可直接运行。
"""

import concurrent.futures
from dataclasses import dataclass, field

from multi_agent_system import LLMResponse, MockLLM


@dataclass
class Task:
    """一个子任务：id、负责角色、描述、依赖的任务 id 列表。"""

    id: str
    role: str
    description: str
    dependencies: list[str] = field(default_factory=list)


@dataclass
class TaskResult:
    """子任务的执行结果，成功时 content 有值，失败时 error 有值。"""

    task: Task
    content: str = ""
    error: str = ""

    @property
    def ok(self) -> bool:
        """是否执行成功。"""
        return not self.error


@dataclass
class TaskQueue:
    """任务队列：待执行任务 + 已完成任务 id。"""

    tasks: list[Task]
    completed: set[str] = field(default_factory=set)


@dataclass
class Plan:
    """编排计划：子任务列表；单任务时可直接指定目标角色。"""

    subtasks: list[Task]
    target_role: str = ""


class PlanningLLM(MockLLM):
    """在 MockLLM 基础上增加 plan()，把请求拆成带依赖的任务。"""

    def plan(self, request: str) -> Plan:
        """根据请求关键词生成单任务或多任务计划。"""
        if "简单" in request:
            return Plan(
                subtasks=[Task("t1", "写作员", "写一段简介")],
                target_role="写作员",
            )
        return Plan(subtasks=[
            Task("t1", "研究员", "调研市场数据"),
            Task("t2", "写作员", "基于调研撰写报告", dependencies=["t1"]),
            Task("t3", "审核员", "审核报告", dependencies=["t1"]),
        ])

    def generate(self, prompt: str) -> LLMResponse:
        """按角色关键词返回模拟结果（覆盖父类方法）。"""
        if "整合" in prompt:
            return LLMResponse(content="最终方案：结合调研、初稿与审核，项目可推进。")
        if "写作员" in prompt:
            return LLMResponse(content="报告初稿：Agent 市场规模持续扩大。")
        if "研究员" in prompt:
            return LLMResponse(content="调研结论：市场年增长率约 30%。")
        if "审核员" in prompt:
            return LLMResponse(content="审核结论：内容通过。")
        return LLMResponse(content="（默认响应）")


class Subagent:
    """子 Agent 基类：有角色、关联 LLM 和工具列表。"""

    def __init__(self, role: str, llm: MockLLM, tools: list | None = None) -> None:
        self.role = role
        self.llm = llm
        self.tools = tools or []

    def execute(self, task: str) -> str:
        """执行任务：由子类按角色实现具体逻辑。"""
        return self.llm.generate(f"角色：{self.role}\n任务：{task}").content

    def describe(self) -> str:
        """返回该 Agent 的角色简介。"""
        return f"{self.role}（可用工具 {len(self.tools)} 个）"


class OrchestratorAgent:
    """主编排 Agent：负责任务分解、依赖调度和结果整合。"""

    def __init__(self, llm: PlanningLLM, subagents: list[Subagent]) -> None:
        self.llm = llm
        self.subagents = {agent.role: agent for agent in subagents}

    def handle_request(self, request: str) -> str:
        """处理请求的完整流程：分析 → 调度 → 整合。"""
        plan = self.llm.plan(request)

        if len(plan.subtasks) == 1:
            return self._handle_single(plan)

        return self._handle_multiple(plan)

    def _handle_single(self, plan: Plan) -> str:
        """单任务：直接分发给目标角色执行。"""
        task = plan.subtasks[0]
        agent = self.subagents.get(plan.target_role or task.role)
        if agent is None:
            return f"未知角色：{plan.target_role or task.role}"
        return agent.execute(task.description)

    def _handle_multiple(self, plan: Plan) -> str:
        """多任务：按依赖分批并行执行，再整合结果。"""
        queue = TaskQueue(list(plan.subtasks))
        results: list[TaskResult] = []

        while queue.tasks:
            ready = self.get_parallel_tasks(queue)
            if not ready:
                # 剩余任务存在无法满足的依赖（如循环依赖），避免死循环
                for task in queue.tasks:
                    results.append(TaskResult(task=task, error="依赖无法满足"))
                break

            batch = self.execute_in_parallel(ready)
            results.extend(batch)
            queue = self.update_queue(queue, batch)

        return self.integrate_results(results)

    def get_parallel_tasks(self, queue: TaskQueue) -> list[Task]:
        """取出依赖都已满足的任务，可并行执行。"""
        return [
            task for task in queue.tasks
            if all(dep in queue.completed for dep in task.dependencies)
        ]

    def execute_in_parallel(self, tasks: list[Task]) -> list[TaskResult]:
        """用线程池并行执行任务，统一返回 TaskResult。"""
        results: list[TaskResult] = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(self.execute_task, task): task for task in tasks
            }
            for future in concurrent.futures.as_completed(futures):
                task = futures[future]
                try:
                    results.append(future.result())
                except (ValueError, RuntimeError) as exc:
                    results.append(TaskResult(task=task, error=str(exc)))
        return results

    def execute_task(self, task: Task) -> TaskResult:
        """执行单个任务，无论成功失败都返回 TaskResult。"""
        agent = self.subagents.get(task.role)
        if agent is None:
            return TaskResult(task=task, error=f"未知角色：{task.role}")
        return TaskResult(task=task, content=agent.execute(task.description))

    def update_queue(self, queue: TaskQueue,
                     completed: list[TaskResult]) -> TaskQueue:
        """把已完成任务标记为完成并从待办列表移除。"""
        for result in completed:
            if result.ok:
                queue.completed.add(result.task.id)
        queue.tasks = [
            task for task in queue.tasks if task.id not in queue.completed
        ]
        return queue

    def integrate_results(self, results: list[TaskResult]) -> str:
        """整合所有子任务结果，生成最终回答。"""
        summary = "\n".join(
            f"- {r.task.role}: {r.content if r.ok else '错误：' + r.error}"
            for r in results
        )
        return self.llm.generate(f"整合以下结果：\n{summary}").content

    def list_roles(self) -> list[str]:
        """列出所有可用的子 Agent 角色。"""
        return list(self.subagents)


def main() -> None:
    """构建编排系统，分别演示单任务与多任务（含依赖）两种请求。"""
    llm = PlanningLLM()
    agents = [
        Subagent("研究员", llm),
        Subagent("写作员", llm),
        Subagent("审核员", llm),
    ]
    orchestrator = OrchestratorAgent(llm, agents)

    print("可用角色：", orchestrator.list_roles())
    print("\n[单任务] 结果：", orchestrator.handle_request("简单任务"))
    print("\n[多任务] 结果：", orchestrator.handle_request("写市场报告"))


# ============================================================
# 测试用例与运行结果
# ------------------------------------------------------------
# 输入：无外部输入，直接运行 `python3 orchestrator_agent.py`。
#
# 输出：
#   可用角色： ['研究员', '写作员', '审核员']
#
#   [单任务] 结果： 报告初稿：Agent 市场规模持续扩大。
#
#   [多任务] 结果： 最终方案：结合调研、初稿与审核，项目可推进。
#
# 流程：单任务直接分发给写作员；多任务先由研究员调研，调研完成后
#   写作员与审核员并行执行，最后整合三者结果。
# ============================================================

if __name__ == "__main__":
    main()
