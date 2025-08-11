# 基础镜像
FROM langchain/langgraph-api:3.11

# 将本地文件复制到容器中
ADD .. /deps/app

# 安装依赖
RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -c /api/constraints.txt -e /deps/*

# 修复路径问题：将 Windows 风格的路径转换为 Linux 风格路径
ENV LANGSERVE_GRAPHS='{"agent": "/deps/app/src/enrichment_agent/graph.py:graph"}'

# 设置工作目录
WORKDIR /deps/app
