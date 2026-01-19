# from veadk.tools.sandbox.code_sandbox import code_sandbox
from veadk.memory.short_term_memory import ShortTermMemory
from veadk import Agent
from veadk.runner import Runner
from veadk.tools.builtin_tools.run_code import run_code

app_name = "coding_agent"
user_id = "test0"
session_id = "test0"

def build_short_memory(model: str) -> ShortTermMemory:
    return ShortTermMemory(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id + f"_{model}",
    )

import os

def read_local_file(file_path: str) -> str:
    """读取本地文件内容"""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        abs_path = os.path.join(script_dir, file_path)
        if os.path.exists(abs_path):
            with open(abs_path, "r", encoding="utf-8") as f:
                return f.read()
    except NameError:
        pass  # __file__ not defined.

    raise FileNotFoundError(f"文件不存在: {file_path}")

def write_local_file(file_path: str, content: str) -> None:
    """写入本地文件内容。如果文件已存在，则在文件末尾追加内容；否则，创建新文件。"""
    if not os.path.isabs(file_path):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(script_dir, file_path)
        except NameError:
            file_path = os.path.abspath(file_path)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    mode = 'a' if os.path.exists(file_path) else 'w'
    with open(file_path, mode, encoding="utf-8") as f:
        f.write(content)


def build_agent(model:str = "doubao-seed-1-6-251015"):
    agent = Agent(
        model_name=model,
        name="coding_agent",
        description="代码智能体来优化代码进行benchmark测试",
        instruction=f"""根据用户的需求，完成代码优化，工作方式为：
        1. 使用read_local_file工具，读取本地代码文件 (代码不要改动)；
        2. For C++ code, don't execute it directly, compile and execute via Python; write sources and object files to /tmp. 
        2. 使用读取到的代码，调用run_code补全函数，通过run_code执行，查看性能如运行时间等指标，执行run_code返回的结果,不要做任何修改，
            使用write_local_file工具将每次生成的代码写到，append模式写入到本地'.source_code/sandbox_meta_info.txt'里，记录每次执行代码的输出和消耗时间，
            按照不同的${model} 区分开，我的目标是要比标准库性能还要好，选择最优的那个算法说明实现。
        3. 使用write_local_file工具，将每次生成的代码都写入本地'.source_code' 文件夹之内，持续的优化代码，每次的优化用{model}_v1, {model}_v2, {model}_vn版本在文件说明区分出来是哪个模型创建的；
        4. 按照不同的model输出报告，append模式写到本地文件'.source_code/{model}_report.md'，输出格式类似下边，
            【优化版本】{model}_v1；
            【优化内容】1. 优化了xxx；2. 优化了yyy，原因是zzz；
            【优化后性能】1. 运行时间从xxx秒优化到yyy秒；2. 内存占用从zzzMB优化到xxxMB；
            【和标准库对比】1. 运行时间比标准库快了xxx秒；2. 内存占用比标准库低了xxxMB；
             【优化版本】{model}_v2；          
             【优化内容】1. 优化了xxx；2. 优化了yyy，原因是zzz；
             【优化后性能】1. 运行时间从xxx秒优化到yyy秒；2. 内存占用从zzzMB优化到xxxMB；
             【和标准库对比】1. 运行时间比标准库快了xxx秒；2. 内存占用比标准库低了xxxMB；
             【优化版本】{model}_vn；
        注意：阶段2，有可能会运行多次来达到最优性能，每次运行都要输出报告。""",
        tools=[run_code, read_local_file, write_local_file],
    )    
    return agent

import time
import asyncio

async def run_for_model(model):
    try:
        print(f"[{model}] 开始运行")
        start_time = time.time()
        root_agent = build_agent(model=model)
        runner = Runner(
            agent=root_agent,
            short_term_memory=build_short_memory(model),
            app_name=app_name,
            user_id=user_id,
        )
        # 等待任务完成并返回结果
        result = await runner.run(
            "我本地有一个文件，topk_benchmark.cpp，想完善这个代码，把my_topk_inplace函数写好，要求性能要非常好，要比代码里面的标准库还要好！",
            session_id=session_id + f"_{model}",
        )
        end_time = time.time()
        print(f"[{model}] 任务已完成，耗时 {end_time - start_time:.2f} 秒")
        print(f"[{model}] 测试结果：{result}")
    except Exception as e:
        print(f"[{model}] 提交失败: {e}")

async def main():
    model_list = ["doubao-seed-1-6-251015", "doubao-seed-code-preview-251028", "deepseek-v3-1-terminus", "kimi-k2-250905"]
    
    # 并发提交所有任务，不等待完成
    await asyncio.gather(*[asyncio.create_task(run_for_model(model)) for model in model_list])
    print("所有模型任务已并发提交，主线程继续执行不阻塞。")
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())