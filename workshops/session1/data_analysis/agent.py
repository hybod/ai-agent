# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd. and/or its affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from veadk import Agent
from veadk.knowledgebase.knowledgebase import KnowledgeBase
from veadk.memory.long_term_memory import LongTermMemory
from veadk.memory.short_term_memory import ShortTermMemory
from veadk.tools.sandbox.code_sandbox import code_sandbox
from veadk.tools.sandbox.browser_sandbox import browser_sandbox
from veadk.tools.builtin_tools.web_search import web_search
from veadk.tools.builtin_tools.las import las
from veadk.utils.logger import get_logger
from . import prompt
from google.adk.planners.plan_re_act_planner import PlanReActPlanner
# from veadk.planners.react_planner import ReActPlanner
from google.genai import types

logger = get_logger(__name__)
APP_NAME= "data_analysis_agent"

# define your agent here
agent: Agent = Agent(
    name=APP_NAME,
    description="A data analysis for stock marketing",
    instruction="""
    Talk with user friendly. You can invoke your tools to finish user's task or question.
    Load memory and knowledgebase first. In case you already have answer from memory or knowledgebase, you can use it directly.
    Search data lake data firstly if las is available. Retrieve the dataset id through dataset name firstly.
    Then search knowledgebase. Make sure you can check memory and knowledgebase before you make any other search.
    Download the stock data thru sandbox if it is not available in las.
    * If trading data is not found, download the stock trading data using code_sandbox. You can use the Python library akshare to download relevant stock data.
    * After downloading, execute code through code_sandbox to avoid installation checks each time.
    * You can use the web_search tool to search for relevant company operational data.
    * If dependency libraries are missing, install them for the sandbox using Python code.
    * You can use the browser_sandbox tool to open a browser and view relevant data.
    """,
    tools=[las, code_sandbox, web_search, browser_sandbox],
    knowledgebase=KnowledgeBase(app_name=APP_NAME, backend="opensearch"),
    long_term_memory=LongTermMemory(app_name=APP_NAME, backend="opensearch"),
    # short_term_memory=ShortTermMemory(app_name=APP_NAME, backend="local"),
    global_instruction=prompt.GLOBAL_PROMPT.format(Domain_Name="data analysis for stock marketing"),
    generate_content_config=types.GenerateContentConfig(
            safety_settings=[
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                    threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                    threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
                )
            ]
        )
    )

# required from Google ADK Web
root_agent = agent

from google.adk.agents.run_config import RunConfig, StreamingMode

agent_run_config = RunConfig(
    streaming_mode=StreamingMode.SSE,
    support_cfc=True,
    max_llm_calls=150,
)
