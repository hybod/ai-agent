# 1. Agent 评测
你可以通过以下三种方式评测你的 Agent ：
1. 基于网页的用户界面（veadk web）
通过基于网页的界面，以交互方式评测 Agent 。操作过程中可直接在网页上与 Agent 互动，实时观察其表现并进行评测。
2. 命令行界面（veadk eval）
直接从命令行对现有的评测集文件运行评测。无需打开图形界面，通过输入命令即可快速执行评测操作，适合熟悉命令行的开发人员。
3. 编程方式（pytest）
使用 pytest（Python 的一种测试框架）和测试文件，将评测集成到你的测试流程中。这种方式适合自动化测试场景，可与现有开发测试链路无缝衔接。

VeADK 目前支持 [DeepEval](https://deepeval.com/) 和 [ADKEval](https://google.github.io/adk-docs/evaluate/) 两种评测器。

|评测器|简介|推荐使用场景|
|-----|---|-----------|
|ADKEval|ADK 是 Agent Development Kit（由 Google 推出）用于构建代理（agent）或多代理系统的平台。它内置了评估机制，用于衡量“agent”在执行任务、调用工具、步骤轨迹等方面的表现。|<li>如果你的系统是一个 agent（或多agent）系统：例如用户的问题可能触发多个工具调用、多个子步骤、agent 需要判断、切换工具、执行任务、然后给出最终输出。<li>如果你要追踪不仅“最终回答”，还要追踪“中间工具调用”、“agent使用了哪些子agent”、“执行轨迹是否符合预期”。例如：任务规划、执行、反馈循环、业务流程自动化。
|DeepEval|DeepEval 是一个开源的 LLM（大语言模型）评估框架，专注于“LLM 输出”（包括 RAG、聊天机器人、生成任务等）质量的自动化评估。|<li>如果你的系统主要是 “LLM → 输出” 型，比如：用户提问 → 模型回答；或者 RAG (检索 + 生成) 系统，注重回答的相关性、事实正确性、连贯性、可解释性，而不太依赖工具调用或复杂的代理轨迹，希望专注于 “生成质量” 监控。<li>如果你希望引入比较丰富的指标（如 hallucination 检测、contextual recall／precision、answer relevancy等），并希望把评估作为 CI/CD流程的一部分（像单元测试那样）运行。
|两者混用||<li>如果你的系统既包含“生成模块”（回答用户）又包含“agent流程”（工具调用、子任务执行），那么可以考虑混用：a) 对于“回答质量”部分：用 DeepEval 来做，比如检索+生成、聊天对话。b) 对于“流程/agent行为”部分：用 ADKEval 来做，比如工具调用路径、任务完成过程、agent 内部策略符合预期。<li>你也可以在早期阶段（模型／生成效果验证）用 DeepEval，然后在进入“agent化部署”阶段切换或引入 ADKEval，来增强流程监控。



# 2. 项目结构

```bash
/evaluation/
├── config.yaml # 配置文件 (需要用户复制config.yaml.example并更名为config.yaml，填写api_key和aksk)
├── config.yaml.example # 配置文件示例
├── ecommerce_agent # 示例 Agent
│   ├── __init__.py
│   ├── agent.py
│   ├── simple.evalset.json # 简单评测用例集（单轮对话），veadk web 会从 Agent 所在目录加载和保存评测集
│   └── complex.evalset.json # 复杂评测用例集（多轮对话），veadk web 会从 Agent 所在目录加载和保存评测集
└── tests
    ├── simple.test.json # 简单评测用例集（单轮对话），用于 veadk eval 和 pytest
    ├── complex.test.json # 复杂评测用例集（多轮对话），用于 veadk eval 和 pytest
    └── test_agent.py # 测试文件，用于 pytest
```

# 3. 快速开始

### 依赖
- VeADK 0.2.18 及以上版本
- Python 3.12 及以上版本

### 启动
**安装必需依赖：**
```bash
# Clone this repository.
git clone git@code.byted.org:data/agent_workshop.git
cd agent_workshop/workshops/session3/evaluation
# Install the package and dependencies.
uv venv --python 3.12
source .venv/bin/activate
uv sync

# 复制config.yaml.example并更名为config.yaml，填写api_key和aksk
```

# 4. veadk web
网页用户界面（Web UI）提供了一种交互式方式，可用于评测 Agent 、生成评测数据集以及详细检查 Agent 行为。

