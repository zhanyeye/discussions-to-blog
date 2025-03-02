FROM python:3.9-slim  

# 设置工作目录  
WORKDIR /github/workspace  

# 安装依赖  
COPY requirements.txt .  
RUN pip install --no-cache-dir -r requirements.txt  

# 复制脚本文件  
COPY entrypoint.py .  
COPY discussions_to_blog.py .  

# 设置默认入口  
ENTRYPOINT ["python", "entrypoint.py"]  