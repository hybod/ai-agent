from veadk import Agent
from veadk.a2a.remote_ve_agent import RemoteVeAgent
from veadk.runner import Runner
from veadk.tools.builtin_tools.web_search import web_search

image_generator = RemoteVeAgent(
    name="image_generator",
    url="http://127.0.0.1:8010/",
)

video_generator = RemoteVeAgent(
    name="video_generator",
    url="http://127.0.0.1:8011/",
)

root_agent = Agent(
    name="eposide_generator",
    model_name="deepseek-v3-1-terminus",
    description="调用子 Agents 生成首帧图和视频",
    instruction="""你可以根据用户输入的一段小说文字来生成视频，请注意，生成的视频中不要带有任何汉字。
    你需要完成如下几项任务：
    1. 调用网络搜索能力来检索相关素材，以便让你的提示词更加准确生动
    2. 使用 `image_generator` Agent 来生成一张视频首帧图，
    3. 根据这个首帧图的完整 URL，使用 `video_generator` Agent来生成一个视频
    4. 把完整的视频链接给用户。""",
    sub_agents=[image_generator, video_generator],
    tools=[web_search],
)
runner = Runner(agent=root_agent)


async def generate_image(prompt: str) -> str:
    """根据提示词生成图片

    Args:
        prompt (str): 图片生成的提示词

    Returns:
        str: 图片的 URL 链接
    """
    response = await runner.run(messages=prompt)
    return response


async def generate_video(prompt: str) -> str:
    """根据提示词和图片 URL 生成视频

    Args:
        prompt (str): 视频生成的提示词
        image_url (str): 视频生成的首帧图片 URL

    Returns:
        str: 视频的 URL 链接
    """
    response = await runner.run(messages=prompt)
    return response


if __name__ == "__main__":
    import asyncio

    response = asyncio.run(
        generate_image("请生成古文片段 落霞与孤鹜齐飞，秋水共长天一色 的首帧图片")
    )
    print(response)

    # response = asyncio.run(
    #     generate_video(
    #         prompt="请根据古文片段 落霞与孤鹜齐飞，秋水共长天一色 的首帧图，生成视频。首帧图片链接是 "
    #     )
    # )
    # print(response)
