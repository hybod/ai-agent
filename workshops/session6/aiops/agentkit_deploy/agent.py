import os

from google.adk.planners import BuiltInPlanner
from google.adk.planners import PlanReActPlanner
from google.adk.tools.mcp_tool.mcp_toolset import (
    StreamableHTTPConnectionParams,
)
from google.genai import types
from veadk import Agent
from veadk.a2a.remote_ve_agent import RemoteVeAgent
from veadk.config import getenv
from veadk.knowledgebase.knowledgebase import KnowledgeBase
from veadk.memory.long_term_memory import LongTermMemory
from veadk.memory.short_term_memory import ShortTermMemory
from veadk.integrations.ve_identity import (
    VeIdentityMcpToolset,
    IdentityClient,
    oauth2_auth,
    AuthRequestProcessor,
)
from veadk.config import settings


from agentkit.apps import AgentkitAgentServerApp

short_term_memory = ShortTermMemory(backend="local")

# long_term_memory = LongTermMemory(backend="local")
# Knowledgebase usage
# Required env vars for viking knowledgebase
# Local VOLCENGINE_ACCESS_KEY, VOLCENGINE_ACCESS_KEY,
# Clooud: ServiceRole with VikingdbFullAccess permission
my_ops_knowledge_collection = os.getenv(
    "DATABASE_VIKING_COLLECTION", "my_ops_collection"
)
knowledgebase = KnowledgeBase(backend="viking", index=my_ops_knowledge_collection)
### depend on database_tos realated configuration for import knowledgebase
knowledgebase.add_from_files(files=["./sop_aiops.md"])
# knowledgebase.add_from_files(files=["https://aaa-bbb-ccc-ddd.tos-cn-beijing.volces.com/agentkit/travel_qa.md"])
# restrict user to access this knowledgebase
my_sec_knowledge_collection = os.getenv(
    "DATABASE_VIKING_COLLECTION", "my_sec_collection"
)
knowledgebase_sec = KnowledgeBase(backend="viking", index=my_sec_knowledge_collection)
knowledgebase_sec.add_from_files(files=["./sop_sec.md"])

my_database_knowledge_collection = os.getenv(
    "DATABASE_VIKING_COLLECTION", "my_database_collection"
)
knowledgebase_database = KnowledgeBase(
    backend="viking", index=my_database_knowledge_collection
)
knowledgebase_database.add_from_files(files=["./sop_database.md"])


# LTM Memory usage for memorybase/mem0
# backend = os.getenv("LONG_TERM_MEMORY_BACKEND", "mem0")
### Required env vars for memorybase
# DATABASE_MEM0_BASE_URL=<url of mem0>
# DATABASE_MEM0_API_KEY=<apikey of mem0>
# long_term_memory_mem0 = LongTermMemory(
#         backend="mem0",
#         top_k=3,
#         app_name="my_app_name",
#     )


### Required env vars for VikingDB Memory
# DATABASE_VIKINGMEM_COLLECTION=<collection_name> #index

my_memory_collection = os.getenv(
    "DATABASE_VIKINGMEM_COLLECTION", "default_memory_collection"
)
long_term_memory = LongTermMemory(
    backend="viking",
    top_k=3,
    index=my_memory_collection,
)

remote_security_agent = RemoteVeAgent(
    name="remote_security_agent",
    # instruction="你是一个旅行规划顾问，负责旅行规划。",
    url="https://sd46699mfog2gt9o8rfu0.apigateway-cn-beijing.volceapi.com",  # <--- url from cloud platform
)


identity_client = IdentityClient(region=settings.veidentity.region)

mcp_security = VeIdentityMcpToolset(
    auth_config=oauth2_auth(
        provider_name="sec-agent-oauth-provider",
        auth_flow="USER_FEDERATION",
        identity_client=identity_client,
    ),
    connection_params=StreamableHTTPConnectionParams(
        url=getenv("SECURITY_MCP_URL", "https://sec-agent.mcp.volcbiz.com/mcp"),
        timeout=30.0,
    ),
)

# 创建 RDS MySQL MCP Tool
mcp_rds_mysql = VeIdentityMcpToolset(
    auth_config=oauth2_auth(
        provider_name="rds-mysql-oauth-provider",
        auth_flow="USER_FEDERATION",
        identity_client=identity_client,
    ),
    connection_params=StreamableHTTPConnectionParams(
        url=getenv("RDS_MYSQL_MCP_URL", "https://rds-mysql.mcp.volcbiz.com/mcp"),
        timeout=30.0,
    ),
)

# 创建 TLS MCP Tool
mcp_tls = VeIdentityMcpToolset(
    auth_config=oauth2_auth(
        provider_name="tls-oauth-provider",
        auth_flow="USER_FEDERATION",
        identity_client=identity_client,
    ),
    connection_params=StreamableHTTPConnectionParams(
        url=getenv("TLS_MCP_URL", "https://tls.mcp.volcbiz.com/mcp"),
        timeout=30.0,
    ),
)

# 创建 VMP MCP Tool
mcp_vmp = VeIdentityMcpToolset(
    auth_config=oauth2_auth(
        provider_name="vmp-oauth-provider",
        auth_flow="USER_FEDERATION",
        identity_client=identity_client,
    ),
    connection_params=StreamableHTTPConnectionParams(
        url=getenv("VMP_MCP_URL", "https://vmp.mcp.volcbiz.com/mcp"),
        timeout=30.0,
    ),
)

