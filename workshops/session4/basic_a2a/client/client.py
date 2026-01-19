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
        url="http://localhost:8000/",  # <--- url of A2A server
    )
    print(f"Remote agent name is {weather_agent.name}.")
    print(f"Remote agent description is {weather_agent.description}.")

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
