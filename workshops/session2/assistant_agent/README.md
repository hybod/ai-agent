# assistant agent

assistant agent demo based on VeADK

### 项目结构

```bash
/assistant_agent/
├── sub_agents/ # 子agent代码目录
│   ├── __init__.py
│   ├── loop_agent.py # 循环agent，供主agent调用
│   ├── parallel_agent.py # 并行agent，供主agent调用
│   ├── sequential_agent.py # 顺序agent，供主agent调用
├── agent.py # 主agent，支持veadk web运行
├── prompts.py # 定义prompt模板
├── main.py # 主程序，支持terminal运行
```

<img src="./doc/architecture.jpeg" alt="assistant_agent" width="50%">

## 快速开始

### 依赖

- VeADK 0.2.14 及以上版本
- Python 3.12 及以上版本

### 启动

**安装必需依赖：**

```bash
# Clone this repository.
git clone git@code.byted.org:data/agent_workshop.git
cd agent_workshop/workshops/session2/assistant_agent/
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
cd agent_workshop/workshops/session2/
veadk web # 在http://127.0.0.1:8000界面，选择assistant_agent这个agent，即可调试
# or terminal
cd agent_workshop/workshops/session2/
python assistant_agent/main.py # or uv run main.py
```

## Support

- [VeADK 文档](https://volcengine.github.io/veadk-python/)
