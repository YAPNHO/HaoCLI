import os
import subprocess
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv(override=True) # 加载环境变量

if os.getenv("ANTHROPIC_BASE_URL"):
    os.environ.pop("ANTHROPIC_AUTH_TOKEN", None) # 清除环境变量中的 ANTHROPIC_AUTH_TOKEN, 避免与 Anthropic API 认证冲突

client = Anthropic(base_url=os.getenv("ANTHROPIC_BASE_URL"))
MODEL = os.environ["MODEL_ID"]

SYSTEM = f"You are a coding agent at {os.getcwd()}. Use bash to solve tasks. Act, don't explain." # os.getcwd() 获取当前工作目录, 用于在系统提示中显示当前目录

'''
bash 工具定义,"type": "object" 表示输入参数是一个对象, 包含一个属性command, 类型为字符串
'''
TOOLS = [{
    "name": "bash",
    "description": "Run a shell command.",
    "input_schema": {
        "type": "object",
        "properties": {"command": {"type": "string"}},
        "required": ["command"],
    },
}]

def run_bash(command: str) -> str:
    dangerous = ["rm -rf /", "sudo", "shutdown", "reboot", "> /dev/"] # 防止执行危险命令, 如删除所有文件、重启系统等操作
    if any(d in command for d in dangerous): # d in command for d in dangerous 它会遍历 dangerous 列表中的每个元素 d，检查 d 是否在 command 字符串中。
        return "Error: Dangerous command blocked"
    try:
        r = subprocess.run(command, shell=True, cwd=os.getcwd(), # subprocess用于创建子进程, 执行命令并捕获输出
                           capture_output=True, text=True, timeout=120)
        out = (r.stdout + r.stderr).strip() # .strip() 移除输出首尾的空格
        return out[:50000] if out else "(no output)"
    except subprocess.TimeoutExpired: # 命令执行超时
        return "Error: Timeout (120s)"
    except (FileNotFoundError, OSError) as e:
        return f"Error: {e}"


def agent_loop(messages: list):
    while True:
        response = client.messages.create(
            model=MODEL, system=SYSTEM, messages=messages,
            tools=TOOLS, max_tokens=8000,
        )

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            return

        # Execute each tool call, collect results
        results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"\033[33m$ {block.input['command']}\033[0m")
                output = run_bash(block.input["command"])
                print(output[:200])
                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output,
                })

        messages.append({"role": "user", "content": results})


if __name__ == "__main__":
    print("s01_Loop")
    print("输入问题，回车发送。输入 q 退出。\n")

    history = []
    while True:
        try:
            query = input("\033[36ms01 >> \033[0m")
        except (EOFError, KeyboardInterrupt): # 捕获用户输入的输入流结束 EOFError (Ctrl+D) 或 KeyboardInterrupt (Ctrl+C)
            break
        if query.strip().lower() in ("q", "exit", ""):
            break
        history.append({"role": "user", "content": query})
        agent_loop(history)
        response_content = history[-1]["content"] # 获取模型的最新回复内容
        if isinstance(response_content, list): # 检查 response_content 是否为列表类型
            for block in response_content:
                if getattr(block, "type", None) == "text": # 检查 block 是否为文本块，如果是则打印文本内容
                    print(block.text)
        print()
