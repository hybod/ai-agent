from veadk import Runner
from veadk_web_agent.agent import root_agent as veadk_web_agent

async def main(message=None):
    runner = Runner(veadk_web_agent)
    response = await runner.run(message)
    print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main(message="hello"))