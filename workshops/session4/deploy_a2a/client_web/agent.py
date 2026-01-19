import os

from veadk.a2a.remote_ve_agent import RemoteVeAgent

root_agent = RemoteVeAgent(
    name="weather_agent",
    url=os.getenv("VEADK_A2A_URL"),
    auth_method="querystring",
    auth_token=os.getenv("VEADK_A2A_API_KEY"),
)
