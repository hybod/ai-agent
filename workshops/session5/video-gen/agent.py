import logging
from agentkit.apps import AgentkitSimpleApp
from google.adk.agents import RunConfig
from google.adk.agents.run_config import StreamingMode
from google.genai.types import Content, Part
from veadk import Runner
from veadk.agent_builder import AgentBuilder
from google.adk.tools.mcp_tool.mcp_toolset import (
    McpToolset,
    StdioServerParameters,
    StdioConnectionParams,
)

logger = logging.getLogger(__name__)
app_name = "storyvideo"

app = AgentkitSimpleApp()

agent_builder = AgentBuilder()

server_parameters = StdioServerParameters(
    command="npx",
    args=["@pickstar-2002/video-clip-mcp@latest"],
)
mcpTool = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=server_parameters,
        timeout=60.0
    ),
    errlog=None
)
agent = agent_builder.build(path="agent.yaml")
agent.tools.append(mcpTool)
runner = Runner(agent=agent, app_name=app_name)

@app.entrypoint
async def run(payload: dict, headers: dict):
    prompt = payload["prompt"]
    user_id = headers["user_id"]
    session_id = headers["session_id"]

    session_service = runner.short_term_memory.session_service
    try:
        await session_service.create_session(
            app_name=app_name, user_id=user_id, session_id=session_id
        )
        logger.info(f"Created new session: {session_id}")
    except Exception as e:
        if "already exists" in str(e).lower() or "AlreadyExistsError" in type(e).__name__:
            logger.info(f"Session {session_id} already exists, reusing it")
        else:
            raise

    new_message = Content(role="user", parts=[Part(text=prompt)])
    try:
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=new_message,
            run_config=RunConfig(streaming_mode=StreamingMode.SSE),
        ):
            # Format as SSE data
            sse_event = event.model_dump_json(exclude_none=True, by_alias=True)
            logger.debug("Generated event in agent run streaming: %s", sse_event)
            yield f"data: {sse_event}\n\n"
    except Exception as e:
        logger.exception("Error in event_generator: %s", e)
        yield f'data: {{"error": "{str(e)}"}}\n\n'


@app.ping
def ping() -> str:
    return "pong!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)