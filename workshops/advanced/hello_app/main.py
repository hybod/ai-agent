import asyncio
import time
from dotenv import load_dotenv

load_dotenv(override=True)

import os

import agent
from google.adk.agents.run_config import RunConfig

from google.adk.cli.utils import logs
from google.adk.runners import InMemoryRunner
from google.adk.sessions.session import Session
from google.genai import types

logs.log_to_tmp_folder()


async def main():
  app_name = 'my_app'
  user_id_1 = 'user1'
  runner = InMemoryRunner(
      agent=agent.root_agent,
      app_name=app_name,
  )
  session_11 = await runner.session_service.create_session(
      app_name=app_name, user_id=user_id_1
  )

  async def run_prompt(session: Session, new_message: str):
    content = types.Content(
        role='user', parts=[types.Part.from_text(text=new_message)]
    )
    print('** User says:', content.model_dump(exclude_none=True))
    async for event in runner.run_async(
        user_id=user_id_1,
        session_id=session.id,
        new_message=content,
    ):
      if event.content.parts and event.content.parts[0].text:
        print(f'** {event.author}: {event.content.parts[0].text}')

  async def run_prompt_bytes(session: Session, new_message: str):
    content = types.Content(
        role='user',
        parts=[
            types.Part.from_text(text=new_message)
        ],
    )
    print('** User says:', content.model_dump(exclude_none=True))
    async for event in runner.run_async(
        user_id=user_id_1,
        session_id=session.id,
        new_message=content,
        run_config=RunConfig(save_input_blobs_as_artifacts=False),
    ):
      if event.content.parts and event.content.parts[0].text:
        print(f'** {event.author}: {event.content.parts[0].text}')

  async def check_recipes_in_state(recipes_size: int):
    session = await runner.session_service.get_session(
        app_name=app_name, user_id=user_id_1, session_id=session_11.id
    )
    assert len(session.state['recipes']) == recipes_size
    for recipe in session.state['recipes']:
      assert isinstance(recipe, str)

  start_time = time.time()
  print('Start time:', start_time)
  print('------------------------------------')
  prompts = [
      '你好，我想吃点辣的。',
      '你们有螃蟹做的菜吗？',
      '听起来不错，就按你说的做一份吧。',
      '再来一份宫保鸡丁。',
      '我点完了，结账。',
  ]
  for prompt in prompts:
    await run_prompt(session_11, prompt)
  end_time = time.time()
  print('------------------------------------')
  print('End time:', end_time)
  print('Total time:', end_time - start_time)


if __name__ == '__main__':
  asyncio.run(main())