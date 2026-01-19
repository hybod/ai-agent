import os
from veadk.integrations.ve_identity import IdentityClient
from volcenginesdkcore.rest import ApiException


async def create_oauth2_provider(identity_client: IdentityClient, mcp_url: str) -> str:
    """
    创建 OAuth2 credential provider

    Args:
        identity_client: IdentityClient 实例
        mcp_url: MCP 服务的 URL，例如 "https://sec-agent.mcp.volcbiz.com/mcp"

    Returns:
        OAuth2 credential provider
    """
    # 从 URL 中提取域名
    from urllib.parse import urlparse

    parsed_url = urlparse(mcp_url)
    hostname = parsed_url.hostname  # 例如: sec-agent.mcp.volcbiz.com

    # 提取第一部分作为 provider name
    provider_name = hostname.split(".")[0] if hostname else "default"

    # 构建 TokenEndpoint 和 RegisterEndpoint
    base_url = f"{parsed_url.scheme}://{hostname}"
    token_endpoint = f"{base_url}/auth/oauth/token"
    register_endpoint = f"{base_url}/auth/oauth/register"
    try:
        resp = await identity_client.create_oauth2_credential_provider_with_dcr(
            {
                "name": f"{provider_name}-oauth-provider",
                "vendor": 0,
                "config": {
                    "Scopes": ["read"],
                    "RedirectUrl": "https://auth.id.cn-beijing.volces.com/api/v1/oauth2callback",
                    "Oauth2Discovery": {
                        "AuthorizationServerMetadata": {
                            "AuthorizationEndpoint": "https://signin.volcengine.com/authorize/oauth/authorize",
                            "Issuer": "https://signin.volcengine.com",
                            "TokenEndpoint": token_endpoint,
                            "RegisterEndpoint": register_endpoint,
                        }
                    },
                },
            }
        )
        return resp.name
    except ApiException as e:
        if e.status == 409:
            print(f"OAuth2 provider 已存在: {e}")
        else:
            raise e
    except Exception as e:
        print(f"创建 OAuth2 provider 失败: {e}")


async def main():
    # RUNTIME_IAM_ROLE_TRN need to remove when run setup
    os.environ["RUNTIME_IAM_ROLE_TRN"] = ""
    
    identity_client = IdentityClient(region="cn-beijing")

    await create_oauth2_provider(
        identity_client, "https://ecs.mcp.volcbiz.com/cloud_assistant/mcp"
    )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
