# Shopping Cart Docker 部署

## 构建镜像
```bash
docker build -t shopping-cart:latest .
```

## 运行容器
```bash
docker run -d \
  --name shopping-cart-app \
  -p 9090:9090 \
  -e DB_HOST=host.docker.internal \
  -e DB_PORT=3306 \
  -e DB_NAME=shopping-cart \
  -e DB_USERNAME=root \
  -e DB_PASSWORD=root123 \
  -e MAILER_EMAIL=your_email@example.com \
  -e MAILER_PASSWORD=your_app_password \
  shopping-cart:latest
```

## 环境变量说明
- `DB_HOST`: 数据库主机地址 (默认: localhost)
- `DB_PORT`: 数据库端口 (默认: 3306)
- `DB_NAME`: 数据库名称 (默认: shopping-cart)
- `DB_USERNAME`: 数据库用户名 (默认: root)
- `DB_PASSWORD`: 数据库密码 (默认: root123)
- `MAILER_EMAIL`: 邮件发送地址
- `MAILER_PASSWORD`: 邮件应用密码

## 访问应用
应用将在端口 9090 上运行：
- 主页: http://localhost:9090/shopping-cart/
- API: http://localhost:9090/shopping-cart/ListProducts
- 图片: http://localhost:9090/shopping-cart/ShowImage?pid=P20230423084146
