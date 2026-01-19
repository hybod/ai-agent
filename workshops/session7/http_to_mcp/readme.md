# shopping cart agent 使用说明

## 配置文件
```markdown
# 在当前目录下面配置 config.yaml 文件如下：
# api_key 为模型使用
model:
  agent:
    api_key: 

# 如果要部署 agent 到 faas，需要填写下面的 ak/sk
volcengine:
  access_key: 
  secret_key: 

# for shopping cart mcp server，本 demo 中，如下配置必须填写
shopping_cart_mcp_api_key:
shopping_cart_mcp_tools_url: 
```