# agent demo

agent demo based on VeADK

### 项目结构

```bash
/agent_demo/
├── terminal_agent/ # 终端方式运行agent的代码
│   ├── basic_agent.py # 基础agent
│   ├── tool_agent.py # 工具agent，定义tools供agent调用
│   ├── short_mem_local_agent.py # 短期记忆agent，agent会话具备短期记忆能力。短期记忆在本地内存，agent结束运行数据清除
│   ├── short_mem_mysql_agent.py # 短期记忆agent，agent会话具备短期记忆能力。短期记忆存储在云上mysql，agent结束运行再次运行数据不清除
│   ├── long_mem_viking_agent.py # 长期记忆agent，agent会话具备长期记忆能力。长期记忆存储在云上viking记忆库，agent不同session均可访问，agent结束运行再次运行数据不清除
│   ├── long_mem_opensearch_agent.py # 长期记忆agent，agent会话具备长期记忆能力。长期记忆存储在云上opensearch，agent不同session均可访问，agent结束运行再次运行数据不清除
│   ├── sub_agent.py # 子agent，多个子agent供root agent调用
├── veadk_web_agent/
│   ├── __init__.py
│   ├── agent.py # 定义veadk web agent，这个agent可以生图/生视频
├── main.py # 终端方式启动veadk web agent，实现生图/生视频
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
cd agent_workshop/workshops/session1/agent_demo/
# Install the package and dependencies.
uv venv --python 3.12
source .venv/bin/activate
uv sync

# 复制config.yaml.example并更名为config.yaml，填写api_key和aksk
# Note：如果只调用方舟模型，仅填写api_key即可。如果要使用Viking DB、web_search、trace、TOS等能力，需要填写aksk

```

**启动项目：**

```bash
# for veadk_web_agent
cd agent_workshop/workshops/session1/agent_demo/
veadk web # 在http://127.0.0.1:8000界面，选择veadk_web_agent这个agent，即可调试
# or
cd agent_workshop/workshops/session1/agent_demo/
python main.py # or uv run main.py

# for basic_agent, session_agent, builtintools_agent, customtools_agent, multi_agent
cd agent_workshop/workshops/session1/agent_demo/terminal_agent/
python basic_agent.py # or uv run basic_agent.py
```

## Support

- [VeADK 文档](https://volcengine.github.io/veadk-python/)
