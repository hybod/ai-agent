# A2A Simple 示例项目

## 项目概述

A2A Simple 是一个基于 VEADK 和 A2A (Agent-to-Agent) 协议的简单示例项目，展示了如何构建和部署一个支持骰子投掷和质数检查功能的智能代理。该项目包含本地客户端和远程代理服务，演示了 A2A 协议的基本使用方式。

## 项目结构

```
a2a_simple/
├── __init__.py              # 包初始化文件
├── agent.py                 # 本地代理配置（RemoteVeAgent）
├── local_client.py          # 本地客户端实现
├── remote_client/           # 远程代理服务
│   ├── __init__.py
│   └── agent.py            # 远程代理核心实现
├── requirements.txt         # 依赖包列表
└── README.md               # 本文件
```

## 核心组件说明

### 1. 远程代理 (remote_client/agent.py)

远程代理是项目的核心，提供以下功能：

#### 工具函数
- **roll_die(sides: int, tool_context: ToolContext) -> int**
  - 功能：投掷指定面数的骰子
  - 参数：sides - 骰子面数，tool_context - 工具上下文
  - 返回值：随机生成的骰子点数（1到sides之间）
  - 特性：记录每次投掷结果到工具状态中

- **check_prime(nums: list[int]) -> str**
  - 功能：检查数字列表中的质数
  - 参数：nums - 需要检查的数字列表
  - 返回值：质数检查结果的字符串描述

#### 代理配置
代理使用 VEADK 框架配置，具有以下特性：
- 名称：hello_world_agent
- 描述：能够投掷8面骰子并检查质数的简单代理
- 端口：8001

#### 提示词指令
代理遵循严格的指令流程：
1. 当要求投掷骰子时，必须调用 roll_die 工具
2. 获取投掷结果后，才能调用 check_prime 工具检查质数
3. 支持并行调用多个工具
4. 可以讨论之前的投掷结果
5. 严格遵守参数类型要求（整数而非字符串）

### 2. 本地客户端 (local_client.py)

本地客户端实现了 A2A 协议的客户端功能：

#### 核心类：A2ASimpleClient
- **功能**：与远程 A2A 代理进行通信
- **特性**：
  - 支持缓存代理卡片信息
  - 配置超时设置（默认240秒）
  - 支持 JSON-RPC 和 HTTP-JSON 传输协议

#### 主要方法
- **create_task(agent_url: str, message: str) -> str**
  - 功能：向指定代理发送消息并获取响应
  - 流程：
    1. 获取代理卡片信息
    2. 创建 A2A 客户端
    3. 发送消息并收集响应
    4. 解析并返回结果

### 3. 本地代理配置 (agent.py)

配置本地 RemoteVeAgent，连接到远程代理服务：
- 代理名称：a2a_agent
- 远程地址：http://localhost:8001/

## 快速开始

### 启动远程代理服务
```bash
# 在 a2a_simple 目录下执行
uvicorn remote.agent:a2a_app --host localhost --port 8001
```

### 验证代理服务
打开浏览器访问：`http://localhost:8001/.well-known/agent-card.json`

应该看到类似以下的响应：
```json
{
  "name": "hello_world_agent",
  "description": "hello world agent that can roll a dice of 8 sides and check prime numbers.",
  "instruction": "...",
  "tools": [
    {
      "name": "roll_die",
      "description": "Roll a die and return the rolled result.",
      "parameters": {
        "sides": {
          "type": "integer",
          "description": "The integer number of sides the die has."
        }
      }
    },
    {
      "name": "check_prime",
      "description": "Check if a given list of numbers are prime.",
      "parameters": {
        "nums": {
          "type": "array",
          "items": {
            "type": "integer"
          },
          "description": "The list of numbers to check."
        }
      }
    }
  ]
}
```

### 测试客户端
```bash
python local_client.py
```

