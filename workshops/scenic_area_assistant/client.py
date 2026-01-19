import requests
import httpx
import random
import asyncio

from google.adk.cli.adk_web_server import CreateSessionRequest, RunAgentRequest
from google.genai.types import Content, Part


if __name__ == "__main__":
    # Step 0: setup running configs
    app_name = "scenic_area_companion"
    user_id = "agentkit_user"
    session_id = "agentkit_sample_session"
    # base_url = "http://127.0.0.1:8000"
    base_url = "https://sd5l4vg3al76cj6r9uti0.apigateway-cn-beijing.volceapi.com"
    api_key = ""

    task_num = 1

    # Step 1: create a session
    def create_session():
        create_session_request = CreateSessionRequest(
            session_id=session_id + f"_{random.randint(1, 9999)}",
        )

        response = requests.post(
            url=f"{base_url}/apps/{app_name}/users/{user_id}/sessions/{create_session_request.session_id}",
            headers={"Authorization": f"Bearer {api_key}"},
        )

        print(f"[create session] Response from server: {response.json()}")

        return create_session_request.session_id

    # 3. Handle streaming events
    async def send_request(message: str):
        current_session_id = create_session()
        run_agent_request = RunAgentRequest(
            app_name=app_name,
            user_id=user_id,
            session_id=current_session_id,
            new_message=Content(parts=[Part(text=message)], role="user"),
            stream=True,
        )

        print(f"[run agent] Sending request: {message}")
        try:
            with httpx.stream(
                "POST",
                f"{base_url}/run_sse",
                json=run_agent_request.model_dump(exclude_none=True),
                timeout=120,
                headers={"Authorization": f"Bearer {api_key}"},
            ) as r:
                for line in r.iter_lines():
                    print(line)
        except Exception as e:
            print(f"[run agent] Error: {e}")

    async def send_request_parallel():
        # Example: Pre-trip planning
        query = "我明天去北京动物园玩，2个大人1个小孩，预算2000元，帮忙规划一下行程和酒店、注意事项等"
        tasks = [send_request(query) for _ in range(task_num)]
        await asyncio.gather(*tasks)

    asyncio.run(send_request_parallel())