**步骤 1：创建并保存测试用例**
* 通过运行命令启动 Web 服务器：`veadk web`
* 在网页界面中，选择一个 Agent 并与其交互以创建会话。
* 选择界面右侧的 `Eval` 标签页。
* 创建新的评测集或选择现有评测集。
* 点击 `Add current session`，将对话保存为新的评测用例。

**步骤 2：查看和编辑你的测试用例**

用例保存后，可点击列表中的用例 ID 进行查看。如需修改，点击 `Edit current eval case` 图标（铅笔图标）。此交互式视图支持以下操作：
* 修改 Agent 的文本响应，以优化测试场景。
* 从对话中删除单个 Agent 消息。
* 若评测用例不再需要，可删除整个用例。

**步骤 3：使用自定义指标运行评测**
1. 从你的评测集中选择一个或多个测试用例。
2. 点击 `Run Evaluation`，会弹出 `EVALUATION METRIC` 对话框。
3. 在对话框中，使用滑块配置以下指标的阈值：
    * Tool trajectory avg score：工具调用轨迹平均得分，取值范围0~1，1表示完全匹配
    * Response match score：响应匹配得分，取值范围0~1，1表示完全匹配
4. 点击 `Start`，使用你的自定义标准运行评测。评测历史记录会记录每次运行所使用的指标。

**步骤 4：分析结果**

运行完成后，你可以按以下方式分析结果：
* 分析运行失败情况：点击任意 `Pass` 或 `Fail` 结果。对于失败的情况，你可以将鼠标悬停在 `Fail` 标签上，查看实际输出与预期输出的并排对比，以及导致失败的具体分数。

![veadk_web_eval.gif](images/veadk_web_eval.gif)

# 5 生成评测文件

除了使用`veadk web`通过网页操作的方式生成评测集文件，我们还可以在 Agent 运行结束后，通过调用 runner.save_eval_set() 将运行时数据导出为评测集文件。

```python
async def main(messages: str):
    response = await runner.run(messages=messages, session_id=session_id)
    # Save the running results as evaluation data.
    dump_eval_path = await runner.save_eval_set(session_id=session_id, eval_set_id=uuid.uuid4().hex)
    print(f"prompt: {messages},\n response: {response},\n dump_eval_path: {dump_eval_path}")
```

# 6. veadk eval
你也可以通过命令行界面（CLI）对评测集文件运行评测。这种方式执行的评测与在用户界面（UI）上运行的评测完全相同，但更有助于实现自动化 —— 例如，你可以将此命令添加到常规的构建生成和验证流程中。

例如，示例命令：`veadk eval --agent-dir ecommerce_agent --evalset-file tests/simple.test.json --evaluator deepeval`

`--evaluator`可选值包括adk、deepeval

了解更多详细使用方式：`veadk eval --help`

![veadk_eval.gif](images/veadk_eval.gif)

# 7. pytest
你也可以使用 pytest 来运行测试文件，将其作为集成测试的一部分。

示例命令：`python -m pytest tests/test_agent.py -v`

示例测试代码：以下是一个运行单个测试文件的 pytest 测试用例示例
```python
class TestAgentEvaluation:
    """Agent evaluation tests using ADKEvaluator"""

    @pytest.mark.asyncio
    async def test_simple_evalset_with_adkevaluator(self):
        """Agent evaluation tests using ADKEvaluator"""
        evaluator = ADKEvaluator(agent=agent)
        await evaluator.evaluate(
            eval_set_file_path="tests/simple.test.json",
            response_match_score_threshold=1,
            tool_score_threshold=0.5,
            num_runs=1,
            print_detailed_results=True
        )

    @pytest.mark.asyncio
    async def test_simple_evalset_with_deepevalevaluator(self):
        """Agent evaluation tests using DeepevalEvaluator"""
        evaluator = DeepevalEvaluator(agent=agent)
        metrics = [
            GEval(
                threshold=0.8,
                name="Base Evaluation",
                criteria=eval_principle_prompt,
                evaluation_params=[
                    LLMTestCaseParams.INPUT,
                    LLMTestCaseParams.ACTUAL_OUTPUT,
                    LLMTestCaseParams.EXPECTED_OUTPUT,
                ],
                model=evaluator.judge_model,
            ),
            ToolCorrectnessMetric(threshold=0.5, model=evaluator.judge_model),
        ]
        await evaluator.evaluate(
            eval_set_file_path="tests/simple.test.json", 
            metrics=metrics)        
```