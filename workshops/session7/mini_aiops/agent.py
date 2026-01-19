import os

from google.adk.planners import BuiltInPlanner
from google.adk.planners import PlanReActPlanner
from google.adk.tools.mcp_tool.mcp_toolset import (
    StreamableHTTPConnectionParams,
)
from google.genai import types
from veadk import Agent
from veadk.config import getenv
from veadk.knowledgebase.knowledgebase import KnowledgeBase
from veadk.memory.long_term_memory import LongTermMemory
from veadk.memory.short_term_memory import ShortTermMemory
from google.adk.tools.mcp_tool.mcp_toolset import (
    McpToolset,
    MCPToolset,
    StdioServerParameters,
    StdioConnectionParams,
    StreamableHTTPConnectionParams,
)
from google.adk.tools import AgentTool
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams
from veadk.config import settings

from agentkit.apps import AgentkitAgentServerApp

short_term_memory = ShortTermMemory(backend="local")

# long_term_memory = LongTermMemory(backend="local")
# Knowledgebase usage
# Required env vars for viking knowledgebase
# Local VOLCENGINE_ACCESS_KEY, VOLCENGINE_ACCESS_KEY,
# Clooud: ServiceRole with VikingdbFullAccess permission

### Auto create knowledgebase if not exist for aiops
knowledgebase = KnowledgeBase(backend="viking", app_name = "aiops", top_k=3)
### depend on database_tos realated configuration for import knowledgebase
# knowledgebase.add_from_files(files=["sop_aiops.md"])

# restrict user to access this knowledgebase

# knowledgebase.add_from_files(files=["sop_database.md"])
# knowledgebase.add_from_files(files=["sop_sec.md"])


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
### Auto create memory collection if not exist for aiops
my_memory_collection = os.getenv(
    "DATABASE_VIKINGMEM_COLLECTION", "default_memory_collection"
)
long_term_memory = LongTermMemory(
    backend="viking",
    top_k=3,
    app_name="aiops_memory",
    # index=my_memory_collection,rds_mysql_agent
)

###Remote MCP Server with apikey or jwt token
apikey = "1234"
url = "https://sec-agent.mcp.volcbiz.com/mcp?token={}".format(getenv("MCP_API_KEY", apikey))
mcp_sec_remote = McpToolset(
        connection_params=StreamableHTTPConnectionParams(
        url=url,
        headers={"Authorization": f"Bearer {apikey}"}
    ),
)

# 创建本地 MCP Sec Agent Tool
mcp_sec_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="uvx",
            args=[
                "--from",
                "git+https://github.com/volcengine/mcp-server.git#subdirectory=server/mcp_server_sec_agent",
                "mcp-server-sec-agent"
            ],
            env={
                "VOLC_ACCESSKEY": os.getenv("VOLC_ACCESSKEY", "your ak"),
                "VOLC_SECRETKEY": os.getenv("VOLC_SECRETKEY", "your sk"),
            }
        ),
        timeout=180.0
    ),
    errlog=None
)

# 创建本地 MCP RDS MySQL Tool
mcp_rds_mysql_local = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="uvx",
            args=[
                "--from",
                "git+https://github.com/volcengine/mcp-server.git#subdirectory=server/mcp_server_rds_mysql",
                "mcp-server-rds-mysql"
            ],
            env={
                # "VOLCENGINE_ENDPOINT": os.getenv("VOLCENGINE_ENDPOINT", "cloudcontrol.cn-beijing.volcengineapi.com"),
                # "VOLCENGINE_REGION": os.getenv("VOLCENGINE_REGION", "cn-beijing"),
                "VOLCENGINE_ACCESS_KEY": os.getenv("VOLCENGINE_ACCESS_KEY", "your ak"),
                "VOLCENGINE_SECRET_KEY": os.getenv("VOLCENGINE_SECRET_KEY", "your sk")
            }
        ),
        timeout=180.0
    ),
    errlog=None
)


### control center mcp server
server_parameters = StdioServerParameters(
    command="uvx",
    args=[
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_ccapi",
        # "git+https://github.com/volc-sdk-team/mcp-server#subdirectory=server/mcp_server_ccapi",

        "mcp-server-ccapi"
    ],
    env={
        "VOLCENGINE_ACCESS_KEY": os.getenv("VOLCENGINE_ACCESS_KEY", "your ak"),
        "VOLCENGINE_SECRET_KEY": os.getenv("VOLCENGINE_SECRET_KEY", "your sk"),
        # "VOLCENGINE_SESSION_TOKEN": os.getenv("VOLCENGINE_SESSION_TOKEN", "your session token"),
        # "VOLCENGINE_ENDPOINT": "cloudcontrol.cn-beijing.volcengineapi.com",
        # "VOLCENGINE_REGION": "cn-beijing"
    }
)
ccapi_mcp_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=server_parameters,
        timeout=180.0
    ),
    errlog=None
)
# 创建独立的 CCAPI Agent
# Prompt：分析一下tls实例相关风险

