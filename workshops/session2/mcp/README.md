# MCP (Multi-turn Conversation Protocol) 示例

这个目录包含了使用 **MCP (Multi-turn Conversation Protocol)** 的示例代码，旨在演示如何通过该协议极大地扩展和共享 Agent 的能力。

MCP 允许 Agent 系统实现模块化，你可以：
1.  **作为客户端**：让你的 Agent 连接到外部的、遵循 MCP 协议的服务，从而“即插即用”地获得强大的新能力。
2.  **作为服务端**：将你自己的本地代码（例如，一个或多个工具）包装成一个 MCP 服务，安全、标准地共享给其他 Agent 使用。

## 目录结构

```
mcp/
├── amap/                           # 示例 1: Agent 作为 MCP 客户端，调用外部高德地图服务
│   ├── invoke_gaode_mcp.py
│   ├── mcp_gaode_sample.py
│   └── sample.env
└── local/                          # 示例 2: Agent 作为 MCP 服务端，将本地能力通过MCP暴露出去
    ├── invoke_local_mcp.py
    └── local_mcp_server.py
└── streamablehttp/                 # 示例 3: agent client 和 mcp server 通过 streamable_http 方式连接
    ├── mcp_server.py
    └── mcp_client.py
```

---

## 示例 1: `amap` - Agent 作为 MCP 客户端

这个示例演示了如何让一个本地 Agent 作为客户端，去调用一个（假设存在的）外部高德地图 MCP 服务，从而获得地图查询与规划的能力。

### 文件说明

-   **`mcp_gaode_sample.py`**:
    这是一个基准示例，展示了一个功能完备的 **本地 Agent**。它在本地定义了四个模拟的高德地图 API 函数（如地理编码、周边搜索等），并将它们作为工具直接赋予 Agent。这代表了不使用 MCP，在本地通过 ReAct + Function Calling 实现能力的传统方式。

-   **`invoke_gaode_mcp.py`**:
    这是核心的 MCP 客户端示例。它创建的 Agent 不再自己实现地图工具，而是通过 `MCPToolset` 去连接一个外部的、专业的高德地图 MCP 服务。这展示了 Agent 如何“外挂”一个强大的工具集。

    它演示了三种不同的连接方式：
    -   `stdio`: 通过标准输入/输出连接一个本地启动的 MCP 服务。
    -   `sse`: 通过 Server-Sent Events 连接一个提供流式响应的远端服务。
    -   `streamable_http`: 通过标准的 HTTP 请求连接远端服务。

-   **`sample.env`**:
    配置文件模板。你需要将它重命名为 `.env` 并填入你的高德地图 API Key。

### 如何运行

1.  **配置 API Key**:
    将 `amap/sample.env` 文件重命名为 `amap/.env`，并将其中的 `xxxxx` 替换为你的高德地图 API Key。
    ```
    GAODE_API_KEY="你的高德API_KEY"
    ```

2.  **运行客户端**:
    在终端中执行以下命令，可以通过 `--connection` 参数指定连接方式（默认为 `stdio`）。
    ```bash
    python workshops/session2/mcp/amap/invoke_gaode_mcp.py --connection stdio
    ```
    *注意：由于高德地图官方并未提供公开的 MCP 服务，此示例中的 `sse` 和 `streamable_http` URL 仅为演示格式，无法直接运行。`stdio` 模式会尝试通过 `npx` 启动一个 `@amap/amap-maps-mcp-server`，这也需要相应的环境支持。*

---

## 示例 2: `local` - Agent 作为 MCP 服务端

这个示例反其道而行之，演示了如何将你自己的本地 Python 代码（一个 ADK 工具）包装成一个 MCP 服务，供其他任何兼容 MCP 协议的客户端 Agent 来调用。

### 文件说明

-   **`local_mcp_server.py`**:
    创建了一个 MCP 服务。它将一个本地的 ADK 工具（`load_web_page`，用于加载网页内容）包装起来，并通过 MCP 协议将其能力暴露给外部。它实现了 `list_tools` 和 `call_tool` 两个关键的 MCP 协议接口，并通过 `stdio` 方式提供服务。

-   **`invoke_local_mcp.py`**:
    创建了一个 MCP 客户端 Agent。这个 Agent 的工具就是 `MCPToolset`，它被配置为在需要时自动启动 `local_mcp_server.py` 脚本作为其工具提供方。当 Agent 需要使用 `load_web_page` 工具时，它会通过 MCP 协议与这个后台服务进行通信。该文件还包含了单元测试，以验证整个通信链路的正确性。

### 如何运行

`invoke_local_mcp.py` 脚本本身就是一个测试运行器。它会自动在后台启动 `local_mcp_server.py`。

在终端中执行以下命令来运行测试：
```bash
python workshops/session2/mcp/local/invoke_local_mcp.py
```
你将看到测试结果，表明客户端 Agent 成功地通过 MCP 调用了服务端暴露的 `load_web_page` 工具。

---

## 示例 3: `streamablehttp` - Agent 作为 client 通过 streamable_http 方式，调用 MCP 服务端

### 文件说明

-   **`mcp_server.py`**:
    创建了一个 MCP 服务，并通过 MCP 协议将其能力暴露给外部。为了更直观，它简化了实现，提供了 mock 版本的 `get_city_weather` 工具，并通过 `streamable_http` 方式提供服务。

-   **`mcp_client.py`**:
    创建了一个 Agent。这个 Agent 的工具就是 `MCPToolset`，会通过 streamable_http 方式与 `mcp_server.py` 进行通信。

### 如何运行

`mcp_client.py` 脚本本身就是一个测试运行器。它会自动在后台启动 `mcp_server.py`。

在终端中执行以下命令来运行测试：
```bash
# 在一个终端中运行mcp server，默认会一直运行
python workshops/session2/mcp/streamablehttp/mcp_server.py

# 在另一个终端中运行mcp client，client中的veadk agent会调用mcp server中的get_city_weather工具，完成运行会自动退出
python workshops/session2/mcp/streamablehttp/mcp_client.py
```
你将看到测试结果，表明客户端 Agent 成功地通过 MCP 调用了服务端暴露的 `get_city_weather` 工具。

## 核心价值

通过这两个示例，你可以理解 MCP 在构建复杂 Agent 系统中的核心价值：
-   **能力扩展**: Agent 可以作为客户端，动态地从外部服务获取强大的、专业化的能力。
-   **能力共享**: 你可以将自己的代码或工具作为服务端，通过标准协议，安全、便捷地共享给其他 Agent 使用。

这使得 Agent 的构建不再是“单打独斗”，而是可以像搭积木一样，组合来自不同地方的能力，构建出功能更加强大和复杂的智能应用。