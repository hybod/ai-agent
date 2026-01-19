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


from google.adk.planners import BuiltInPlanner, PlanReActPlanner
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.genai import types
from veadk import Agent
from veadk.a2a.remote_ve_agent import RemoteVeAgent
from veadk.config import getenv

###Gaode MCP Server
url = "https://mcp.amap.com/mcp?key={}".format(getenv("GAODE_MCP_API_KEY"))
mcp_hotel_finder = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=url,
        # headers={"Authorization": f"Bearer {apikey}"}
    ),
)

remote_agent = RemoteVeAgent(
    name="travel_agent",
    # instruction="你是一个旅行规划顾问，负责旅行规划。",
    url="https://sd46699mfog2gt9o8rfu0.apigateway-cn-beijing.volceapi.com",  # <--- url from cloud platform
)

local_agent: Agent = Agent(
    name="lbs_analysis_agent",
    model_name="deepseek-v3-1-250821",
    description="地理位置信息智能体",
    instruction="你是一个地理位置信息专家",
    tools=[mcp_hotel_finder],
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
            thinking_budget=1024,
        )
    ),
)

root_agent = Agent(
    name="main_agent",
    model_name="deepseek-v3-1-250821",
    instruction="You are an planner agent.",
    planner=PlanReActPlanner(),
    sub_agents=[remote_agent, local_agent],
)
