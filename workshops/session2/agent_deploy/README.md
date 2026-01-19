# agent demo

agent deploy

### 项目结构

```bash
/agent_deploy/
├── veadk_web_agent/
│   ├── __init__.py
│   ├── agent.py # 定义veadk web agent，这个agent可以生图/生视频
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
cd agent_workshop/workshops/session2/agent_deploy/
# Install the package and dependencies.
uv venv --python 3.12
source .venv/bin/activate
uv sync

# 复制config.yaml.example并更名为config.yaml，填写api_key和aksk
# Note：如果只调用方舟模型，仅填写api_key即可。如果要使用Viking DB、web_search、trace、TOS等能力，需要填写aksk

```

### 部署
```bash
cd agent_workshop/workshops/session2/agent_deploy/veadk_web_agent/
veadk deploy --access-key YOUR_AK --secret-key YOUR_SK --vefaas-app-name=youragentname --use-adk-web
# 运行后，可能需要等待几分钟，等APIG、VeFaaS等环节部署完成
# Note：--vefaas-app-name，命名规则为，不包含_，不包含大写字母
# 如果想指定apig网关，可以增加如下参数 --veapig-instance-name=YOUR_APIG_NAME
```
也可参考如下文档
https://bytedance.larkoffice.com/docx/O5fsdZwDjoGgSexludUcdSOonMe

**启动项目：**

```bash
# for veadk_web_agent
cd agent_workshop/workshops/session2/agent_demo/
veadk web # 在http://127.0.0.1:8000界面，选择veadk_web_agent这个agent，即可调试
```

## Support

- [VeADK 文档](https://volcengine.github.io/veadk-python/)
