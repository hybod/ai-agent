import logging
import os

from google.adk.planners import PlanReActPlanner
from google.adk.tools.mcp_tool.mcp_toolset import (
    StreamableHTTPConnectionParams,
)
from veadk import Agent
from veadk.config import getenv
from veadk.knowledgebase.knowledgebase import KnowledgeBase
from veadk.integrations.ve_identity import (
    VeIdentityMcpToolset,
    IdentityClient,
    oauth2_auth,
    AuthRequestProcessor,
)
from veadk.config import settings

my_ops_knowledge_collection = os.getenv(
    "DATABASE_VIKING_COLLECTION", "my_ops_collection"
)
# Knowledgebase usage
# Required env vars for viking knowledgebase
# Local VOLCENGINE_ACCESS_KEY, VOLCENGINE_ACCESS_KEY,
# Cloud: ServiceRole with VikingdbFullAccess permission
knowledgebase = KnowledgeBase(backend="viking", index=my_ops_knowledge_collection)
### depend on database_tos related configuration for import knowledgebase
knowledgebase.add_from_files(files=["./sop_aiops.md"])

identity_client = IdentityClient(region=settings.veidentity.region)

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

agent = Agent(
    name="ecs_agent",
    model_name="deepseek-v3-1-250821",
    description="ECS 运维智能体",
    instruction="你是一个 ECS 云服务器运维专家",
    planner=PlanReActPlanner(),
    tools=[mcp_ecs],
    knowledgebase=knowledgebase,
    run_processor=AuthRequestProcessor(),
)

root_agent = agent
