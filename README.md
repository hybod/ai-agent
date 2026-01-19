# Introductions

通过工作坊的系列培训，让行解、产解、产品等团队通过全流程动手实际操作结合一定的理论和最佳实践，具备从零到一构建企业级 AI Agent 的实战能力。完成系列培训后你将掌握从 Agent 设计、开发、部署、运维到持续评估与优化的完整技能体系。

## 具体内容
全部计划表参考： https://bytedance.larkoffice.com/wiki/BLTjwiDm3iJW6pkD84qcfQlJnhc?from=from_parent_docx 包括环境安装和设置，需要先完成环境安装和设置才能进行下面的课程。
### 快速落地化
通过 AI IDE Trae 和火山的 Agent SDK VeADK 帮助大家快速将 AI Agent 落地化，实现 Vibe 编程，每个人都可以完成基础的 Agent 开发加速进阶。

### 能力跃迁
通过集成和使用 Agentkit 将 AI Agent 实现从 Research 到 Production-Ready 的能力跃迁。

### 最佳实践闭环
形成面向真实客户场景的最佳实践闭环，加速 AI 从试点到规模化应用的落地。

### 共建生态
共建构建完善的样例库和需求，促进知识共享和持续创新。


## 第一课内容
https://bytedance.larkoffice.com/wiki/WEAawzqSdirJUnkR6FfcVzxenzg
### 课程简介
专注于基本概念和快速上手，适合刚接触Agent开发者；相关功能配置简单，能快速验证想法。

### 学习目标
- 清晰掌握 AI Agent 基本概念（定义、应用场景）、核心组件（记忆模块、工具调用层、决策引擎等）
- 了解各组件与火山引擎产品的对应关系（如记忆组件对应火山 "向量数据库"、工具调用对应 "函数服务"）
- 通过AI IDE 一起Vibe 编程来实现一些简单的Agent开发来调用工具

## 第二课内容
https://bytedance.larkoffice.com/wiki/YgkuwNa4JiYdpskMJlcc89CInod


### 依赖

- VeADK 0.2.14 及以上版本
- Python 3.12 及以上版本

### 启动

**安装必需依赖：**

```bash
# Clone this repository.
git clone git@code.byted.org:data/agent_workshop.git

# 可以在任意目录，运行如下命令安装依赖
uv venv --python 3.12
source .venv/bin/activate
uv sync

# 复制config.yaml.example并更名为config.yaml，填写api_key和aksk
# Note：如果只调用方舟模型，仅填写api_key即可。如果要使用Viking DB、web_search、trace、TOS等能力，需要填写aksk

# 也可以进入对应项目目录即可，如agent_demo、agent_build等，安装依赖/运行项目，详情可以参考目录下的README.md
cd agent_workshop/workshops/session1/agent_demo/

```

### AI Agent 开发的关键FAQ


