import asyncio
import sys
from veadk import Runner

from basic_agent.agent import root_agent as basic_agent
from builtintools_agent.agent import root_agent as builtintools_agent
from customtools_agent.agent import root_agent as customtools_agent
from multi_agents.agent import root_agent as multi_agent

agents = {
    "basic_agent": basic_agent,
    "builtintools_agent": builtintools_agent,
    "customtools_agent": customtools_agent,
    "multi_agent": multi_agent
}

async def run_agent(agent_name=None, message=None):
    if agent_name not in agents:
        print(f"Avaliable agents: {list(agents.keys())}")
        return
    
    runner = Runner(agents[agent_name])
    print(f"Running agent: {agent_name} with message: {message}")
    response = await runner.run(message)
    print(f"Running agent: {agent_name} response: {response}")
    
async def main():
    await run_agent(agent_name="basic_agent", message="hello")
    await run_agent(agent_name="builtintools_agent", message="How is the weather in Beijing?")
    await run_agent(agent_name="customtools_agent", message="roll a die and check prime numbers")
    await run_agent(agent_name="multi_agent", message="What clothing should I wear in Beijing?")
    
if __name__ == "__main__":
    asyncio.run(main())