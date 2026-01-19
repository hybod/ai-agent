from google.adk.a2a.utils.agent_to_a2a import to_a2a
from veadk import Agent
from veadk.tools.demo_tools import get_city_weather

agent = Agent(
    name="weather_agent",
    description="An agent that can get the weather of a city",
    tools=[get_city_weather],
)

app = to_a2a(agent=agent)
