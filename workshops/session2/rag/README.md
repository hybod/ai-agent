# rag agent

rag agent demo based on VeADK

### 项目结构

```bash
/rag/
├── opensearch_rag.py # 基于opensearch的rag demo
├── viking_rag.py # 基于viking db的rag demo
```

## 快速开始

### 依赖

- VeADK 0.2.14 及以上版本
- Python 3.12 及以上版本

### 启动

**开通与创建资源：**
详情可参考文档：https://bytedance.larkoffice.com/docx/ReW7dmAQXop3K4xvrcRcmfOknEb
for viking知识库
1. [必须] 开通viking知识库
2. [必须] 创建viking知识库/collection
3. [必须] 开通tos (viking知识库需要将本地文件上传到tos，然后上传到viking知识库，因此需要开通tos)

for opensearch知识库
1. [必须] 开通opensearch
2. [必须] 创建opensearch实例，获取必要信息，

**修改配置文件：**
复制config.yaml.example并更名为config.yaml，填写api_key和aksk
Note：如果只调用方舟模型，仅填写api_key即可。如果要使用Viking知识库，需要填写aksk。如果需要opensearch知识库，需要填写opensearch的host、port、username、password等信息

**安装依赖：**
```bash
# Clone this repository.
git clone git@code.byted.org:data/agent_workshop.git
cd agent_workshop/workshops/session2/rag/
# Install the package and dependencies.
uv venv --python 3.12
source .venv/bin/activate
uv sync

```

**启动项目：**

```bash
cd rag
# 启动opensearch rag demo
python opensearch_rag.py
# 启动viking rag demo
python viking_rag.py
```

## Support

- [VeADK 文档](https://volcengine.github.io/veadk-python/)
