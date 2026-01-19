import asyncio
from veadk import Runner
from veadk.agent_builder import AgentBuilder

agent_builder = AgentBuilder()

agent = agent_builder.build(path="basic_agent/agent.yaml")

root_agent = agent

if __name__ == "__main__":
    runner = Runner(agent)
    response = asyncio.run(runner.run("你能做啥"))
    print(response)