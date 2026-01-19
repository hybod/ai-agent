import os

from veadk import Agent, Runner
from veadk.a2a.remote_ve_agent import RemoteVeAgent


async def main(prompt: str) -> str:
    """Main function for run an agent.

    Args:
        prompt (str): The prompt to run.

    Returns:
        str: The response from the agent.
    """
    weather_agent = RemoteVeAgent(
        name="weather_agent",
        url=os.getenv("VEADK_A2A_URL"),
        auth_method="querystring",
        auth_token=os.getenv("VEADK_A2A_API_KEY"),
    )

    agent = Agent(
        name="root_agent",
        description="An assistant for fetching weather.",
        instruction="You are a helpful assistant. You can invoke weather agent to get weather information.",
        sub_agents=[weather_agent],
    )

    runner = Runner(agent=agent)
    response = await runner.run(messages=prompt)

    return response


if __name__ == "__main__":
    import asyncio

    response = asyncio.run(main("What is the weather like of Beijing?"))
    print(response)