### A2A 访问案例
在 samples 目录下面运行命令打开操作窗口，访问 `http://localhost:8001` 即可查看代理的操作界面。
```bash
adk web
```

## 使用示例

### 测试场景表格

| 测试场景 | 发送消息示例 | 代理行为 | 预期结果 |
|---------|-------------|----------|----------|
| **基本投掷** | `"hello , show me one number"` | 1. 投掷一个骰子<br>2. 检查结果是否为质数 | 返回单个数字的投掷结果和质数检查 |
| **批量测试（10个数）** | `"请投掷10次骰子并统计结果"` | 1. 连续投掷10次<br>2. 统计各数字出现频率<br>3. 检查所有质数 | 返回频率分布和质数统计 |
| **概率统计（20个数）** | `"投掷20次骰子，分析概率分布"` | 1. 投掷20次记录结果<br>2. 计算各面概率<br>3. 质数出现频率分析 | 概率分布图表和统计报告 |
| **指定面数** | `"请投掷一个12面的骰子"` | 1. 使用指定面数投掷<br>2. 检查结果是否为质数 | 返回12面骰子的投掷结果 |
| **历史记录查询** | `"查看之前的投掷记录"` | 1. 从工具状态获取历史<br>2. 显示所有投掷结果<br>3. 分析历史质数分布 | 历史投掷记录和统计 |
| **质数验证** | `"检查数字[2,3,5,7,11]是否为质数"` | 1. 直接调用质数检查工具<br>2. 验证给定数字列表 | 质数验证结果报告 |

### 自定义交互示例

您可以修改 local_client.py 中的测试函数，实现上述场景：

```python
async def comprehensive_test():
    # 场景1: 基本投掷
    result1 = await a2a_client.create_task(
        "http://localhost:8001", 
        "hello , show me one number"
    )
    print("基本投掷结果:", result1)
    
    # 场景2: 批量测试10个数
    result2 = await a2a_client.create_task(
        "http://localhost:8001", 
        "请投掷10次骰子并统计结果"
    )
    print("\n批量测试结果:", result2)
    
    # 场景3: 概率统计20个数
    result3 = await a2a_client.create_task(
        "http://localhost:8001", 
        "投掷20次骰子，分析概率分布"
    )
    print("\n概率统计结果:", result3)
    
    # 场景4: 指定面数测试
    result4 = await a2a_client.create_task(
        "http://localhost:8001", 
        "请投掷一个12面的骰子"
    )
    print("\n指定面数结果:", result4)
    
    # 场景5: 历史记录查询
    result5 = await a2a_client.create_task(
        "http://localhost:8001", 
        "查看之前的投掷记录"
    )
    print("\n历史记录:", result5)
    
    # 场景6: 质数验证
    result6 = await a2a_client.create_task(
        "http://localhost:8001", 
        "检查数字[2,3,5,7,11]是否为质数"
    )
    print("\n质数验证:", result6)
```


## 工作原理详解

### A2A 协议流程
1. **服务发现**：客户端通过 `.well-known/agent-card.json` 端点获取代理能力信息
2. **能力协商**：客户端根据代理卡片选择支持的传输协议
3. **消息传输**：使用 JSON-RPC 或 HTTP-JSON 协议发送消息
4. **工具调用**：代理根据指令调用相应的工具函数
5. **结果返回**：代理将工具执行结果返回给客户端

### 工具调用机制
- **状态管理**：roll_die 工具使用 ToolContext 维护投掷历史记录
- **类型安全**：严格检查参数类型，确保整数参数的正确传递
- **错误处理**：包含完整的异常处理机制

## 配置说明

### 安全设置
代理配置了安全设置，禁用了骰子投掷相关的危险内容检测：
```python
safety_settings=[
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=types.HarmBlockThreshold.OFF,
    ),
]
```

### 超时配置
客户端默认超时时间为240秒，可根据需要调整：
```python
a2a_client = A2ASimpleClient(default_timeout=300.0)  # 5分钟超时
```
