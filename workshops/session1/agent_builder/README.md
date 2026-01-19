# 低代码agent

提供基于 VeADK 的多个低代码 agent sample。

### 项目结构

```bash
/agent-builder/
├── basic_agent # 最基础的single agent
│   ├── __init__.py
│   ├── agent.py # 基于配置文件构建single agent的代码
│   ├── agent.yaml # single agent配置文件
├── builtintools_agent # single agent使用veadk builtin tools
│   ├── __init__.py
│   ├── agent.py
│   ├── agent.yaml
├── customtools_agent # single agent使用自定义tools
│   ├── __init__.py
│   ├── agent.py
│   ├── agent.yaml
│   ├── tools.py # 自定义tools代码
├── multi_agents # multi agents
│   ├── __init__.py
│   ├── agent.py
│   ├── agent.yaml
└── config.yaml # 配置文件 (需要用户复制config.yaml.example并更名为config.yaml，填写api_key和aksk)
└── config.yaml.example # 配置文件示例
└── main.py # 终端方式启动项目
```

## 快速开始

### 依赖

- VeADK 0.2.14 及以上版本
- Python 3.12 及以上版本
  
### 启动

**安装必需依赖：**

```bash
# Clone this repository.
git clone git@code.byted.org:data/agent_workshop.git
cd agent_workshop/workshops/session1/agent_builder
# Install the package and dependencies.
uv venv --python 3.12
source .venv/bin/activate
uv sync

# 复制config.yaml.example并更名为config.yaml，填写api_key和aksk

```

**启动项目：**

```bash
cd agent_workshop/workshops/session1/agent_builder
# 启动veadk web在浏览器选择agent，运行调试
veadk web

or

# 在终端运行全部agent
python main.py
```

## Support

- [VeADK 文档](https://volcengine.github.io/veadk-python/)
