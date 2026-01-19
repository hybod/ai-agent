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

import os
import json
import logging
import hashlib
import base64
import requests
import asyncio
import threading
from typing import Optional, Dict, Any, Tuple
from Crypto.Cipher import AES

from veadk import Agent, Runner
from veadk.tools.builtin_tools.web_search import web_search
from agentkit.apps import AgentkitSimpleApp

import lark_oapi as lark
from lark_oapi.api.im.v1 import P2ImMessageReceiveV1

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = AgentkitSimpleApp()

# --- Configuration ---
LARK_APP_ID = os.getenv("LARK_APP_ID")
LARK_APP_SECRET = os.getenv("LARK_APP_SECRET")
LARK_ENCRYPT_KEY = os.getenv("LARK_ENCRYPT_KEY")
LARK_VERIFICATION_TOKEN = os.getenv("LARK_VERIFICATION_TOKEN")
DOCS_BASE = os.getenv("DOCS_BASE", "https://www.volcengine.com/docs")

# --- Lark Encryption Helper (For HTTP Webhook) ---
class AESCipher(object):
    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(AESCipher.str_to_bytes(key)).digest()

    @staticmethod
    def str_to_bytes(data):
        u_type = type(b"".decode('utf8'))
        if isinstance(data, u_type):
            return data.encode('utf8')
        return data

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]

    def decrypt(self, enc):
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:]))

    def decrypt_string(self, enc):
        enc = base64.b64decode(enc)
        return self.decrypt(enc).decode('utf8')

class LarkClient:
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.tenant_access_token = ""

    def get_token(self):
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        headers = {"Content-Type": "application/json; charset=utf-8"}
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        try:
            resp = requests.post(url, headers=headers, json=data)
            resp.raise_for_status()
            self.tenant_access_token = resp.json().get("tenant_access_token")
        except Exception as e:
            logger.error(f"Failed to get tenant_access_token: {e}")

    def reply_message(self, message_id, content):
        if not self.tenant_access_token:
            self.get_token()
        
        url = f"https://open.feishu.cn/open-apis/im/v1/messages/{message_id}/reply"
        headers = {
            "Authorization": f"Bearer {self.tenant_access_token}",
            "Content-Type": "application/json; charset=utf-8"
        }
        data = {
            "content": json.dumps({"text": content}),
            "msg_type": "text"
        }
        try:
            resp = requests.post(url, headers=headers, json=data)
            resp.raise_for_status()
            logger.info(f"Reply sent: {resp.json()}")
        except Exception as e:
            logger.error(f"Failed to reply message: {e}")
            # Retry once if token expired (simple logic)
            self.get_token()
            try:
                headers["Authorization"] = f"Bearer {self.tenant_access_token}"
                requests.post(url, headers=headers, json=data)
            except Exception as e2:
                logger.error(f"Retry failed: {e2}")

# --- Agent Setup ---

INSTRUCTION = f"""
【System Role】
You are the "VolcEngine Docs QA Assistant" (火山引擎文档问答助手). Your sole authoritative data source is the VolcEngine Official Documentation Center ({DOCS_BASE}).

【Responsibilities】
1. Understand and clarify the user's question (ask briefly if necessary).
2. Retrieve authoritative answers by searching the official documentation.
3. Provide answers with verifiable sources (Title/Section/URL).

【Data Source & Scope】
- ONLY use the official documentation. If not found, explicitly state "No authoritative basis found in official documentation" (未在官方文档中找到权威依据) and provide a general entry point.
- DO NOT fabricate APIs, parameters, quotas, error codes, etc.
- If versions differ, note the update date.

【Search & Evidence】
- Prioritize searching for Product Name, Feature, API Name, SDK, Console Page.
- Provide at least 1 verifiable reference:
  - Format: Document Title > Chapter > Section
  - Full URL

【Response Style】
- Language: Chinese (中文).
- Structure:
  1) Abstract (1 sentence/max 3 lines)
  2) Details (Steps, conditions, differences, notes)
  3) Code/Config (if needed, specify language/version)
  4) References (List with Title and URL)

【Safety & Compliance】
- DO NOT output APP_SECRET or ENCRYPT_KEY. Mask with "***".
- For billing/SLA/compliance, cite the original document.
- Refuse privacy/confidential questions.
"""

agent = Agent(
    name="VolcEngineDocsQA",
    description="An assistant for VolcEngine Documentation.",
    instruction=INSTRUCTION,
    tools=[web_search], # Enable web_search
)
runner = Runner(agent=agent)
lark_client = LarkClient(LARK_APP_ID, LARK_APP_SECRET)
cipher = AESCipher(LARK_ENCRYPT_KEY) if LARK_ENCRYPT_KEY else None


