# 使用一个轻量级的 Python 镜像  
FROM python:3.9-slim  

# 设置工作目录为 GitHub Actions 默认的工作区  
WORKDIR /github/workspace  

# 复制 Python 的依赖文件（如果有 requirements.txt）  
COPY requirements.txt .  

# 安装依赖  
RUN pip install --no-cache-dir -r requirements.txt  

# 复制所有文件到容器工作目录  
COPY . .  

# 调试：打印当前工作目录文件列表  
RUN echo "打印 /github/workspace 文件列表:" && ls -la /github/workspace  

# 声明入口文件 (entrypoint.py 必须存在于项目根目录)  
ENTRYPOINT ["python", "entrypoint.py"]  