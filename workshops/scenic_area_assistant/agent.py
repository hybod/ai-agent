# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd. and/or its affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging
import os
import sys
from pathlib import Path

from agentkit.apps import AgentkitAgentServerApp
from google.adk.tools.mcp_tool.mcp_toolset import (
    MCPToolset,
    StreamableHTTPConnectionParams,
)

from veadk import Agent
from veadk.knowledgebase.knowledgebase import KnowledgeBase
from veadk.memory.long_term_memory import LongTermMemory
from veadk.memory.short_term_memory import ShortTermMemory
from veadk.tools.builtin_tools.web_search import web_search

# 当前目录
sys.path.append(str(Path(__file__).resolve().parent))
# 上层目录
sys.path.append(str(Path(__file__).resolve().parent.parent))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app_name = "scenic_area_companion"

# 1. 配置短期记忆
short_term_memory = ShortTermMemory(backend="local")

# 2. 配置知识库： Viking 向量数据库
# 如果环境变量未设置，则不启用知识库，避免启动失败
knowledge = None
knowledge_collection_name = os.getenv("DATABASE_VIKING_COLLECTION", "")
tos_bucket_name = os.getenv("DATABASE_TOS_BUCKET", "")
tos_region = os.getenv("DATABASE_TOS_REGION", "")

if knowledge_collection_name and tos_bucket_name and tos_region:
    try:
        knowledge = KnowledgeBase(backend="viking", index=knowledge_collection_name)
        # 从预构建目录加载知识库内容
        knowledge_dir = str(Path(__file__).resolve().parent) + "/knowledgebase_docs"
        if os.path.exists(knowledge_dir):
            success = knowledge.add_from_directory(
                knowledge_dir,
                tos_bucket_name=tos_bucket_name,
            )
            if success:
                logger.info("Knowledgebase loaded successfully.")
            else:
                logger.warning("Failed to load knowledgebase.")
        else:
             logger.warning(f"Knowledgebase directory not found: {knowledge_dir}")
    except Exception as e:
        logger.error(f"Failed to load knowledgebase: {e}")
else:
    logger.warning("Knowledgebase environment variables not set. Skipping Knowledgebase.")


# 3. 配置长期记忆： Viking 向量数据库
long_term_memory = None
memory_collection_name = os.getenv("DATABASE_VIKINGMEM_COLLECTION", "")
if memory_collection_name:
    long_term_memory = LongTermMemory(
        backend="viking",
        top_k=3,
        index=memory_collection_name,
    )
else:
    logger.warning("DATABASE_VIKINGMEM_COLLECTION not set. Long-term memory disabled.")


# 4. 配置 Gaode MCP Server (可选，增强地理位置能力)
amap_tool = None
gaode_mcp_api_key = os.getenv("GAODE_MCP_API_KEY", "")
if gaode_mcp_api_key:
    url = "https://mcp.amap.com/mcp?key={}".format(gaode_mcp_api_key)
    amap_tool = MCPToolset(
        connection_params=StreamableHTTPConnectionParams(
            timeout=30,
            url=url,
        ),
    )
else:
    logger.warning("GAODE_MCP_API_KEY not set. Amap tool disabled.")

# 5. 配置智能体 Prompt
companion_prompt = """
你是一个“伴游AI助手”，为游客在景区旅游的“游前/游中/游后”全流程提供个性化智能服务。

## 角色与目标
**身份**：专业、可信、贴心的旅行伴侣与导览解说员。
**目标**：
- **游前**：门票/酒店/伴手礼预订导购 + 路线规划（含人流热度识别）。
- **游中**：实时导览、语音讲解、路线伴游、客服问答。
- **游后**：旅行日志分享 + 基于步数/卡路里/时长的游历总结报告。

## 能力与工具
1. **Web Search (web_search)**：
   - 查询动态信息（价格库存、开放时间、公告、天气、客流、交通、优惠）。
   - **优先引用官方来源**；非官方来源需标注“待核实”。
2. **记忆库 (long_term_memory)**：
   - 存储并应用用户偏好（预算、同伴类型、餐饮、步速体能、语言风格、打卡偏好）。
   - 支持用户随时清除记忆。
3. **LBS地理信息 (amap_tool)** (如果可用)：
   - 用于获取精确的位置、路线、交通状况和周边设施信息。
4. **知识库 (knowledgebase)** (如果可用)：
   - 包含景区通用知识、安全须知等。

## 交互原则
- **语气**：专业友好、结构清晰。
- **输出规范**：必须包含“下一步行动”建议与信息的“官方核验路径”。
- **澄清机制**：如果信息不足，最多提问3次进行澄清。结合记忆库提供默认值建议（如日期与城市、同伴与预算、避人群与步行强度）。

## 工作流程

### 游前阶段
1. **获取偏好与约束**：询问日期、预算、同伴（亲子/情侣/老人）、餐饮喜好、体能状况、交通方式、是否避开人群。
2. **信息检索**：搜索门票、酒店、伴手礼的实时价格/库存，查询人流预测和天气预报。
3. **路线规划**：输出2–3个备选方案（如：省钱版、舒适版、亲子版）。
   - 对比维度：价格、总时长、换乘次数、潜在风险点。

### 游中阶段
1. **实时导览与改道**：根据当前位置、拥挤度、临时关闭通知或排队时长，动态调整路线。
2. **语音讲解脚本**：生成适合语音播放的讲解词（故事/人文/科普/亲子风格），每段控制在1–3分钟阅读时长，并提供延伸阅读链接。
3. **伴游导航与提醒**：主动提醒补水、休息、最佳拍照/打卡点、无障碍设施/母婴室/厕所位置。
4. **风险提醒**：针对人流拥堵、天气突变、交通管制等发布预警，并提供就近替代点与跳转方案。

### 游后阶段
1. **社媒分享模板**：生成适合朋友圈/小红书的图文结构化文案。
2. **游历总结报告**：
   - 估算总步数、总时长、消耗卡路里。
   - 列出热门打卡点及停留最长点。
   - 预算复盘（如果用户提供了预算）。
   - 下次游玩优化建议。

## 核心行为准则
1. **安全第一**：所有路线和建议必须考虑安全性。
2. **实事求是**：工具无法获取的信息明确告知，不臆造。
3. **个性化**：充分利用长期记忆中的用户偏好。
"""

# 支持用户在runtime修改模型
model_name = os.getenv("MODEL_AGENT_NAME", "ep-20260112221629-hl7m4")

tools = [web_search]
if amap_tool:
    tools.append(amap_tool)

agent = Agent(
    name="scenic_area_companion",
    model_name=model_name,
    instruction=companion_prompt,
    tools=tools,
    long_term_memory=long_term_memory,
    knowledgebase=knowledge,
)

agent_server_app = AgentkitAgentServerApp(
    agent=agent,
    short_term_memory=short_term_memory,
)

if __name__ == "__main__":
    logger.info("Starting Scenic Area Companion Agent Server...")
    agent_server_app.run(host="0.0.0.0", port=8000)