ccapi_agent: Agent = Agent(
    name="ccapi_agent",
    # model_name="deepseek-v3-1-250821",
    # model_name="doubao-1-5-pro-256k-250115",
    # model_name="doubao-seed-1-6-250615",
    model_name="deepseek-v3-1-terminus",
    description="云资源管控智能体",
    instruction="你是一个云资源管控专家，擅长通过 CCAPI 管理各类云资源",
    knowledgebase=knowledgebase,
    tools=[ccapi_mcp_toolset],
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=False,
            thinking_budget=0,
        )
    ),
)




# 创建独立的 RDS MySQL Agent
rds_mysql_agent: Agent = Agent(
    name="rds_mysql_agent",
    model_name="deepseek-v3-1-250821",
    description="RDS MySQL 运维智能体",
    instruction="你是一个 RDS MySQL 数据库运维专家",
    knowledgebase=knowledgebase,
    tools=[mcp_rds_mysql_local],
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
            thinking_budget=1024,
        )
    ),
)
#Prompt：哪个mysql数据库存在稳定性风险

# 创建本地 MCP CloudMonitor Tool
mcp_cloudmonitor_local = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="uvx",
            args=[
                "--from",
                "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_cloudmonitor",
                "mcp-server-cloudmonitor-stdio"
            ],
            env={
                "VOLCENGINE_ACCESS_KEY": os.getenv("VOLCENGINE_ACCESS_KEY", "your ak"),
                "VOLCENGINE_SECRET_KEY": os.getenv("VOLCENGINE_SECRET_KEY", "your sk")
            }
        ),
        timeout=180.0
    ),
    errlog=None
)

# 创建独立的 CloudMonitor Agent
cloudmonitor_agent: Agent = Agent(
    name="cloudmonitor_agent",
    model_name="deepseek-v3-1-terminus",
    description="云监控智能体",
    instruction="你是一个云监控专家，擅长通过 CloudMonitor 查看和分析云资源监控指标",
    knowledgebase=knowledgebase,
    tools=[mcp_cloudmonitor_local],
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=False,
            thinking_budget=0,
        )
    ),
)




# 创建独立的 Sec Agent
sec_agent: Agent = Agent(
    name="sec_agent",
    model_name="deepseek-v3-1-250821",
    description="安全运维智能体",
    instruction="你是一个安全运维专家",
    knowledgebase=knowledgebase,
    tools=[mcp_sec_toolset],
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
            thinking_budget=1024,
        )
    ),
    # enable_authz=True, # Sec Agent 需要用户认证鉴权后才能访问，使用permission控制
    # run_processor=AuthRequestProcessor(),
)

# 看一下哪个数据库存在稳定性风险
agent = Agent(
    name="ve_ai_ops_agent",
    model_name="deepseek-v3-1-terminus",
    description="AIOps agent",
    instruction="你是一个云计算运维专家，一次完整的云服务巡检需要包括TLS-MCP（日志）、VMP-MCP（监控指标）、ECS Assistant（主机诊断）、RDS-MySQL MCP（慢 SQL）、Sec-Agent（安全风险）、APMPlus-MCP（Tracing）",
    planner=PlanReActPlanner(),
    sub_agents=[
        # rds_mysql_agent,
        # cloudmonitor_agent,
        ccapi_agent,
        
    ],
    # tools=[ccapi_mcp_toolset],
    # tools=[AgentTool(ccapi_agent), AgentTool(rds_mysql_agent)],
    long_term_memory=long_term_memory,
    knowledgebase=knowledgebase,
)

root_agent = agent

from google.adk.apps.app import EventsCompactionConfig


agent_server_app = AgentkitAgentServerApp(
    agent=agent,
    short_term_memory=short_term_memory,
    # events_compaction_config=EventsCompactionConfig(
    #     compaction_interval=3,  # Trigger compaction every 3 new invocations.
    #     overlap_size=1          # Include last invocation from the previous window.
    # ),
)

if __name__ == "__main__":
    agent_server_app.run(host="0.0.0.0", port=8000)