# --- Shared Message Processing ---
async def process_user_message(text: str, message_id: str):
    logger.info(f"Processing message: {text}")
    try:
        # Note: Runner is async
        response_text = await runner.run(messages=text)
        # Ensure response is a string
        if not isinstance(response_text, str):
            if isinstance(response_text, dict):
                 response_text = response_text.get("reply") or response_text.get("error") or str(response_text)
            else:
                 response_text = str(response_text)
        
        # Reply to Lark
        lark_client.reply_message(message_id, response_text)
    except Exception as e:
        logger.error(f"Agent execution failed: {e}")
        lark_client.reply_message(message_id, f"抱歉，系统暂时遇到问题：{str(e)}")

# --- Lark WebSocket Handler ---
def handle_ws_message(data: P2ImMessageReceiveV1):
    # Verify data structure before accessing
    if not data.event or not data.event.message:
        logger.warning("Received invalid WebSocket event data")
        return

    event = data.event
    message = event.message
    message_type = message.message_type
    message_id = message.message_id
    content_json = message.content
    
    if message_type == "text":
        try:
            content = json.loads(content_json)
            text = content.get("text", "")
            logger.info(f"[WebSocket] Received user prompt: {text}")
            
            # Use asyncio.run inside a new thread to avoid "asyncio.run() cannot be called from a running event loop"
            def run_async_task():
                # Create a new event loop for this thread to isolate execution
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    loop.run_until_complete(process_user_message(text, message_id))
                finally:
                    loop.close()
            
            threading.Thread(target=run_async_task).start()
            
        except json.JSONDecodeError:
            logger.error(f"Failed to decode message content: {content_json}")
    else:
        logger.info(f"Unsupported message type: {message_type}")

def start_lark_ws():
    if not LARK_APP_ID or not LARK_APP_SECRET:
        logger.warning("Lark App ID or Secret not set, skipping WebSocket client.")
        return

    logger.info("Starting Lark WebSocket Client...")
    
    # Use configured keys for event handler
    event_handler = lark.EventDispatcherHandler.builder(
        LARK_ENCRYPT_KEY or "", 
        LARK_VERIFICATION_TOKEN or ""
    ).register_p2_im_message_receive_v1(handle_ws_message).build()

    ws_client = lark.ws.Client(
        LARK_APP_ID, 
        LARK_APP_SECRET, 
        event_handler=event_handler, 
        log_level=lark.LogLevel.INFO
    )
    ws_client.start()

# --- Main Entry Point (HTTP) ---
@app.entrypoint
async def run(payload: dict, headers: dict) -> Dict[str, Any]:
    logger.info(f"Received payload: {payload}")

    # Handle direct invocation via agentkit invoke
    if "prompt" in payload and "token" not in payload and "encrypt" not in payload:
        logger.info("Handling direct invocation")
        prompt = payload["prompt"]
        try:
            response_text = await runner.run(messages=prompt)
            return {"reply": response_text}
        except Exception as e:
            logger.error(f"Agent execution failed: {e}")
            return {"error": str(e)}
    
    # 1. Decrypt if encrypted
    event = payload
    if "encrypt" in payload:
        if not cipher:
            logger.error("Received encrypted event but LARK_ENCRYPT_KEY is not set.")
            return {"code": 500, "msg": "Server Error"}
        
        try:
            decrypted_json = cipher.decrypt_string(payload["encrypt"])
            event = json.loads(decrypted_json)
            logger.info(f"Decrypted event: {event}")
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            return {"code": 403, "msg": "Decryption Failed"}

    # 2. Verify Token
    if event.get("token") != LARK_VERIFICATION_TOKEN:
        logger.warning(f"Verification token mismatch: {event.get('token')}")
        # Lark expects strict verification, but we return 403
        return {"code": 403, "msg": "Invalid Token"}

    # 3. Handle URL Verification (Challenge)
    if event.get("type") == "url_verification":
        return {"challenge": event.get("challenge")}

    # 4. Handle Message Event
    # Lark V2 event structure: { "schema": "2.0", "header": {...}, "event": {...} }
    if event.get("schema") == "2.0":
        header = event.get("header", {})
        event_type = header.get("event_type")
        
        if event_type == "im.message.receive_v1":
            event_data = event.get("event", {})
            message = event_data.get("message", {})
            message_type = message.get("message_type")
            message_id = message.get("message_id")
            content_json = message.get("content", "{}")
            
            if message_type == "text":
                content = json.loads(content_json)
                text = content.get("text", "")
                await process_user_message(text, message_id)
            else:
                 logger.info(f"Unsupported message type: {message_type}")

    return {"code": 0, "msg": "success"}

@app.ping
def ping() -> str:
    return "pong!"

if __name__ == "__main__":
    # Start WS client in a background thread
    ws_thread = threading.Thread(target=start_lark_ws, daemon=True)
    ws_thread.start()
    
    app.run(host="0.0.0.0", port=8000)
