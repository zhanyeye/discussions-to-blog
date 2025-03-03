#!/usr/bin/env python3  
import os  
import json
import discussions_to_blog  

def main():  
    # 从环境变量读取用户输入  
    github_token = os.getenv("INPUT_GITHUB_TOKEN")  
    repo_owner = os.getenv("INPUT_REPO_OWNER")  
    repo_name = os.getenv("INPUT_REPO_NAME")  
    category_id = os.getenv("INPUT_CATEGORY_ID")  
    output_dir = os.getenv("INPUT_OUTPUT_DIR", "content/posts")  
    delete_on_removed = os.getenv("INPUT_DELETE_ON_REMOVED", "false").lower() == "true"  

    # 检查必要参数是否存在  
    if not github_token or not repo_owner or not repo_name or not category_id:  
        raise ValueError("缺少必要的输入参数：github_token, repo_owner, repo_name, category_id")  

    # 读取 github.event.json 文件  
    event_file_path = "/github/workflow/event.json"  
    if not os.path.exists(event_file_path):  
        raise FileNotFoundError(f"无法找到 {event_file_path}，请确保在 GitHub Actions 中运行。")
    else:  
        with open(event_file_path, "r", encoding="utf-8") as f:  
            event = json.load(f)  
            print(f"[INFO] 读取事件文件：{event}")

    # 调用核心逻辑  
    discussions_to_blog.run(  
        github_token=github_token,  
        repo_owner=repo_owner,  
        repo_name=repo_name,  
        category_id=category_id,  
        output_dir=output_dir,  
        delete_on_removed=delete_on_removed,  
    )  

if __name__ == "__main__":  
    main()