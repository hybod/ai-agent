import requests
import base64
from typing import Optional, Dict, Any
from os import getenv
from dotenv import load_dotenv

load_dotenv()

def get_m2m_access_token_with_basic_auth(
    token_endpoint: str,
    client_id: str,
    client_secret: str,
    scope: Optional[str] = None,
    audience: Optional[str] = None,
    additional_params: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """
    使用 HTTP Basic Authentication 请求 M2M AccessToken
    Args:
        token_endpoint: OAuth2 token endpoint URL
        client_id: M2M 客户端 ID
        client_secret: M2M 客户端密钥
        scope: 请求的权限范围 (可选)
        audience: 目标受众 (可选)
        additional_params: 额外的请求参数 (可选)
    Returns:
        包含 access_token 等信息的字典
    """
    # 构建请求数据 (不包含 client_id 和 client_secret)
    data = {
        "grant_type": "client_credentials",
    }
    # 添加可选参数
    if scope:
        data["scope"] = scope
    if audience:
        data["audience"] = audience
    if additional_params:
        data.update(additional_params)
    # 设置请求头
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }
    # 创建 Basic Auth 凭据
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode('utf-8')
    auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
    headers["Authorization"] = f"Basic {auth_b64}"
    try:
        # 发送 POST 请求
        response = requests.post(
            token_endpoint,
            data=data,
            headers=headers,
            timeout=30,
        )
        response.raise_for_status()
        token_response = response.json()
        if "access_token" not in token_response:
            raise ValueError("Response does not contain access_token")
        return token_response
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        raise
    except ValueError as e:
        print(f"Invalid response format: {e}")
        raise
if __name__ == "__main__":
    print(get_m2m_access_token_with_basic_auth(
        token_endpoint=getenv("ADK_OAUTH2_TOKEN_URL"),
        client_id=getenv("ADK_OAUTH2_CLIENT_ID"),
        client_secret=getenv("ADK_OAUTH2_CLIENT_SECRET"),
        scope="read",
    ))