# 使用 Python 3.11.11 作为基础镜像
FROM python:3.11.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    git \
    cron \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY . /app/

# 安装 Python 依赖
RUN pip install --no-cache-dir -e .

# 设置环境变量
ENV PYTHONUNBUFFERED=1

# 创建 cron 任务文件
RUN echo "*/5 * * * * cd /app && python main.py >> /var/log/cron.log 2>&1" > /etc/cron.d/secretary-cron

# 设置 cron 日志文件权限
RUN touch /var/log/cron.log

# 给 cron 任务文件添加执行权限
RUN chmod 0644 /etc/cron.d/secretary-cron

# 启动 cron 服务
CMD cron && tail -f /var/log/cron.log 