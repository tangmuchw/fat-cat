"""文件系统 MCP Server 演示（基于 MCP 2.x 的 MCPServer API）。

通过 stdio 对外提供三个工具：read_file / write_file / list_directory。
所有路径被限制在一个工作目录内，防止越权访问。
直接运行脚本会先做本地自测（不启动 stdio 服务），验证工具逻辑。
"""

import asyncio
from pathlib import Path

from mcp.server.mcpserver import MCPServer

# 允许访问的根目录：脚本所在目录下的 sandbox 子目录
WORKSPACE = Path(__file__).resolve().parent / "mcp_sandbox"
WORKSPACE.mkdir(exist_ok=True)

app = MCPServer("filesystem")


def resolve_safe_path(path: str) -> Path:
    """把相对路径解析到 WORKSPACE 内，阻止访问工作目录之外的文件。"""
    target = (WORKSPACE / path).resolve()
    if not target.is_relative_to(WORKSPACE):
        raise ValueError(f"路径越界：{path}")
    return target


@app.tool(name="read_file", description="读取文件内容")
def read_file(path: str, encoding: str = "utf-8") -> str:
    """读取指定文件并返回文本内容。"""
    target = resolve_safe_path(path)
    if not target.is_file():
        raise ValueError(f"不是文件：{path}")
    return target.read_text(encoding=encoding)


@app.tool(name="write_file", description="写入文件内容（自动创建父目录）")
def write_file(path: str, content: str) -> str:
    """把内容写入指定文件，返回成功提示。"""
    target = resolve_safe_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return f"已写入：{path}（{len(content)} 字符）"


@app.tool(name="list_directory", description="列出目录内容")
def list_directory(path: str = ".") -> str:
    """列出目录下的条目名称，用换行分隔。"""
    target = resolve_safe_path(path)
    if not target.is_dir():
        raise ValueError(f"不是目录：{path}")
    return "\n".join(sorted(entry.name for entry in target.iterdir()))


async def self_test() -> None:
    """本地自测：直接调用三个工具，验证读写列目录与路径安全。"""
    tools = await app.list_tools()
    print("可用工具：", [tool.name for tool in tools])

    print("写入：", await app.call_tool("write_file", {
        "path": "notes/demo.txt", "content": "Hello MCP!"
    }))
    print("读取：", await app.call_tool("read_file", {"path": "notes/demo.txt"}))
    print("列目录：", await app.call_tool("list_directory", {"path": "notes"}))

    try:
        await app.call_tool("read_file", {"path": "../outside.txt"})
        print("越权访问：未拦截")
    except Exception:  # pylint: disable=broad-exception-caught
        # MCPServer 把工具内的 ValueError 包装成 UnexpectedToolError，
        # 这里统一捕获以确认越权路径确实被拒绝（自测用途）。
        print("越权访问：已拦截")


def main() -> None:
    """先跑本地自测，再以 stdio 传输启动 MCP 服务。"""
    print("=== 本地自测 ===")
    asyncio.run(self_test())
    print("\n=== 启动 MCP Server（stdio）===")
    app.run("stdio")


# ============================================================
# 测试用例与运行结果（本地自测部分）
# ------------------------------------------------------------
# 输入：无外部输入，直接运行 `python3 filesystem_mcp_server.py`。
#
# 输出（节选）：
#   可用工具： ['read_file', 'write_file', 'list_directory']
#   写入： ... text='已写入：notes/demo.txt（10 字符）' ...
#   读取： ... text='Hello MCP!' ...
#   列目录： ... text='demo.txt' ...
#   越权访问： 已拦截
#
# 说明：自测会在脚本同目录创建 mcp_sandbox/notes/demo.txt；
#   路径越界（如 ../outside.txt）会被 resolve_safe_path 拒绝。
#   自测后正式以 stdio 启动服务，供 MCP 客户端调用。
# ============================================================

if __name__ == "__main__":
    main()
