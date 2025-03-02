# 使用一个轻量级的 Python 镜像  
FROM python:3.9-slim  

WORKDIR WORKDIR /app  

COPY requirements.txt .  

# 安装依赖  
RUN pip install --no-cache-dir -r requirements.txt  

# 复制所有文件到容器工作目录  
COPY . .  


# 声明入口文件 (entrypoint.py 必须存在于项目根目录)  
ENTRYPOINT ["python", "/app/entrypoint.py"]  entrypoint.py