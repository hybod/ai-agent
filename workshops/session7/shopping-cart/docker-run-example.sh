#!/bin/bash

# 运行 shopping-cart Docker 镜像的示例脚本
# 通过环境变量配置数据库和邮件参数

docker run -d \
  --name shopping-cart-app \
  --platform linux/amd64 \
  -p 9090:9090 \
  -e DB_HOST=mysql-server \
  -e DB_PORT=3306 \
  -e DB_NAME=shopping_cart_db \
  -e DB_USERNAME=app_user \
  -e DB_PASSWORD=secure_password \
  -e MAILER_EMAIL=noreply@example.com \
  -e MAILER_PASSWORD=email_app_password \
  shopping-cart:latest

echo "Shopping Cart 应用已启动"
echo "访问地址: http://localhost:9090/shopping-cart"
echo "查看日志: docker logs shopping-cart-app"
echo "停止应用: docker stop shopping-cart-app"
echo "删除容器: docker rm shopping-cart-app"