# 创建 ECS Cloud Assistant MCP Tool
mcp_ecs_cloud_assistant = VeIdentityMcpToolset(
    auth_config=oauth2_auth(
        provider_name="ecs-oauth-provider",
        auth_flow="USER_FEDERATION",
        identity_client=identity_client,
    ),
    connection_params=StreamableHTTPConnectionParams(
        url=getenv(
            "ECS_CLOUD_ASSISTANT_MCP_URL",
            "https://ecs.mcp.volcbiz.com/cloud_assistant/mcp",
        ),
        timeout=30.0,
    ),
)

# 创建 ECS MCP Tool
mcp_ecs = VeIdentityMcpToolset(
    auth_config=oauth2_auth(
        provider_name="ecs-oauth-provider",
        auth_flow="USER_FEDERATION",
        identity_client=identity_client,
    ),
    connection_params=StreamableHTTPConnectionParams(
        url=getenv("ECS_MCP_URL", "https://ecs.mcp.volcbiz.com/ecs/mcp"),
        timeout=30.0,
    ),
)

# 创建 APMPlus MCP Tool
mcp_apmplus = VeIdentityMcpToolset(
    auth_config=oauth2_auth(
        provider_name="apmplus-oauth-provider",
        auth_flow="USER_FEDERATION",
        identity_client=identity_client,
    ),
    connection_params=StreamableHTTPConnectionParams(
        url=getenv("APMPULS_MCP_URL", "https://apmplus.mcp.volcbiz.com/mcp"),
        timeout=30.0,
    ),
)

# 创建独立的 RDS MySQL Agent
rds_mysql_agent: Agent = Agent(
    name="rds_mysql_agent",
    model_name="deepseek-v3-1-250821",
    description="RDS MySQL 运维智能体",
    instruction="你是一个 RDS MySQL 数据库运维专家",
    knowledgebase=knowledgebase_database,
    tools=[mcp_rds_mysql],
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
            thinking_budget=1024,
        )
    ),
    run_processor=AuthRequestProcessor(),
)

# 创建独立的 TLS Agent
tls_agent: Agent = Agent(
    name="tls_agent",
    model_name="deepseek-v3-1-250821",
    description="TLS 运维智能体",
    instruction="你是一个 TLS 证书运维专家",
    tools=[mcp_tls],
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
            thinking_budget=1024,
        )
    ),
    run_processor=AuthRequestProcessor(),
)

# 创建独立的 VMP Agent
vmp_agent: Agent = Agent(
    name="vmp_agent",
    model_name="deepseek-v3-1-250821",
    description="VMP 运维智能体",
    instruction="你是一个 VMP 监控运维专家",
    tools=[mcp_vmp],
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
            thinking_budget=1024,
        )
    ),
    run_processor=AuthRequestProcessor(),
)

# 创建独立的 ECS Cloud Assistant Agent
ecs_cloud_assistant_agent: Agent = Agent(
    name="ecs_cloud_assistant_agent",
    model_name="deepseek-v3-1-250821",
    description="ECS Cloud Assistant 运维智能体",
    instruction="你是一个 ECS Cloud Assistant 运维专家",
    tools=[mcp_ecs_cloud_assistant],
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
            thinking_budget=1024,
        )
    ),
    run_processor=AuthRequestProcessor(),
)

# 创建独立的 ECS Agent
ecs_agent: Agent = Agent(
    name="ecs_agent",
    model_name="deepseek-v3-1-250821",
    description="ECS 运维智能体",
    instruction="你是一个 ECS 云服务器运维专家",
    tools=[mcp_ecs],
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
            thinking_budget=1024,
        )
    ),
    run_processor=AuthRequestProcessor(),
)

# 创建独立的 APMPlus Agent
apmplus_agent: Agent = Agent(
    name="apmplus_agent",
    model_name="deepseek-v3-1-250821",
    description="APMPlus 运维智能体",
    instruction="你是一个 APMPlus 应用性能监控运维专家",
    tools=[mcp_apmplus],
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
            thinking_budget=1024,
        )
    ),
    run_processor=AuthRequestProcessor(),
)


sec_agent: Agent = Agent(
    name="sec_agent",
    model_name="deepseek-v3-1-250821",
    description="安全运维智能体",
    instruction="你是一个安全运维专家",
    knowledgebase=knowledgebase_sec,
    tools=[mcp_security],
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
            thinking_budget=1024,
        )
    ),
    run_processor=AuthRequestProcessor(),
)

agent = Agent(
    name="ve_ai_ops_agent",
    model_name="deepseek-v3-1-250821",
    description="AIOps agent",
    instruction="你是一个云计算运维专家，一次完整的云服务巡检需要包括TLS-MCP（日志）、VMP-MCP（监控指标）、ECS Assistant（主机诊断）、RDS-MySQL MCP（慢 SQL）、Sec-Agent（安全风险）、APMPlus-MCP（Tracing）",
    planner=PlanReActPlanner(),
    sub_agents=[
        rds_mysql_agent,
        tls_agent,
        vmp_agent,
        ecs_cloud_assistant_agent,
        ecs_agent,
        apmplus_agent,
        sec_agent,
        remote_security_agent,
    ],
    long_term_memory=long_term_memory,
    knowledgebase=knowledgebase,
    run_processor=AuthRequestProcessor(),
)

root_agent = agent


agent_server_app = AgentkitAgentServerApp(
    agent=agent,
    short_term_memory=short_term_memory,
)

if __name__ == "__main__":
    agent_server_app.run(host="0.0.0.0", port=8000)
