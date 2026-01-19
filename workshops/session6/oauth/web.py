import requests
import base64
import hmac
import hashlib
from typing import Optional, Dict, Any
from os import getenv
from dotenv import load_dotenv

load_dotenv()

def veidentity_initiate_auth(
    client_id,
    auth_flow,
    auth_parameters,
    pool_id,
    custom_domain,
    client_secret=None,
):
    """
    使用 veIdentity Auth Frost API 进行用户认证

    Args:
        client_id: 应用客户端ID
        auth_flow: 认证流程 (USER_PASSWORD_AUTH | REFRESH_TOKEN_AUTH)
        auth_parameters: 认证参数字典
        client_secret: 客户端密钥 (可选)
        custom_domain: 自定义域名 (可选)

    Returns:
        认证结果字典
    """
    # 设置请求头
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }
    # 如果有客户端密钥，计算 SECRET_HASH
    if client_secret:
        if auth_flow == "USER_PASSWORD_AUTH":
            message = auth_parameters["USERNAME"] + client_id
        elif auth_flow == "REFRESH_TOKEN_AUTH":
            message = auth_parameters["REFRESH_TOKEN"] + client_id
        else:
            message = ""

        secret_hash = base64.b64encode(
            hmac.new(client_secret.encode(), message.encode(), hashlib.sha256).digest()
        ).decode()
        auth_parameters["SECRET_HASH"] = secret_hash
        # 创建 Basic Auth 凭据
        # auth_string = f"{client_id}:{client_secret}"
        # auth_bytes = auth_string.encode('utf-8')
        # auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
        # headers["Authorization"] = f"Basic {auth_b64}"

    # 构建请求
    url = f"{custom_domain}/userpool/{pool_id}/api/v1/InitiateAuth"

    payload = {
        "AuthFlow": auth_flow,
        "AuthParameters": auth_parameters,
        "ClientId": client_id,
    }

    response = requests.post(url, json=payload)
    # print(response.json())

    # 检查响应状态，如果失败则显示详细错误信息
    if not response.ok:
        error_details = {
            "status_code": response.status_code,
            "reason": response.reason,
            "url": response.url,
            "headers": dict(response.headers),
        }
        # 尝试解析错误响应体
        try:
            error_body = response.json()
            error_details["error_body"] = error_body
            print(f"HTTP {response.status_code} Error:")
            print(f"  URL: {response.url}")
            print(f"  Response body: {error_body}")
        except ValueError:
            # 如果不是 JSON，显示原始文本
            error_text = response.text
            error_details["error_text"] = error_text
            print(f"HTTP {response.status_code} Error:")
            print(f"  URL: {response.url}")
            print(f"  Response text: {error_text}")
        # 抛出包含详细信息的异常
        raise requests.exceptions.HTTPError(
            f"HTTP {response.status_code} Error: {error_details}",
            response=response
        )
    token_response = response.json()
    # if "AccessToken" not in token_response:
    #     raise ValueError("Response does not contain access_token")
    return token_response

def reauthenticate_user(
    *,
    client_id: str,
    pool_id: str,
    preferred_username="workshop",
    preferred_password="Workshop@1",
    client_secret: Optional[str] = None,
):
    # Initialize veIdentity client
    auth_response = veidentity_initiate_auth(
        client_id=client_id,
        client_secret=client_secret,
        auth_flow="USER_PASSWORD_AUTH",
        auth_parameters={
            "USERNAME": f"{preferred_username}@example.com",
            "PASSWORD": preferred_password,
        },
        pool_id=pool_id,
        custom_domain=f"https://auth.id.cn-beijing.volces.com",
    )
    print(auth_response)
    bearer_token = auth_response["Result"]["AuthenticationResult"]["AccessToken"]
    return bearer_token


if __name__ == "__main__":
    access_token = reauthenticate_user(
        client_id=getenv("ADK_OAUTH2_CLIENT_ID"),
        client_secret=getenv("ADK_OAUTH2_CLIENT_SECRET"),
        pool_id=getenv("ADK_OAUTH2_POOL_ID"),
        preferred_username="workshop2",
        preferred_password="Workshop@1",
    )
    print(access_token)