# Session 4: Agent-to-Agent (A2A) 通信与部署

本目录包含 Agent-to-Agent (A2A) 通信和部署相关的实践项目，涵盖了从基础A2A通信到实际部署的完整流程。

## 项目结构

```
session4/
├── basic_a2a/           # 基础A2A通信示例
├── deploy_a2a/          # A2A部署实践
├── eposide_generation/  # 剧集生成（图像+视频）
├── mcp_amap/           # 高德地图MCP集成
└── pyproject.toml      # Python项目配置
```

## 项目详情

### 1. basic_a2a - 基础A2A通信

**功能描述**: 演示基础的Agent-to-Agent通信模式，包含客户端和服务器端实现。

**项目结构**:
```
basic_a2a/
├── client/
│   └── client.py          # 客户端代码
└── server/
    ├── server.py          # 服务器端代码
    └── start.sh           # 启动脚本
```

**核心功能**:
- 天气查询Agent服务端
- 远程Agent调用客户端
- 本地HTTP服务器部署

**使用方法**:
1. 启动服务器端：`cd server && ./start.sh`
2. 运行客户端：`cd client && python client.py`

### 2. deploy_a2a - A2A部署实践

**功能描述**: 展示如何将A2A服务部署到生产环境，包含多种客户端实现。

**项目结构**:
```
deploy_a2a/
├── client_code/
│   ├── client.py          # 标准客户端
│   └── remote_agent.py    # 远程Agent调用
├── client_web/
│   └── agent.py           # Web客户端
└── server/
    ├── agent.py           # 服务器端Agent
    └── deploy.sh          # 部署脚本
```

**核心功能**:
- 生产环境部署配置
- 多类型客户端支持
- 认证和授权机制

**部署方法**（补全 `deploy.sh` 文件中的变量）:
```bash
cd server
./deploy.sh
```

### 3. eposide_generation - 剧集生成

**功能描述**: 基于A2A架构的图像和视频生成系统，能够根据文本描述生成剧集内容。

**项目结构**:
```
eposide_generation/
├── agent.py               # 主Agent协调器
├── image_generator.py     # 图像生成Agent
├── video_generator.py     # 视频生成Agent
├── start_image_generator.sh
└── start_video_generator.sh
```

**核心功能**:
- 多模态内容生成（图像+视频）
- Agent协作工作流
- 网络搜索增强提示词

**启动方法**:
1. 启动图像生成服务：`./start_image_generator.sh`
2. 启动视频生成服务：`./start_video_generator.sh`
3. 运行主Agent：`python agent.py`

### 4. mcp_amap - 高德地图MCP集成

**功能描述**: 集成高德地图MCP服务的酒店查找智能体，本服务需要提供高德 API Key。

**项目结构**:
```
mcp_amap/
├── agent.py               # 酒店查找Agent
└── __init__.py
```

**核心功能**:
- 高德地图MCP服务集成
- 酒店信息查询
- 地理位置服务

**环境配置**:
需要设置 `GAODE_MCP_API_KEY` 环境变量

## 技术栈

- **框架**: Veadk (字节跳动自研Agent框架)
- **通信**: A2A (Agent-to-Agent) 协议
- **部署**: Vefaas 平台
- **工具**: 内置工具集（天气查询、图像生成、视频生成等）
- **集成**: MCP (Model Context Protocol) 协议

## 快速开始

### 环境要求

- Python 3.12+
- veadk-python
- Veadk 框架
- 相关API密钥（如高德地图API）

### 安装依赖

```bash
pip install -e .
```

### 运行示例

1. **基础A2A通信**
```bash
cd basic_a2a/server
./start.sh
# 新开终端
cd basic_a2a/client
python client.py
```

2. **剧集生成**
```bash
cd eposide_generation
./start_image_generator.sh
./start_video_generator.sh
python agent.py
```

## 项目特点

1. **模块化设计**: 每个项目独立，便于学习和测试
2. **生产就绪**: 包含完整的部署配置
3. **实际应用**: 基于真实业务场景
4. **扩展性强**: 易于添加新的Agent和功能

## 学习路径建议

1. 从 `basic_a2a` 开始，理解A2A基础概念
2. 学习 `eposide_generation`，掌握多Agent协作
3. 实践 `deploy_a2a`，了解生产部署
4. 探索 `mcp_amap`，学习第三方服务集成
