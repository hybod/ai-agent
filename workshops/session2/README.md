# Session 2 Agent 项目总结
本文档以表格形式总结了本 Session 中的 Agent 项目及其核心能力。
| 项目 | 主要能力点 |
| --- | --- |
| **`a2a`** | 1. 演示了 Agent-to-Agent (A2A) 通信协议。 2. 包含一个远程 Agent 作为工具提供方 (Tool Provider)，以及一个本地客户端 Agent 作为协作方 (Orchestrator)。 3. 远程 Agent 提供了“投掷骰子”和“检查质数”两个工具。 4. 本地客户端通过 A2A 协议调用远程 Agent 的工具，并完成协作任务。 |
| **`agent_deploy`** | 1. 提供了 `veadk_web_agent` 的部署流程。 2. `veadk_web_agent` 具备生成图片和视频的能力。 3. 展示了如何将一个 Agent 部署为 Web 服务。 |
| **`assistant_agent`** | 1. 演示了主 Agent (Assistant Agent) 如何调用子 Agent (Sub-agent) 来完成复杂任务。 2. 包含 `loop_agent`、`parallel_agent` 和 `sequential_agent` 三个子 Agent。 3. 主 Agent 根据用户意图，自主决定调用哪个子 Agent 来执行任务。 |
| **`mcp`** | 1. 演示了 MCP的使用。 2. 包含一个 MCP 客户端和一个 MCP 服务端。 3. 客户端通过 MCP 协议与服务端进行多轮交互，以完成调用高德地图 API 的任务。 4. 服务端将本地能力（高德地图 API）通过 MCP 协议暴露给客户端。 |
| **`rag`** | 1. 演示了检索增强生成（Retrieval-Augmented Generation, RAG）技术。 2. 提供了分别基于 `OpenSearch` 和 `Viking DB` 的RAG实现。 3. 展示了Agent如何从外部知识库检索信息，以生成更准确、更丰富的回答。 |
| **`callback`** | 1. 演示了如何在 Agent 中使用回调 (Callback) 和护栏 (Guardrail) 功能。 2. 实现了内容审查、参数校验、日志记录、请求修改、响应过滤等多种回调功能。 3. 通过一个中文内容审查的例子，展示了如何使用全生命周期的回调函数来增强 Agent 的可控性和安全性。 |