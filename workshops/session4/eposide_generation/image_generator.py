from google.adk.a2a.utils.agent_to_a2a import to_a2a
from veadk import Agent
from veadk.tools.builtin_tools.image_generate import image_generate

agent = Agent(
    name="image_generator",
    description="图像生成 Agent",
    instruction="你是一个原子化的 Agent，具备图像生成能力，每次执行完毕后，考虑回到主 Agent。",
    tools=[image_generate],
)

app = to_a2a(agent=agent)
