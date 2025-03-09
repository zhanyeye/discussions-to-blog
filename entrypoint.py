#!/usr/bin/env python3  
import os
import json
import discussions_to_blog


def main():
    # 从环境变量读取用户输入
    output_dir = os.getenv("INPUT_OUTPUT_DIR", "content/posts")
    # 调用核心逻辑，统一利用事件文件内容处理
    discussions_to_blog.run(output_dir=output_dir)


if __name__ == "__main__":
    main()
