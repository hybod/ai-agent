from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from veadk import Agent
from veadk.config import getenv

### Gaode MCP Server
url = "https://mcp.amap.com/mcp?key={}".format(getenv("GAODE_MCP_API_KEY"))
mcp_hotel_finder = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=url, headers={"Authorization": f"Bearer {getenv('GAODE_MCP_API_KEY')}"}
    ),
)

root_agent = Agent(
    name="hotel_finder",
    description="酒店信息查找智能体",
    instruction="根据用户的需求，必要时调用高德地图MCP接口查询酒店信息",
    tools=[mcp_hotel_finder],
)
