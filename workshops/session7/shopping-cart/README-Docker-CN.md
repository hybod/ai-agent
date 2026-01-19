# Shopping Cart Docker 部署指南

## 概述

这个项目已经被打包成 Docker 镜像，支持通过环境变量配置数据库和邮件参数。镜像架构为 `linux/amd64`。

## 环境变量

应用支持以下环境变量配置：

| 环境变量 | 描述 | 默认值 |
|---------|------|--------|
| `DB_HOST` | 数据库主机地址 | `localhost` |
| `DB_PORT` | 数据库端口 | `3306` |
| `DB_NAME` | 数据库名称 | `shopping-cart` |
| `DB_USERNAME` | 数据库用户名 | `root` |
| `DB_PASSWORD` | 数据库密码 | `root123` |
| `MAILER_EMAIL` | 邮件发送地址 | `your_email` |
| `MAILER_PASSWORD` | 邮件应用密码 | `your_app_password` |

## 构建镜像

```bash
# 确保已经编译了 WAR 文件
mvn clean package

# 构建 Docker 镜像
docker build --platform linux/amd64 -t shopping-cart:latest .
```

## 运行方式

### 方式一：直接运行 Docker 容器

```bash
docker run -d \
  --name shopping-cart-app \
  --platform linux/amd64 \
  -p 9090:9090 \
  -e DB_HOST=your-mysql-host \
  -e DB_PORT=3306 \
  -e DB_NAME=shopping_cart_db \
  -e DB_USERNAME=your_db_user \
  -e DB_PASSWORD=your_db_password \
  -e MAILER_EMAIL=your_email@example.com \
  -e MAILER_PASSWORD=your_email_app_password \
  shopping-cart:latest
```

### 方式二：使用提供的脚本

```bash
# 编辑 docker-run-example.sh 中的环境变量
./docker-run-example.sh
```

### 方式三：使用 Docker Compose（推荐）

```bash
# 启动完整的应用栈（包含 MySQL 数据库）
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## 访问应用

应用启动后，可以通过以下地址访问：

- 应用地址：http://localhost:9090/shopping-cart
- 端口：9090

## 数据库初始化

如果使用 Docker Compose，MySQL 数据库会自动使用 `databases/mysql_query.sql` 文件进行初始化。

如果单独运行应用容器，需要确保：
1. MySQL 数据库已经运行
2. 数据库已经创建并导入了初始数据
3. 网络连接正常

## 常用命令

```bash
# 查看运行中的容器
docker ps

# 查看应用日志
docker logs shopping-cart-app

# 进入容器
docker exec -it shopping-cart-app bash

# 停止容器
docker stop shopping-cart-app

# 删除容器
docker rm shopping-cart-app

# 查看镜像
docker images shopping-cart
```

## 故障排除

1. **端口冲突**：如果 9090 端口被占用，可以修改端口映射：
   ```bash
   docker run -p 8080:9090 ...
   ```

2. **数据库连接失败**：检查数据库配置和网络连接：
   ```bash
   docker logs shopping-cart-app
   ```

3. **应用启动慢**：首次启动需要解压 WAR 文件，请等待约 10-15 秒

## 生产环境建议

1. 使用外部数据库而不是容器内的数据库
2. 设置合适的资源限制
3. 使用 Docker secrets 管理敏感信息
4. 配置健康检查
5. 使用反向代理（如 Nginx）

## 安全注意事项

- 不要在生产环境中使用默认密码
- 使用强密码和安全的数据库配置
- 考虑使用 Docker secrets 或环境变量文件来管理敏感信息
- 定期更新基础镜像和依赖
