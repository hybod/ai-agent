FROM agentkit-cn-beijing.cr.volces.com/base/py-simple:python3.12-bookworm-slim_v1031_1

ENV UV_SYSTEM_PYTHON=1 UV_COMPILE_BYTECODE=1 PYTHONUNBUFFERED=1 DOCKER_CONTAINER=1

COPY requirements.txt requirements.txt

RUN uv pip install -r requirements.txt
EXPOSE 8000

WORKDIR /app

# Copy entire project
COPY . .

CMD ["python", "-m", "simple_agent"]