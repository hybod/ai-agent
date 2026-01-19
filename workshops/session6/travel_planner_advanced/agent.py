import os

from google.adk.planners import BuiltInPlanner
from google.adk.planners import PlanReActPlanner
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams
from google.genai import types
from veadk import Agent, Runner
from veadk.a2a.remote_ve_agent import RemoteVeAgent
from veadk.config import getenv
from veadk.knowledgebase.knowledgebase import KnowledgeBase
from veadk.memory.long_term_memory import LongTermMemory
from veadk.memory.short_term_memory import ShortTermMemory
from veadk.tools.demo_tools import get_city_weather
from veadk.utils.mcp_utils import get_mcp_params
from veadk.tools.builtin_tools.web_search import web_search

from agentkit.apps import AgentkitAgentServerApp

short_term_memory = ShortTermMemory(backend="local")

# long_term_memory = LongTermMemory(backend="local")
# Knowledgebase usage
# Required env vars for viking knowledgebase
# Local VOLCENGINE_ACCESS_KEY, VOLCENGINE_ACCESS_KEY, 
# Clooud: ServiceRole with VikingdbFullAccess permission
my_knowledge_collection = os.getenv("DATABASE_VIKING_COLLECTION", "my_collection")
knowledgebase = KnowledgeBase(
    backend="viking", 
    index=my_knowledge_collection
)
### depend on database_tos realated configuration for import knowledgebase
# knowledgebase.add_from_files(files=["./travel_qa.md"])
# knowledgebase.add_from_files(files=["https://aaa-bbb-ccc-ddd.tos-cn-beijing.volces.com/agentkit/travel_qa.md"])



# LTM Memory usage for memorybase/mem0
#backend = os.getenv("LONG_TERM_MEMORY_BACKEND", "mem0")
### Required env vars for memorybase 
#DATABASE_MEM0_BASE_URL=<url of mem0>
#DATABASE_MEM0_API_KEY=<apikey of mem0>
# long_term_memory_mem0 = LongTermMemory(
#         backend="mem0",
#         top_k=3,
#         app_name="my_app_name",
#     )


### Required env vars for VikingDB Memory 
# DATABASE_VIKINGMEM_COLLECTION=<collection_name> #index

my_memory_collection = os.getenv("DATABASE_VIKINGMEM_COLLECTION", "default_memory_collection")
long_term_memory = LongTermMemory(
            backend="viking",
            top_k=3,
            index=my_memory_collection,
        )

###Gaode MCP Server
url = "https://mcp.amap.com/mcp?key={}".format(getenv("GAODE_MCP_API_KEY"))
mcp_hotel_finder = MCPToolset(
        connection_params=StreamableHTTPConnectionParams(
        url=url,
        # headers={"Authorization": f"Bearer {apikey}"}
    ),
)

# remote_agent = RemoteVeAgent(
#     name="remote_hotel_book_agent",
#     # instruction="你是一个旅行规划顾问，负责旅行规划。",
#     url="https://sd46699mfog2gt9o8rfu0.apigateway-cn-beijing.volceapi.com" # <--- url from cloud platform
# )

lbs_agent_agent: Agent = Agent(
    name="lbs_analysis_agent",
    # model_name="doubao-1-5-pro-256k-250115",
    model_name="deepseek-v3-1-terminus",
    description="地理位置信息智能体",
    instruction="你是一个地理位置信息专家",
    # tools=[code_sandbox, web_search, browser_sandbox, las],
    #tools=[run_code, web_search, browser_sandbox, las],
    tools=[mcp_hotel_finder],
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
            thinking_budget=1024,
        )
    ),
)

search_agent: Agent = Agent(
    name="search_agent",
    # model_name="doubao-1-5-pro-256k-250115",
    model_name="deepseek-v3-1-terminus",
    description="信息搜索智能体",
    instruction="你是一个信息搜索专家",
    # tools=[code_sandbox, web_search, browser_sandbox, las],
    #tools=[run_code, web_search, browser_sandbox, las],
    tools=[web_search],
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
            thinking_budget=1024,
        )
    ),
)


agent = Agent(
    name="travel_planner_advanced",
    model_name="deepseek-v3-1-terminus",
    instruction="You are an planner agent.",
    planner=PlanReActPlanner(),
    sub_agents=[lbs_agent_agent, search_agent],
    long_term_memory=long_term_memory,
    knowledgebase=knowledgebase,
    
)

root_agent = agent



agent_server_app = AgentkitAgentServerApp(
    agent=agent, short_term_memory=short_term_memory,  
)

if __name__ == "__main__":
    agent_server_app.run(host="0.0.0.0", port=8000)
