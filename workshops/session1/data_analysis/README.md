# agent demo

data-analysis agent based on VeADK

### 项目结构

```bash
/data_analysis/
├── agent.py # agent代码
└── config.yaml # 配置文件 (需要用户复制config.yaml.example并更名为config.yaml，填写api_key和aksk)
└── config.yaml.example # 配置文件示例
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
cd agent_workshop/workshops/session1/data_analysis/
# Install the package and dependencies.
uv venv --python 3.12
source .venv/bin/activate
uv sync

# 复制config.yaml.example并更名为config.yaml，填写api_key、aksk、las、browser use、code use、opensearch等配置。可参考如下链接：

# browser_use: https://www.volcengine.com/mcp-marketplace/detail?name=Browser-Use%20MCP
# coder_use: https://www.volcengine.com/mcp-marketplace/detail?name=Code-Sandbox%20MCP
# las: https://www.volcengine.com/mcp-marketplace/detail?name=LAS%20MCP
# opensearch: https://www.volcengine.com/docs/6465/?lang=zh
```

**启动项目：**

```bash
cd agent_workshop/workshops/session1/
veadk web --log_level ERROR # 在http://127.0.0.1:8000界面，选择data_analysis这个agent，即可调试
```

## Support

- [VeADK 文档](https://volcengine.github.io/veadk-python/)
